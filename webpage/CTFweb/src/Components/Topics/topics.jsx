import React, { useState, useEffect } from 'react';
import Challenges from './challenges.jsx';
import './topics.css';

function Topics() {
  const [challenges, setChallenges] = useState([]);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false); 
  const [selectedTopic, setSelectedTopic] = useState(null);

  useEffect(() => {
    const fetchChallenges = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/challenges/challengesData/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const challengesData = await response.json();
          setChallenges(challengesData);
        } else {
          setError('Failed to fetch challenges!');
        }
      } catch (error) {
        console.error('Error fetching challenges:', error);
        setError('There was an error fetching the challenges.');
      }
    };

    fetchChallenges();
  }, []);

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

  return (
    <div className="topics">
      {challenges.map((topic) => (
        <div key={topic.id} className="topicContainer">
          {/* Topic */}
          <div className="topicHeaders">
            <div 
              className="mainTopic"
              onClick={() => openModal(topic)}
            >
              {topic.name}
            </div>
            <Challenges challenges={topic.challengesHit} />
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
