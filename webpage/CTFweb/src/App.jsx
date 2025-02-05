import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Nav from './Components/Nav.jsx';
import Content from './Components/content.jsx';
import Rules from './Components/navComponents/Rules.jsx';
import NavUsers from "./Components/navComponents/Navusers.jsx";
import Login from "./Components/navComponents/login.jsx";
import Signup from "./Components/navComponents/signup.jsx";
import Profile from "./Components/navComponents/profile.jsx";
import Settings from "./Components/navComponents/settings.jsx";
import Team from "./Components/navComponents/team.jsx";
import Notification from "./Components/navComponents/notification.jsx";

import './App.css';

function App() {
  return (
    <Router>
      <div className="main">
        <div className="nav">
          <Nav />
        </div>

        <div className="content">
          <Routes>
            <Route path="/" element={<Content />} />
            <Route path="/challenges" element={<Content />} />
            <Route path="/notification" element={<Notification />} />
            <Route path="/rules" element={<Rules />} />
            <Route path="/navUsers" element={<NavUsers />} />
            <Route path="/team" element={<Team />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
          </Routes>
        </div>

        <div className="footer">
          @ Oraganised by Raja bhayia
        </div>
      </div>
    </Router>
  );
}

export default App;

