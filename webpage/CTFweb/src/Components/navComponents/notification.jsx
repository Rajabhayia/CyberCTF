import React from "react";
import LeaderApproval from "./teamAPIs/leaderApproval";
import './signup.css'

function Notification() {
    return ( 
        <div className="notification">
            <div className="notification-header">
                <p>Notifications</p>
            </div>
            <div className="notification-content">
                <p>No data Available</p>
            </div>
        </div>
    );
}

export default Notification;