import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
const apiUrl = import.meta.env.VITE_API_URL;


const LeaderApproval = ({ userTeam, username, teamLeader, onRequestUpdate, currentUser }) => {
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    // Handle approval of a join request
    const handleApproval = async (event) => {
        event.preventDefault();

        setLoading(true);
        setError('');

        try {
            const response = await fetch(`${apiUrl}users/leaderApproval/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ userTeam, username, teamLeader, currentUser }),
            });

            const data = await response.json();

            if (response.ok) {
                onRequestUpdate(username, 'approved');
                location.reload();
            } else {
                setError(data.detail || 'Failed to approve request.');
            }
        } catch (err) {
            setError('An error occurred while approving the request.');
            console.error('Approval error:', err);
        } finally {
            setLoading(false);
        }
    };

    // Handle rejection of a join request
    const handleRejection = async (event) => {
        event.preventDefault();

        setLoading(true);
        setError('');
        try {
            const response = await fetch(`${apiUrl}users/rejectPendingRequest/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ userTeam, username, teamLeader, currentUser }),
            });

            const data = await response.json();

            if (response.ok) {
                // Call the callback to update the parent component's state
                onRequestUpdate(username, 'rejected');
                location.reload();
            } else {
                setError(data.detail || 'Failed to reject request.');
            }
        } catch (err) {
            setError('An error occurred while rejecting the request.');
            console.error('Rejection error:', err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className='leaderApproval-buttons'>
            {loading ? (
                <p>Loading...</p>
            ) : (
                <>
                    {error && <p style={{ color: 'red' }}>{error}</p>}
                    <form>
                        <button
                            type="button"
                            onClick={handleApproval}
                            disabled={loading}
                        >
                            Accept
                        </button>
                        <button
                            type="button"
                            onClick={handleRejection}
                            disabled={loading}
                        >
                            Reject
                        </button>
                    </form>
                </>
            )}
        </div>
    );
};

export default LeaderApproval;
