import React, { useState } from 'react';
const apiUrl = import.meta.env.VITE_API_URL;

const JoinTeam = ({ setJoinRequestSent, setTeamNameRequested, setErrors }) => {
    const joinTeam = async (e) => {
        e.preventDefault();
        setErrors('');

        try {
            const username = sessionStorage.getItem('username');
            const teamName = e.target[0].value; // Get team name from input
            const response = await fetch(`${apiUrl}users/joinTeam/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, teamName }),
            });

            const data = await response.json();

            if (response.ok) {
                setJoinRequestSent(true);
                setTeamNameRequested(teamName);
            } else {
                setErrors(data.detail || 'Failed to send join request. Please try again.');
            }
        } catch (err) {
            setErrors('An error occurred while sending the join request. Please try again later.');
            console.error('Join team error:', err);
        }
    };

    return (
        <div className="joinTeam">
            <form onSubmit={joinTeam}>
                <input type="text" placeholder="Enter Teamname" />
                <button type="submit">Join</button>
            </form>
        </div>
    );
};

export default JoinTeam;
