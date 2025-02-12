import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const apiUrl = import.meta.env.VITE_API_URL;  // API URL from environment variables

const FetchUsers = () => {
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const username = sessionStorage.getItem('username');  // Get the username from sessionStorage

    if (!username) {
      setError('You are not logged in!');
      navigate('/login');  // Redirect to login if no username exists
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
          setUserData(data);  // Set profile data
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

  return { userData, error };
};

export default FetchUsers;
