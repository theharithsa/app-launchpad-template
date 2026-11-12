# Public product launch

Use this procedure for a public product launch or a refresh of its public materials. Start with the template's README structure, contributor and security guides, and static starter in `site/`. Confirm the live app and demo links, the intended audience, and the public scope with existing project decisions.

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
- Open the deployed URL at desktop and phone widths. Verify the screenshots, video, and app or demo links. Record the public URL and successful workflow run. A generated repository needs its own Pages settings and product assets.
