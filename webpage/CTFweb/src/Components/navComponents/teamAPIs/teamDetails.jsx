import React, { useState, useEffect } from "react";
import LeaderApproval from "./leaderApproval";
import HandleRemoval from "./handleRemove";
import icon from '../../../assets/icon.jpg'
import './team.css';

const apiUrl = import.meta.env.VITE_API_URL;

function TeamDetails({ teamName }) {
    const [teamData, setTeamData] = useState(null);
    const [error, setError] = useState(null);
    const [showPopup, setShowPopup] = useState(false);
    const [popupContent, setPopupContent] = useState('');
    const curentUser = sessionStorage.getItem('username');

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`${apiUrl}users/fetchTeamDetails/?teamName=${teamName}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    setTeamData(data);
                } else {
                    setError('Failed to fetch team detail. Please try again later.');
                }
            } catch (error) {
                console.error('Error fetching team data:', error);
                setError('There was an error fetching the team.');
            }
        };

        fetchData();
    }, [teamName]);

    const handleRequestUpdate = (username, status) => {
        setTeamData((prevData) => {
            const updatedRequests = Array.isArray(prevData.request)
                ? prevData.request.filter((request) => request.username !== username)
                : [];

            return { ...prevData, request: updatedRequests };
        });
    };

    const handlePopup = (type) => {
        let content = '';

        if (type === 'request') {
            let requests = teamData.request;

            if (typeof requests === 'string') {
                try {
                    requests = requests.replace(/'/g, '"');
                    requests = JSON.parse(requests);
                } catch (error) {
                    console.error('Error parsing requests:', error);
                    requests = [];
                }
            }

            if (requests.length > 0) {
                content = requests.map((request, index) => (
                    <div key={index} className="request-item">
                        <p><strong>Username:</strong> {request.username}</p>
                        <p><strong>Points:</strong> {request.points}</p>
                        <p><strong>Status:</strong> {request.status}</p>
                        <LeaderApproval
                            username={request.username}
                            userTeam={teamName}
                            teamLeader={teamData.leaderName}
                            onRequestUpdate={handleRequestUpdate}
                            currentUser={curentUser}
                            className='leaderAprroval-buttons'
                        />
                    </div>
                ));
            } else {
                content = <p>No requests available.</p>;
            }
        } else if (type === 'members') {
            let members = teamData.members;

            if (typeof members === 'string') {
                try {
                    members = members.replace(/'/g, '"');
                    members = JSON.parse(members);
                } catch (error) {
                    console.error('Error parsing members:', error);
                    members = [];
                }
            }

            if (members.length > 0) {
                content = members.map((member, index) => (
                    <div key={index} className="request-item">
                        <p><strong>Username:</strong> {member.username}</p>
                        <p><strong>Points:</strong> {member.points}</p>
                        <HandleRemoval
                            username={member.username}
                            points={member.points}
                            teamLeader={curentUser}
                            onRemovalSuccess={closePopup}  // Pass the closePopup function to HandleRemoval
                        />
                    </div>
                ));
            } else {
                content = <p>No members available.</p>;
            }
        } else if (type === 'Chat'){
            content = () => (
                <div className="teamChat">
                    <div className="chatBox"></div>
                    <div className="typeBox">
                        <div className="typeBox-content">
                            <form>
                                <input type="text" />
                            </form>
                        </div>
                        <div className="typeBox-icon">
                            <img src={icon} alt="error" />
                        </div>
                    </div>
                </div>
            )
        }

        setPopupContent(content);
        setShowPopup(true);
    };

    const closePopup = () => {
        setShowPopup(false);
        setPopupContent('');
    };

    if (error) {
        return <p>{error}</p>;
    }

    if (!teamData) {
        return <p>Loading...</p>;
    }

    return (
        <div className="teamDetails">
            <div className="subteamDetails">
                <p>Team Leader: {teamData.leaderName}</p>
            </div>
            <div className="subteamDetails">
                <p>Team Points: {teamData.points}</p>
            </div>
            <div className="subteamDetails">
                <p>
                    {teamData.members ? (
                        <button onClick={() => handlePopup('members')} className="viewRequestButton">
                            View Members
                        </button>
                    ) : (
                        'No members'
                    )}
                </p>
            </div>
            <div className="subteamDetails">
                <p>
                    {teamData.request ? (
                        <button onClick={() => handlePopup('request')} className="viewRequestButton">
                            View Request
                        </button>
                    ) : (
                        'No request'
                    )}
                </p>
            </div>
            <div className="subteamDetails">
                <p>
                    <button onClick={() => handlePopup('Chat')} className="viewRequestButton">
                        Chat
                    </button>
                </p>
            </div>

            {showPopup && (
                <div className="popup-teamDetails">
                    <div className="popup-content-teamdetails">
                        <div className="fetched-team-users">
                            <button onClick={closePopup}>&#215;</button>
                            {popupContent}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default TeamDetails;
