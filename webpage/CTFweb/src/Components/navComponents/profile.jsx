import React from 'react';
import FetchUsers from './fetchAPIs/FetchUsers';
import { useNavigate } from 'react-router-dom';
import './signup.css';

function Profile() {
  const { userData, error } = FetchUsers();
  const navigate = useNavigate();

  if (error) {
    return <div>{error}</div>;
  }

  if (!userData) {
    return <div>Loading...</div>;
  }

  const handleNavigateToTeam = () => {
    navigate('/team');
  };

  return (
    <div className="profile">
      <h2>Welcome, {userData.username}!</h2>
      <p><strong>Email:</strong> {userData.email}</p>
      <div className="pointsEarned">
        <p><strong>Points earned:</strong> {userData.points}</p>
      </div>

      <div className="handleNavigateToTeam">
        <p><strong>Team:</strong></p>
        {userData.team === null ? (
          <div onClick={handleNavigateToTeam}>
            <p className="fontRed">click to create or join a team</p>
          </div>
        ) : (
          <p>{userData.team}</p>
        )}
      </div>
    </div>
  );
}

export default Profile;
