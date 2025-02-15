import React, { useState } from "react";

const apiUrl = import.meta.env.VITE_API_URL;

function HandleRemoval({ username, points, teamLeader }) {
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleRemoval = async () => {
        setLoading(true);
        window.location.reload();
        try {
            const response = await fetch(`${apiUrl}users/handleRemoval/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, points, teamLeader }),
            });

            if (response.ok) {
                const data = await response.json();
                console.log("User removed successfully:", data);
                // You can handle success state here
            } else {
                const data = await response.json();
                setError(data.detail || 'Failed to remove the user');
            }
        } catch (error) {
            console.error('Error during the removal request:', error);
            setError('There was an error processing your request.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="HandleRemove-button">
            <button onClick={handleRemoval} disabled={loading}>
                {loading ? "Removing..." : "Remove"}
            </button>
            {error && <p className="error-handleRemoval">{error}</p>}
        </div>
    );
}

export default HandleRemoval;
