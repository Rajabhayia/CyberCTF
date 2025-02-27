import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Nav.css";

function Nav() {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  // Effect hook to check if the username and points exists in sessionStorage
  useEffect(() => {
    const username = sessionStorage.getItem("username");
    console.log("Username in useEffect:", username);
    setIsAuthenticated(!!username);
  }, [sessionStorage.getItem('username')]);

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const closeDropdown = () => {
    setIsDropdownOpen(false);
  };

  const handleLogout = () => {
    sessionStorage.removeItem("username");
    console.log("Logged out, username removed:", sessionStorage.getItem("username"));
    setIsAuthenticated(false);
    navigate("/login"); // Redirect to login after logout
  };

  return (
    <div className="navmain">
      <div className="navLeft">
        <p>CyberCTF 2025</p>
      </div>

      <div className="navRight">
        <div className="hamburger" onClick={toggleDropdown}>
          &#9776;
        </div>

        <nav className={`navbar ${isDropdownOpen ? "open" : ""}`}>
          <Link to="/rules" className="nav-link" onClick={closeDropdown}>
            Rules
          </Link>
          <Link to="/navUsers" className="nav-link" onClick={closeDropdown}>
            Users
          </Link>
          <Link to="/teams" className="nav-link" onClick={closeDropdown}>
            Teams
          </Link>
          <Link to="/scoreboard" className="nav-link" onClick={closeDropdown}>
            Scoreboard
          </Link>
          <Link to="/challenges" className="nav-link" onClick={closeDropdown}>
            Challenges
          </Link>
          <hr />
          <Link to="/notification" className="nav-link" onClick={closeDropdown}>
            🔔 Notifications
          </Link>

          {isAuthenticated ? (
            <>
              <Link to="/team" className="nav-link" onClick={closeDropdown}>
                👥 Team
              </Link>
              <Link to="/profile" className="nav-link" onClick={closeDropdown}>
                👤 Profile
              </Link>
              <Link to="/settings" className="nav-link" onClick={closeDropdown}>
                ⚙️ Settings
              </Link>
              <button onClick={() => {handleLogout(); closeDropdown();}} className="nav-link logout-btn">
                🚪 Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="nav-link" onClick={closeDropdown}>
                Login
              </Link>
              <Link to="/signup" className="nav-link" onClick={closeDropdown}>
                Signup
              </Link>
            </>
          )}
        </nav>
      </div>
    </div>
  );
}

export default Nav;
