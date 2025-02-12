import React, { useState } from 'react';
const apiUrl = import.meta.env.VITE_API_URL;

const CreateTeam = ({ navigate, setErrors }) => {

    const createTeam = async (e) => {
        e.preventDefault();
        setErrors('');

        try {
            const username = sessionStorage.getItem('username');
            const teamName = e.target[0].value; // Get team name from input
            const response = await fetch(`${apiUrl}users/createTeam/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, teamName }),
            });

            const data = await response.json();

            if (response.ok) {
                navigate('/profile');
            } else {
                setErrors(data.detail || 'Team creation failed. Please try again.');
            }
        } catch (err) {
            setErrors('An error occurred while creating the team. Please try again later.');
            console.error('Create team error:', err);
        }
    };

    return (
        <div className="createTeam">
            <form onSubmit={createTeam}>
                <input type="text" placeholder="Enter Teamname" />
                <button type="submit">Create</button>
            </form>
        </div>
    );
};

export default CreateTeam;
