````markdown name=templates/get-a-job-figma/CONVERSION_NOTES.md
```text
Conversion plan and notes

- I will run the export-figma.js script (requires FIGMA_TOKEN + FILE_KEY) to download SVGs and a pages snapshot.
- For each top-level page I will:
  - Create a React component in src/pages/ matching that page name (kebab-cased).
  - Export assets used on the page to src/assets/ (SVG, PNG, JPG as appropriate).
  - Implement plain CSS files scoped via component class names in src/styles/ or component-level css files.
  - Implement interactions: hover states, color changes, modals, forms, small animations.
  - Test responsiveness at mobile/tablet/desktop breakpoints.

- I will push incremental commits for each converted page under templates/get-a-job-figma on main so you can review.

Notes for you:
- If you prefer a PR-based workflow, tell me and I will create a feature branch and open a PR for review instead of pushing directly to main.
```
