// componenets/Navbar
import React, { useContext, useState } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import "../styles/Navbar.css";

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };

  const handleLogout = () => {
    logout();
    setDropdownOpen(false);
  };

  return (
    <nav className="navbar">
      <h1>
        <Link to="/">SignSecure</Link>
      </h1>
      <ul>
        {user ? (
          <>
            <li
              className="welcome-container"
              onClick={toggleDropdown}
            >
              <span>Welcome, {user}</span>
              {dropdownOpen && (
                <div className="dropdown-menu">
                  <button
                    onClick={handleLogout}
                    className="logout-btn"
                  >
                    Logout
                  </button>
                  <Link
                    to="/verify-signature"
                    className="dropdown-link"
                    onClick={() => setDropdownOpen(false)}
                  >
                    Verification page
                  </Link>
                </div>
              )}
            </li>
          </>
        ) : (
          <>
            <li>
              <Link to="/signin">Sign In</Link>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;
