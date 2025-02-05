import React, { useEffect, useState } from "react";
import './signup.css'

function FetchPoints({username}) {
    const [points, setPoints] = useState(0);
    const [error, setError] = useState(null);

    useEffect(() => {

        if (!username) {
            setError('Username not found');
            return;
        }

        const fetchedPoints = async () => {
            try {
                // Append the username as a query parameter
                const url = `http://localhost:8000/api/usersData/load_points/?username=${username}`;

                const response = await fetch(url, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',  // Although not needed for GET requests, it's fine to include it.
                    },
                });

                if (response.ok) {
                    const fetchedPoint = await response.json();
                    setPoints(fetchedPoint);
                } else {
                    setError('Failed to fetch points');
                }
            } catch (error) {
                setError('Error fetching points');
                console.error('Error fetching points:', error);
            }
        };

        fetchedPoints();
    }, [username]);

    // Return points or an error message
    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div className="fetchedPoints">
            <p>{points}</p>
        </div>
    )
}

export default FetchPoints;
