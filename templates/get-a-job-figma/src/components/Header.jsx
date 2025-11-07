import React from 'react'
import { Link } from 'react-router-dom'

export default function Header(){
  return (
    <header className="header">
      <div className="container inner">
        <div className="brand">GetAJob</div>
        <nav className="nav" aria-label="Main navigation">
          <Link to="/">Home</Link>
          <Link to="/page/1">Page 1</Link>
          <Link to="/page/2">Page 2</Link>
          <Link to="/page/3">Page 3</Link>
        </nav>
      </div>
    </header>
  )
}