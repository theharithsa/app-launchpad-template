"""Check the documented JSON Schema subset using only the standard library.

Local $ref, type, const, enum, object/array/string constraints and if/then/allOf
and explicit additionalProperties are supported. No instance-supplied $schema URI is loaded and no network is used.
"""
from datetime import datetime
import json
import math
import re


def load_json(path):
    def reject_constant(value):
        raise ValueError('Invalid JSON numeric constant: ' + value)
    return json.loads(path.read_text(encoding='utf-8'), parse_constant=reject_constant)


KEYWORDS = frozenset({
    '$schema', '$id', '$defs', '$ref', 'title', 'description', 'type', 'const', 'enum',
    'required', 'properties', 'additionalProperties', 'minItems', 'items', 'minLength',
    'pattern', 'format', 'minimum', 'allOf', 'if', 'then',
})


def schema_errors(schema, location='$schema'):
    if not isinstance(schema, dict):
        return [f'{location}: expected schema object']
    errors = [
        f'{location}: unsupported schema keyword {key!r}'
        for key in sorted(schema.keys() - KEYWORDS)
    ]
    if 'format' in schema and schema['format'] != 'date-time':
        errors.append(f'{location}: unsupported schema format {schema["format"]!r}')
    for keyword in ('$defs', 'properties'):
        for name, child in schema.get(keyword, {}).items():
            errors.extend(schema_errors(child, f'{location}.{keyword}.{name}'))
    for keyword in ('items', 'if', 'then', 'additionalProperties'):
        if keyword not in schema or (keyword == 'additionalProperties' and type(schema[keyword]) is bool):
            continue
        errors.extend(schema_errors(schema[keyword], f'{location}.{keyword}'))
    for index, child in enumerate(schema.get('allOf', [])):
        errors.extend(schema_errors(child, f'{location}.allOf[{index}]'))
    return errors


def validate_shape(value, schema, location='$', document=None):
    document = schema if document is None else document
    problems = schema_errors(document)
    return problems or _validate_shape(value, schema, location, document)


def _validate_shape(value, schema, location, document):
    errors = []
    if '$ref' in schema:
        reference = schema['$ref']
        if not reference.startswith('#/'):
            return [f'{location}: unsupported non-local schema reference']
        target = document
        for part in reference[2:].split('/'):
            target = target[part.replace('~1', '/').replace('~0', '~')]
        return _validate_shape(value, target, location, document)
    types = {'object': lambda v: isinstance(v, dict), 'array': lambda v: isinstance(v, list),
             'string': lambda v: isinstance(v, str), 'null': lambda v: v is None,
             'integer': lambda v: type(v) is int or (type(v) is float and math.isfinite(v) and v.is_integer()),
             'number': lambda v: type(v) is int or (type(v) is float and math.isfinite(v)),
             'boolean': lambda v: type(v) is bool}
    expected = schema.get('type')
    expected = [expected] if isinstance(expected, str) else expected
    if expected and not any(types[kind](value) for kind in expected):
        return [f'{location}: expected {" or ".join(expected)}']
    same = lambda a, b: ((type(a) in (int, float) and type(b) in (int, float)) or type(a) is type(b)) and a == b
    if 'const' in schema and not same(value, schema['const']):
        errors.append(f'{location}: expected constant {schema["const"]!r}')
    if 'enum' in schema and not any(same(value, item) for item in schema['enum']):
        errors.append(f'{location}: expected one of {schema["enum"]}')
    if isinstance(value, dict):
        for key in schema.get('required', []):
            if key not in value:
                errors.append(f'{location}.{key}: required key missing')
        properties = schema.get('properties', {})
        for key, child in sorted(properties.items()):
            if key in value:
                errors.extend(_validate_shape(value[key], child, f'{location}.{key}', document))
        additional = schema.get('additionalProperties', True)
        for key in sorted(value.keys() - properties.keys()):
            if additional is False:
                errors.append(f'{location}.{key}: additional property is not allowed')
            elif isinstance(additional, dict):
                errors.extend(_validate_shape(value[key], additional, f'{location}.{key}', document))
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0):
            errors.append(f'{location}: needs at least {schema["minItems"]} items')
        if 'items' in schema:
            for index, item in enumerate(value):
                errors.extend(_validate_shape(item, schema['items'], f'{location}[{index}]', document))
    if isinstance(value, str):
        if len(value) < schema.get('minLength', 0):
            errors.append(f'{location}: nonempty text required')
        if 'pattern' in schema:
            pattern = schema['pattern']
            anchored = pattern.startswith('^') and pattern.endswith('$') and not pattern.endswith(r'\$')
            match = re.fullmatch(pattern, value) if anchored else re.search(pattern, value)
            if not match:
                errors.append(f'{location}: invalid format')
        if schema.get('format') == 'date-time':
            try:
                if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})', value):
                    raise ValueError('Expected RFC3339 timestamp')
                parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
                if parsed.tzinfo is None:
                    raise ValueError('Timezone missing')
            except ValueError:
                errors.append(f'{location}: expected timestamp with timezone')
    if type(value) in (int, float) and value < schema.get('minimum', value):
        errors.append(f'{location}: below minimum {schema["minimum"]}')
    for child in schema.get('allOf', []):
        errors.extend(_validate_shape(value, child, location, document))
    if 'if' in schema and not _validate_shape(value, schema['if'], location, document) and 'then' in schema:
        errors.extend(_validate_shape(value, schema['then'], location, document))
    return errors


def validate_record(root, name, value):
    try:
        schema = load_json(root / 'schemas' / f'{name}.schema.json')
        return validate_shape(value, schema)
    except (OSError, ValueError, KeyError, TypeError, AttributeError, re.error) as error:
        return [f'Cannot load {name} schema: {error}']
