import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => (
  <nav className="navbar fixed-top navbar-expand-lg navbar-dark bg-gradient-bt">
    <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
      <span className="navbar-toggler-icon" />
    </button>
    <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
      <div className="navbar-nav ml-auto">
        <Link className="nav-link" to="/features">features</Link>
        <Link className="nav-link" to="/predict">predict <span className="sr-only">(current)</span></Link>
        <Link className="nav-link" to="/history">history</Link>
      </div>
    </div>
  </nav>

);


export default Navbar;
