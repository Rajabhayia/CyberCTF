import React, { useState } from 'react';
const apiUrl = import.meta.env.VITE_API_URL;
import './challenges.css';

function Challenges({ challenges }) {
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [isFlagStatusOpen, setIsFlagStatusOpen] = useState(false);
  const [selectedChallenge, setSelectedChallenge] = useState(null);
  const [flag, setFlag] = useState('');
  const [flagStatus, setFlagStatus] = useState(''); // Stores flag status: 'correct' or 'incorrect'

  const togglePopup = (challenge) => {
    setSelectedChallenge(challenge);
    setIsPopupOpen(!isPopupOpen);
  };

  const submit = async (e) => {
    e.preventDefault();

    if (!selectedChallenge) return;

    const challengeID = selectedChallenge; // Using challenge name as the ID

    const response = await fetch(`${apiUrl}challenges/checkFlag/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ challengeID, flag }), // Send both challengeID and flag to backend
    });

    if (response.ok) {
      setFlagStatus('correct');
    } else {
      setFlagStatus('incorrect');
    }
    setIsFlagStatusOpen(true); // Show flag status popup
  };

  // Challenge Popup Content
  let popupContent = null;
  if (isPopupOpen && selectedChallenge) {
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
            <form onSubmit={submit}>
              <input
                type="text"
                placeholder="Enter your flag here"
                value={flag}
                onChange={(e) => setFlag(e.target.value)}
              />
              <button>Submit</button>
            </form>
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
          {flagStatus === 'correct' ? 'Well done! The flag is correct.' : 'Oops! The flag is incorrect.'}
        </div>
        <button onClick={() => setIsFlagStatusOpen(false)}>&#215;</button>
      </div>
    );
  }

  return (
    <div className="subTopic">
      {challenges && challenges.map((challenge, index) => (
        <div
          key={index}
          className="challenges"
          onClick={() => togglePopup(challenge)}
        >
          {challenge}
        </div>
      ))}

      {popupContent}

      {flagStatusContent}
    </div>
  );
}

export default Challenges;
