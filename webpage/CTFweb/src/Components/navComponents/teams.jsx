import React, { useState, useEffect } from "react";
const apiUrl = import.meta.env.VITE_API_URL;
import './signup.css'

function Teams() {
    const [teams, setTeams] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const globalTeams = async () => {
            try {
                const response = await fetch(`${apiUrl}usersData/load_team/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
    
                if (response.ok) {
                    const data = await response.json();
                    setTeams(data.teams); 
                } else {
                    setError('Failed to fetch users');
                }
            } catch (error) {
                setError('Error fetching users');
                console.error('Error fetching users:', error);
            }
        };

        globalTeams();
    }, []);

    if (error) {
        return <div>{error}</div>;
    }

    if (teams.length === 0) {
        return <div>Loading...</div>; 
    }

    return ( 
        <div className="NavUsers_Main">
            <div className="NavUsers_Header">
                <p>Teams</p>
            </div>
            <div className="NavUsers_Content">
                {teams.map((team, index) => (
                    <div key={index} className="fetchedPoint">
                        <div className="fetchedPoint-content">{team.TeamName}</div>
                        <div className="fetchedPoint-content">{team.points}</div>
                    </div>
                    ))}
            </div>
        </div>
    );
}

export default Teams;
