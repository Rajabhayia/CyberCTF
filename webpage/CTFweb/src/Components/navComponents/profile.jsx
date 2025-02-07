import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
const apiUrl = import.meta.env.VITE_API_URL;
import './signup.css';

function Profile() {
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const username = sessionStorage.getItem('username'); // Get the username from sessionStorage

    if (!username) {
      setError('You are not logged in!');
      navigate('/login'); // Redirect to login if no username exists
      return;
    }

    const fetchProfile = async () => {
      try {
        const response = await fetch(`${apiUrl}users/profile/?username=${username}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const data = await response.json();
          setUserData(data); // Set profile data
        } else {
          setError('Failed to fetch profile. Please try again later.');
        }
      } catch (error) {
        console.error('Error fetching profile:', error);
        setError('There was an error fetching the profile.');
      }
    };

    fetchProfile();
  }, [navigate]);


  if (error) {
    return <div>{error}</div>;
  }

  if (!userData) {
    return <div>Loading...</div>;
  }

  return (
    <div className="profile">
      <h2>Welcome, {userData.username}!</h2>
      <p>Email: {userData.email}</p>
      <div className="pointsEarned">
        <p>Points earned: {userData.points}</p>
      </div>
    </div>
  );
}

export default Profile;
