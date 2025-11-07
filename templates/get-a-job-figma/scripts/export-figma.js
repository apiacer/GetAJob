const fs = require('fs');
const path = require('path');
const https = require('https');

if (!process.env.FIGMA_TOKEN || !process.env.FIGMA_FILE_KEY) {
  console.error('\nERROR: Please set FIGMA_TOKEN and FIGMA_FILE_KEY environment variables.');
  console.error('See templates/get-a-job-figma/scripts/README.md for details.\n');
  process.exit(1);
}

const FIGMA_TOKEN = process.env.FIGMA_TOKEN;
const FILE_KEY = process.env.FIGMA_FILE_KEY;
const OUTPUT_DIR = path.join(__dirname, '..', 'src', 'assets');

function apiRequest(pathname) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.figma.com',
      path: pathname,
      method: 'GET',
      headers: { 'X-Figma-Token': FIGMA_TOKEN }
    };

    const req = https.request(options, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (err) { reject(err); }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

async function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

async function downloadFile(url, destPath) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(destPath);
    https.get(url, res => {
      if (res.statusCode !== 200) return reject(new Error('Download failed: ' + res.statusCode));
      res.pipe(file);
      file.on('finish', () => file.close(resolve));
    }).on('error', err => reject(err));
  });
}

(async () => {
  try {
    console.log('Fetching Figma file nodes...');
    const fileData = await apiRequest('/v1/files/' + FILE_KEY);

    // Basic node collection: gather top-level node ids for export
    const nodeIds = [];
    if (fileData && fileData.document && fileData.document.children) {
      fileData.document.children.forEach(page => {
        if (page && page.children) {
          page.children.forEach(child => {
            if (child.id) nodeIds.push(child.id);
          });
        }
      });
    }

    if (!nodeIds.length) {
      console.log('No nodes found for export.');
      return;
    }

    console.log(`Found ${nodeIds.length} nodes. Requesting images from Figma...`);
    const idsParam = nodeIds.join(',');
    const imagesRes = await apiRequest(`/v1/images/${FILE_KEY}?ids=${idsParam}&format=svg`);

    await ensureDir(OUTPUT_DIR);

    const images = imagesRes && imagesRes.images ? imagesRes.images : {};
    const keys = Object.keys(images);
    console.log(`Downloading ${keys.length} images to ${OUTPUT_DIR} ...`);

    for (const id of keys) {
      const url = images[id];
      if (!url) continue;
      const safeName = id + '.svg';
      const dest = path.join(OUTPUT_DIR, safeName);
      await downloadFile(url, dest);
      console.log('Saved', safeName);
    }

    // Also write a small JSON snapshot of top-level pages and their ids
    const pages = fileData.document.children.map(p => ({
      id: p.id,
      name: p.name,
      children: p.children ? p.children.map(c => ({ id: c.id, name: c.name })) : []
    }));
    fs.writeFileSync(path.join(OUTPUT_DIR, 'pages-snapshot.json'), JSON.stringify(pages, null, 2));
    console.log('Wrote pages-snapshot.json');

    console.log('Figma export complete. Review templates/get-a-job-figma/src/assets');
  } catch (err) {
    console.error('Export failed:', err.message || err);
    process.exit(1);
  }
})();
