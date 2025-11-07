````markdown name=templates/get-a-job-figma/scripts/README.md
```text
Figma export helper

This folder contains a small Node script that will download SVG exports for top-level nodes from your Figma file using the Figma REST API.

How to use
1. Create a Figma personal access token: https://www.figma.com/developers/api#access-tokens
2. From the Figma file URL, copy the file key (the long ID in the URL). Example: https://www.figma.com/file/<FILE_KEY>/...
3. From the repository root run:

   cd templates/get-a-job-figma
   export FIGMA_TOKEN=your_token_here
   export FIGMA_FILE_KEY=your_file_key_here
   node scripts/export-figma.js

4. The script will create or update templates/get-a-job-figma/src/assets/ and write a pages-snapshot.json that lists top-level pages and child node ids.

Notes
- The script requests SVGs for top-level child nodes. You can modify the script to request pngs or to filter by node name.
- This script is a helper to speed up the conversion; I will still inspect layers and create React components manually to match the designs.
```
