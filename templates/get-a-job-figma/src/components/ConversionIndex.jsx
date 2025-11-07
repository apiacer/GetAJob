import React from 'react'
import pagesSnapshot from '../assets/pages-snapshot.json'

export default function ConversionIndex(){
  const pages = pagesSnapshot || [];
  return (
    <div className="container">
      <h2>Conversion index (auto-generated)</h2>
      <p>This page lists the top-level pages found in the Figma file (if you ran the export script). Each entry will become its own React component during conversion.</p>
      <ul>
        {pages.map(p => (
          <li key={p.id}><strong>{p.name}</strong> — {p.children.length} child nodes</li>
        ))}
      </ul>
      <p>If pages-snapshot.json is missing, run the export script (see templates/get-a-job-figma/scripts/README.md).</p>
    </div>
  )
}