import React from "react";
import { Home, Plus, User } from "lucide-react"; 
import { Link } from "react-router-dom";  
import "../styles/Admin.css";
import logo from '../assets/images/Logo.png';

const Sidebar = () => {
  return (
    <div className="sidebar">
      <Link to="/">
          <img src={logo} alt="SmarTask Logo" className="logo-img" />
      </Link>
      <nav className="nav-links">
        <Link to="/admin" className="nav-item">
          <Home size={20} className="icon" /> Home
        </Link>
        <Link to="/admin/add_algor" className="nav-item"> 
          <Plus size={20} className="icon" /> Add Algorithm
        </Link>
      </nav>
      <div className="admin-btn">
        <Link>
          <button>
            <User size={20} className="icon" /> Admin
          </button>
        </Link>
      </div>
    </div>
  );
};

export default Sidebar;
