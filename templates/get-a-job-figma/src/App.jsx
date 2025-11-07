import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Placeholder from './pages/Placeholder'
import Header from './components/Header'
import Footer from './components/Footer'
import ConversionIndex from './components/ConversionIndex'

export default function App() {
  return (
    <div className="app-root">
      <Header />
      <main className="app-main">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/page/:id" element={<Placeholder />} />
          <Route path="/conversion" element={<ConversionIndex />} />
        </Routes>
      </main>
      <Footer />
    </div>
  )
}