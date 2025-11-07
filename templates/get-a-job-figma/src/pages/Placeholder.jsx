import React from 'react'
import { useParams } from 'react-router-dom'

export default function Placeholder(){
  const { id } = useParams()
  return (
    <div className="container">
      <h2>Figma Page {id} (placeholder)</h2>
      <div className="placeholder" style={{marginTop:16}}>
        <p>This is a placeholder for the Figma page {id}. I will extract assets, styles, and layout from the Figma file and implement pixel-faithful, responsive React components with plain CSS (hover/color changes/animations) as requested.</p>
      </div>
    </div>
  )
}