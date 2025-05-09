import React from 'react'

import { AiFillProduct } from 'react-icons/ai'
import { BiLogOut, BiSolidDashboard } from 'react-icons/bi'
import { BsDash } from 'react-icons/bs'
import { CgProfile } from 'react-icons/cg'
import { MdPayment } from 'react-icons/md'
import { SiShopify } from 'react-icons/si'
import { Link, Outlet } from 'react-router-dom'

const Home = () => {
  return <main className="main">
    <section className="sidebar">
        <div className="logo">
            <p className="text">Techno <strong>Panel</strong></p>
        </div>
        <div className="options">
            <Link to="/" className='select'><BiSolidDashboard size={30}/>Dashboard</Link>
            <Link to="/create" className='select'><CgProfile size={30}/>Create Client</Link>
        </div>
    </section>
    <section className="content">
        <Outlet/>
    </section>
  </main>
}

export default Home