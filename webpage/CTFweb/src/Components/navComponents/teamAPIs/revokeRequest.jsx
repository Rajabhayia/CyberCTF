import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import FetchUsers from '../fetchAPIs/FetchUsers';
import './team.css'

const apiUrl = import.meta.env.VITE_API_URL;

const RevokeRequest = ({ setJoinRequestSent, setErrors }) => {
    const { userData, error } = FetchUsers();
    const [teamNameRequested, setTeamNameRequested] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        if (userData?.message) {
            setTeamNameRequested(userData.message);
        }
    }, [userData]);

    const revokeRequest = async () => {
        setLoading(true);
        setErrors('');
        try {
            const username = sessionStorage.getItem('username');
            const response = await fetch(`${apiUrl}users/deleteRequest/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, teamName: teamNameRequested }),
            });

            const data = await response.json();

            if (response.ok) {
                setJoinRequestSent(false);
                setTeamNameRequested('');
                navigate('/profile');
            } else {
                setErrors(data.detail || 'Failed to revoke request. Please try again.');
            }
        } catch (err) {
            setErrors('An error occurred while revoking the request. Please try again later.');
            console.error('Revoke request error:', err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="joinRequestSent">
            {teamNameRequested && (
                <p>Your join request has been sent to Team {teamNameRequested}. <br /> Please wait for approval.</p>
            )}
            <button onClick={revokeRequest} disabled={loading}>
                {loading ? 'Revoking...' : 'Revoke Request'}
            </button>
        </div>
    );
};

export default RevokeRequest;

