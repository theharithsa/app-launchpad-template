# Documentation and public product launch

Use this procedure for a public product launch or a refresh of its public materials. Start with the template's README structure, contributor and security guides, and static starter in `site/`. Confirm the live app and demo links, the intended audience, and the public scope with existing project decisions.

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

## Repository guides

- Lead the README with the product name, audience, and main job it does. Link to the app, demo when available, and product page. Show a few real screenshots with descriptive alt text. Explain the actual stack, service boundaries, API and deployment where applicable, and give working local setup and test commands. Keep the template version marker and provenance.
- Keep `CONTRIBUTING.md` actionable. Explain issue intake, development setup, isolated test data, expected checks, and what to include in a PR.
- Keep `SECURITY.md` accurate to the current implementation and link a working private reporting channel. For a public GitHub repository, enable and verify private vulnerability reporting during authorized setup. For other visibility or hosting choices, document the maintainer's verified private route. Keep vulnerability details out of public issues. [GitHub private reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository)

## Screenshots and video

- Capture the real product in its public demo or an isolated test account with fictional data. Check the images for identifiers, credentials, private URLs, and real records before publication. Use the same reviewed assets in the README and landing page.
- Use the installed `/brag` skill to make a short product video. Use `/brag-slim` if that is the installed variant. Show the starting point, a representative action, and its result. Verify readable text, playback, and audio when used. Keep a poster and share copy with the launch deliverables.
- Put the approved screenshots, poster, and web-ready video under `site/media/`. Keep rendering inputs, intermediate files, and test data outside the public artifact. If product footage is pending, publish only the material that has been reviewed and record the missing deliverable.

## GitHub Pages

- Use the static `site/` directory for the product page unless the project has selected another host. Replace the starter copy with product-specific content and link to the app, demo, help, and repository as applicable. Use relative paths for local assets so the page works under the repository URL. Include a responsive gallery and a video player with controls and a poster.
- The bundled `product-pages.yml` packages site changes on PRs with read-only access. When the project is ready to publish, select **GitHub Actions** as the Pages source and allow the default branch in the `github-pages` environment. The publish job uses Pages and OIDC permissions only after packaging and runs from the default branch with Pages enabled. [GitHub Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- Publish the curated build output only. Keep credentials, customer records, sensitive operational details, and private runbooks out of the artifact. If public docs describe features available only after production deployment, publish those docs from the verified production revision. A staged candidate can produce its own private review evidence.
- Verify the changed public URLs and source revision after publication. The starter stamps generated guides with the Actions revision. A Pages failure has its own status even when the product deploy succeeded.
- Open the deployed URL at desktop and phone widths. Verify the screenshots, video, and app or demo links. Record the public URL and successful workflow run. A generated repository needs its own Pages settings and product assets.

## Roadmap and release history

- Explain the user outcome, expected audience and availability for each roadmap item. Use target windows for planned work. Show the gates between foundations, pilots and wider rollout with an accessible, responsive diagram and equivalent readable text.
- Keep a version index with stable links and concise highlights in plain language. Distinguish planned, unpublished and shipped work. Backfill from the changelog and verified publication records, and retain the original version of any historical capture. Mark entries without publication evidence as changelog history.
- Maintain public roadmap and release-note sources together under a dedicated documentation directory. Publish only curated files. Link the roadmap and release notes from the user guide and verify the rendered pages and historical links at phone and desktop widths.
