import React from "react";
import './settings.css'

function Settings() {
    return ( 
        <div className="settings">
            <div className="settingsHead">Settings</div>
            <div className="settingsContent">
                <div className="settingsProfile">Update Profile</div>
                <div className="settingsTeam">Update and Change Team</div>
                <div className="settingsPassword">Reset Password</div>
            </div>
        </div>
    );
}

export default Settings;