import React, { useState, useEffect } from "react";
import FetchPoints from "./fetchPoints";
const apiUrl = import.meta.env.VITE_API_URL;
import './signup.css'

function NavUsers() {
    const [users, setUsers] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const globalUsers = async () => {
            try {
                const response = await fetch(`${apiUrl}usersData/load_users/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
    
                if (response.ok) {
                    const data = await response.json();
                    setUsers(data.users); // Update the state with the list of usernames
                } else {
                    setError('Failed to fetch users');
                }
            } catch (error) {
                setError('Error fetching users');
                console.error('Error fetching users:', error);
            }
        };

        globalUsers(); // Fetch the users when the component mounts
    }, []); // Empty dependency array to run once when the component mounts

    if (error) {
        return <div>{error}</div>; // Display any error
    }

    if (users.length === 0) {
        return <div>Loading...</div>; // Display loading if no users yet
    }

    return ( 
        <div className="NavUsers_Main">
            <div className="NavUsers_Header">
                <p>Users</p>
            </div>
            <div className="NavUsers_Content">
                {users.map((user, index) => (
                    <div key={index} className="fetchedPoint">
                        <div className="fetchedPoint-content">{user}</div>
                        <div className="fetchedPoint-content">
                            <FetchPoints username={user}/>
                        </div>
                    </div>
                    ))}
            </div>
        </div>
    );
}

export default NavUsers;
