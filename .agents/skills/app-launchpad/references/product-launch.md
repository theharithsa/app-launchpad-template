# Documentation and public product launch

Use this procedure for a public product launch or a refresh of its public materials. Start with the template's README structure, contributor and security guides, and static starter in `site/`. Confirm the live app and demo links, the intended audience, and the public scope with existing project decisions.

## Public entry and recovery

1. Map each shipped user-facing workflow to its audience, starting control, input and visible result. Group related tasks around the user's day. Give each group a concrete example and a guide or demo link. Explain limits where they affect the user's choice. Mark planned features explicitly. Read the current routes and run the workflows before writing the copy.
2. Serve the product landing at the signed-out root. Give sign-in its own reachable route and the workspace its own protected entry. Preserve bookmarked links, invitation or password-reset callbacks and existing sessions. If a public demo exists, open it directly with fictional data. For products without accounts, use their real primary action.
3. Share the header, footer, type, colors, motion preferences and mobile navigation across the landing, help, technical docs and policies. Use the same vocabulary as the product. Link privacy, terms and security from every public page. Cover actual data, providers, retention/deletion options, terms of use, support and the verified private reporting route. Replace every template identity and contact before publishing. Check the form or mailbox with the owner. Keep policies specific to the product.
4. Return a branded 404 with an actual HTTP 404 for an unknown nested URL. Provide branded 5xx recovery pages for the statuses the host can serve, with a plain-language next action. A published example is a preview until the host returns that status. On a failed save, help the user check what was recorded before retrying. Keep the brand animation brief and decorative. Essential text and navigation must work with animation and JavaScript disabled.
5. When a product has both an application host and a Pages mirror, keep the public home, guides, policies, sign-in, demo and first-party API reachable from the application origin. Use relative staging links and the correct repository mount on Pages. Use a verified custom domain when available. Check HTTPS, the www redirect, allowed login domain, nested 404s and an existing deep link in the deployed environment. Change only the DNS records the hosting provider requests.
6. Start a clean desktop and phone session at the public root. Read a real example, follow a guide, try the demo or sign-in, play and seek the tour, and recover from a mistyped nested URL. Also check keyboard focus, reduced motion, captions and the transcript. Record the tested URLs and outcomes.

The starter stores its product and policy facts in `docs/public-guides.json` and its homepage copy in `site/index.html`. Set `publicSite.repository`, `pagesBase` and the primary action for the new project. An app with accounts sets `signInPath` to its local route and `appOrigin` to its verified HTTPS origin. Build with `--hosting` for same-host links and a root-mounted 404. The ordinary build targets the Pages mount. Point the application's host at the generated root and 404 file, and route only known app or auth paths to the application.

## Documentation on every PR

Update affected documentation alongside the change, before merge. In the PR's
**Documentation impact** section, give one decision line. Use `Updated:` with the
affected guides or links. Use `No change:` with the reason when existing docs
still apply. Review what the change actually affects. A green check confirms
the entry exists and that the site builds, while the PR review checks accuracy.

| Guide | Update when |
| --- | --- |
| Product handbook | A user workflow, feature, permission outcome, or troubleshooting step changes. |
| Technical guide | Architecture, services, API contracts, integration, or setup changes. |
| Settings reference | A setting's location, default, scope, permission, or timing changes. |
| SDLC guide | Intake, release authority, branch routing, promotion, or recovery policy changes. |
| CI/CD pipeline | A workflow trigger, job dependency, environment, gate, or publication step changes. Keep a readable ordered flow aligned with the real pipeline. |

Use project facts and mark proposed capabilities clearly. Apps with existing
guides should retain their generator and sources. Wire their actual docs build,
generated-reference consistency checks if used, and link checks into required
PR CI. Projects using the template starter edit `docs/public-guides.json` and
run `python3 scripts/build_public_docs.py`. Maintainers add an impact decision
to bot-authored PRs before merge too.

## First-time reader walkthrough

For new or materially changed public guides, review the content against the
actual app, source and deployed contracts. Use the template as a structure.
Write for each audience using project-specific behaviour:

- **Product handbook**. Explain the entry point, prerequisites, exact controls,
  who can perform the task, what the user should see or what changes after the
  step, and what to do if it fails. Cover changed workflows and the common tasks
  needed to use them. Make demo, signed-in, permission-restricted and planned
  functionality clear where those distinctions affect the task.
- **Technical guide**. Identify the components, service and data boundaries,
  prerequisites and configuration. Run the published setup commands from a
  clean checkout and state how the reader can tell they worked. Where there is
  a public API, start with an unauthenticated read if one exists, then show a
  scoped request and its success response and likely error cases. Use isolated
  accounts or emulators for authenticated verification and writes.
- **Settings, delivery and planning**. Explain defaults, scope and access for
  affected settings. For delivery and pipeline changes, identify what enters
  each gate, what passing proves and what to inspect on failure. Link roadmap
  gates to their source issues or milestones. Use recorded target windows and
  label unscheduled work accordingly.

Follow the affected paths as a first-time reader. Start from the app, product
site or repository entry point a reader would use. Find the guide without an
internal link, follow its steps without relying on prior setup, and compare the
observed result with what it promises. If the owner supplies a published
reference, open it and compare task coverage, permission details and the
depth of troubleshooting. Use that comparison to identify content gaps.

Record the path, tested revision or environment, commands or actions, expected
and observed outcomes, and any unresolved gap in the PR or linked evidence.
Fix inaccurate or unclear instructions and repeat the affected path on the
candidate before merge. After authorized publication, open the live guides at
desktop and phone widths and repeat the public entry-point and task checks.
Keep clean-checkout, demo, synthetic and live observations distinct. Mark
live verification as pending when publication or access is outside scope.
A successful build or link check alone does not complete this review.

## Repository guides

- Lead the README with the product name, audience, and main job it does. Link to the app, demo when available, and product page. Show a few real screenshots with descriptive alt text. Explain the actual stack, service boundaries, API and deployment where applicable, and give working local setup and test commands. Keep the template version marker and provenance.
- Keep `CONTRIBUTING.md` actionable. Explain issue intake, development setup, isolated test data, expected checks, and what to include in a PR.
- Keep `SECURITY.md` accurate to the current implementation and link a working private reporting channel. For a public GitHub repository, enable and verify private vulnerability reporting during authorized setup. For other visibility or hosting choices, document the maintainer's verified private route. Keep vulnerability details out of public issues. [GitHub private reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository)

## Screenshots and video

- Capture the real product in its public demo or an isolated test account with fictional data. Check the images for identifiers, credentials, private URLs, and real records before publication. Use the same reviewed assets in the README and landing page.
- Use the installed `/brag` skill to record the complete primary workflow. Start at the public entry, perform the main actions with fictional data and show the resulting persisted state or calculation. Include connected modules when they change the outcome. Choose a duration that lets a first-time viewer follow the controls, add chapters, captions and a text transcript, and verify playback and seeking on phone and desktop. A short teaser is an optional additional asset. Use `/brag-slim` if that is the installed variant. Show the starting point, a representative action, and its result. Verify readable text, playback, and audio when used. Keep a poster and share copy with the launch deliverables.
- Put the approved screenshots, poster, and web-ready video under `site/media/`. Keep rendering inputs, intermediate files, and test data outside the public artifact. If product footage is pending, publish only the material that has been reviewed and record the missing deliverable.

## GitHub Pages

- Use the static `site/` directory for the product page unless the project has selected another host. Replace the starter copy with product-specific content and link to the app, demo, help, and repository as applicable. Use relative paths for local assets so the page works under the repository URL. Include a responsive gallery and a video player with controls and a poster.
- The bundled `product-pages.yml` packages site changes on PRs with read-only access. When the project is ready to publish, select **GitHub Actions** as the Pages source and allow the default branch in the `github-pages` environment. The publish job uses Pages and OIDC permissions only after packaging and runs from the default branch with Pages enabled. [GitHub Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- Publish the curated build output only. Keep credentials, customer records, sensitive operational details, and private runbooks out of the artifact. If public docs describe features available only after production deployment, publish those docs from the verified production revision. A staged candidate can produce its own private review evidence.
- Verify the changed public URLs and source revision after publication. The starter stamps generated guides with the Actions revision. A Pages failure has its own status even when the product deploy succeeded.
- Follow the [first-time reader walkthrough](#first-time-reader-walkthrough) after publication. Verify screenshots, video and app or demo links when affected. Record the public URL and successful workflow run. A generated repository needs its own Pages settings and product assets.

## Roadmap and release history

- Explain the user outcome, expected audience and availability for each roadmap item. Use target windows for planned work. Show the gates between foundations, pilots and wider rollout with an accessible, responsive diagram and equivalent readable text.
- Keep a version index with stable links and concise highlights in plain language. Distinguish planned, unpublished and shipped work. Backfill from the changelog and verified publication records, and retain the original version of any historical capture. Mark entries without publication evidence as changelog history.
- Maintain public roadmap and release-note sources together under a dedicated documentation directory. Publish only curated files. Link the roadmap and release notes from the user guide and verify the rendered pages and historical links at phone and desktop widths.
