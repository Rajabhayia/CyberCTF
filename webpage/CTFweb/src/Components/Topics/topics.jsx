import React, { useState, useEffect } from 'react';
import Challenges from './challenges.jsx';
const apiUrl = import.meta.env.VITE_API_URL;
import './topics.css';

function Topics() {
  const [challenges, setChallenges] = useState([]);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [flag, setFlag] = useState([]);
  const username = sessionStorage.getItem('username');

  useEffect(() => {
    const fetchChallenges = async () => {
      try {
        const response = await fetch(`${apiUrl}challenges/challengesData/?userName=${username}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const challengesData = await response.json();
          setChallenges(challengesData.data);

          // Update flag state without duplicates
          setFlag(prevFlag => {
            const newSolved = challengesData.solved || [];
            const updatedFlag = prevFlag.concat(newSolved);
            
            const uniqueFlag = [];
            for (let i = 0; i < updatedFlag.length; i++) {
              if (!uniqueFlag.includes(updatedFlag[i])) {
                uniqueFlag.push(updatedFlag[i]);
              }
            }
          
            return uniqueFlag;
          });

        } else {
          setError('Failed to fetch challenges!');
        }
      } catch (error) {
        console.error('Error fetching challenges:', error);
        setError('There was an error fetching the challenges.');
      }
    };

    fetchChallenges();
  }, [username]);  // Only fetch challenges when `username` changes

  // Open the modal and set the selected topic
  const openModal = (topic) => {
    setSelectedTopic(topic);
    setIsModalOpen(true);
  };

  // Close the modal
  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedTopic(null);
  };

  // Update the solved flag after a successful flag submission
  const updateSolvedFlags = (newFlag) => {
    setFlag((prevFlag) => {
      const updatedFlag = prevFlag.concat(newFlag);

      // Remove duplicates manually
    const uniqueFlag = [];
    for (let i = 0; i < updatedFlag.length; i++) {
      if (!uniqueFlag.includes(updatedFlag[i])) {
        uniqueFlag.push(updatedFlag[i]);
      }
    }
      return uniqueFlag
    });
  };

  return (
    <div className="topics">
      {error && <p className="error">{error}</p>}

      {challenges.map((topic) => (
        <div key={topic.id} className="topicContainer">
          <div className="topicHeaders">
            <div 
              className="mainTopic"
              onClick={() => openModal(topic)}
            >
              {topic.name}
            </div>
            <Challenges challenges={topic.challengesHit} solvedFlags={flag} updateSolvedFlags={updateSolvedFlags} />
          </div>
        </div>
      ))}

      {/* Modal for displaying description */}
      {isModalOpen && selectedTopic && (
        <div className="modal">
          <div className="modalContent">
            <h2>{selectedTopic.name}</h2>
            <p>{selectedTopic.description}</p>
            <button onClick={closeModal}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Topics;
