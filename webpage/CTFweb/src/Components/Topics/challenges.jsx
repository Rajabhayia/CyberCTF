import React, { useState } from 'react';
const apiUrl = import.meta.env.VITE_API_URL;
import './challenges.css';

function Challenges({ challenges, solvedFlags, updateSolvedFlags }) {
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [isFlagStatusOpen, setIsFlagStatusOpen] = useState(false);
  const [selectedChallenge, setSelectedChallenge] = useState(null);
  const [flag, setFlag] = useState('');
  const [flagStatus, setFlagStatus] = useState('');
  const username = sessionStorage.getItem('username');

  const togglePopup = (challenge) => {
    setSelectedChallenge(challenge);
    setIsPopupOpen(!isPopupOpen);
  };

  const submit = async (e) => {
    e.preventDefault();

    if (!selectedChallenge) return;

    const challengeID = selectedChallenge; 

    const response = await fetch(`${apiUrl}users/checkFlag/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, challengeID, flag }),
    });

    if (response.ok) {
      setFlagStatus('correct');
      updateSolvedFlags(selectedChallenge); // Update the solvedFlags in the parent component
    } else {
      const errorData = await response.json();
      if (response.status === 401 && errorData.detail === 'Login first') {
        setFlagStatus('login_first');
      } else {
        setFlagStatus('oops! the flag is incorrect');
      }
    }
    setIsFlagStatusOpen(true);

    setTimeout(() => {
      setIsFlagStatusOpen(false);
    }, 1000 );

  };

  // Challenge Popup Content
  let popupContent = null;
  if (isPopupOpen && selectedChallenge) {
    const isSolved = solvedFlags.includes(selectedChallenge);

    popupContent = (
      <div className="popup">
        <div className="popupContent">
          <div className="challengeHit-Nav">
            <div className="challengeHit">
              <p>{selectedChallenge}</p>
            </div>
            <div className="challengeHit-button">
              <button onClick={() => setIsPopupOpen(false)}>&#215;</button>
            </div>
          </div>
          <div className="eventDetails">
            <p>No Data available</p>
            {isSolved ? (
              <div className="solvedQuestions">
                <p>Solved</p>
              </div>
            ) : (
              <form onSubmit={submit}>
                <input
                  type="text"
                  placeholder="Enter your flag here"
                  value={flag}
                  onChange={(e) => setFlag(e.target.value)}
                />
                <button>Submit</button>
              </form>
            )}
          </div>
        </div>
      </div>
    );
  }

  // Flag Status Popup Content
  let flagStatusContent = null;
  if (isFlagStatusOpen) {
    flagStatusContent = (
      <div className="flagPopup">
        <div className={`xflag${flagStatus === 'correct' ? '1' : '2'}`}>
          {flagStatus === 'correct' ? 'Well done! The flag is correct.' : `${flagStatus}`}
        </div>
        <button onClick={() => setIsFlagStatusOpen(false)}>&#215;</button>
      </div>
    );
  }

  return (
    <div className="subTopic">
      {challenges && challenges.map((challenge, index) => {
        const isSolved = solvedFlags.includes(challenge);

        return (
          <div
            key={index}
            className={`challenges ${isSolved ? 'green' : ''}`}
            onClick={() => togglePopup(challenge)}
          >
            {challenge}
          </div>
        );
      })}

      {popupContent}

      {flagStatusContent}
    </div>
  );
}

export default Challenges;
