import './styles/main.css'
import { useState } from 'react'
import Interfaces from './components/Interfaces'
import { Routes, Route } from 'react-router-dom'
import Home from './components/Home'

function App() {
  return (
    <Routes>
      <Route path='/*' element={<Home/>}>
        <Route index element={<Interfaces/>}/>
        <Route path='status' element={<Interfaces/>} />
      </Route>
    </Routes>
  )
}

export default App
