import React from "react";
import './Rules.css'; // Make sure to import the CSS for styling

function Rules() {
  return (
    <div className="rules-container">
      <h2>Rules of CyberCTF 2025</h2>
      <ul className="rules-list">
        <li>The CTF starts on 25th March, 2025 at 6 PM and lasts exactly 36 hours.</li>
        <li> A Team is neccessary to Participate in this competition.</li>
        <li>A team size of a maximum of 3 is allowed.</li>
        <li>The flag format is CyberCTF&#123; &#125;  unless otherwise stated.</li>
        <li>The organizers of this event reserve the right to refuse the eligibility of prizes if any situation of malpractice arises.</li>
        <li>Please refrain from discussing strategy and solutions during the contest.</li>
        <li>CTF organizers' decisions are final.</li>
        <li>The person could have an unlimited number of submissions in most cases, but brute-forcing a server would be penalized and would result in an IP ban and discarding the team from the contest.</li>
        <li>Attacking, DoSing, or otherwise deliberately harming the event infrastructure is strictly prohibited and will result in an immediate ban and block from the event.</li>
      </ul>
    </div>
  );
}

export default Rules;
