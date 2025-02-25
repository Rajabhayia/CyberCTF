import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom"; // Import navigate hook
import './Rules.css';
import FetchUsers from "./fetchAPIs/FetchUsers";
import CreateTeam from "./teamAPIs/createTeam";
import JoinTeam from "./teamAPIs/joinTeam";
import RevokeRequest from "./teamAPIs/revokeRequest";
import TeamDetails from "./teamAPIs/teamDetails";

const Team = () => {
    const [errors, setErrors] = useState('');
    const [userTeam, setUserTeam] = useState(null);
    const [joinRequestSent, setJoinRequestSent] = useState(false);
    const [teamNameRequested, setTeamNameRequested] = useState('');
    const [loading, setLoading] = useState(true); // State to track loading status
    const { userData, error } = FetchUsers();
    const [message, setMessage] = useState(null)
    const navigate = useNavigate(); // Initialize navigate hook

    useEffect(() => {
        if (userData) {
            setLoading(false); // Data fetched, stop loading
            if (userData?.team) {
                setUserTeam(userData.team);
            };
            if (userData?.message) {
                setMessage(userData.message);
            };
        }
    }, [userData]);

    useEffect(() => {
        if (error) {
            setLoading(false); // If there's an error, stop loading
            setErrors(error);
        }
    }, [error]);

    let content;

    if (loading) {
        content = (
            <div className="loading">
                <p>Loading...</p>
            </div>
        );
    } else if (message || joinRequestSent){
        content = (
            <div className="loadMessage">
                <RevokeRequest
                teamNameRequested={teamNameRequested}
                setJoinRequestSent={setJoinRequestSent}
                setErrors={setErrors}
                />
            </div>
        );
    } else if (userTeam) {
        content = (
            <div className="loadTeam">
                <div className="loadTeamHeader">
                    <p>Team: {userTeam}</p>
                </div>
                <div className="loadTeamDetails">
                    <TeamDetails teamName={userTeam}/>
                </div>
            </div>
        );
    } else {
        content = (
            <div className="createJoinClass">
                <div className="teamHeader">
                    <p>Create or Join Team</p>
                </div>
                <div className="teamContent">
                    <CreateTeam navigate={navigate} setErrors={setErrors} />
                    <JoinTeam
                        setJoinRequestSent={setJoinRequestSent}
                        setTeamNameRequested={setTeamNameRequested}
                        setErrors={setErrors}
                    />
                </div>
                <div className="createJoinError">
                        {errors && <div>{errors}</div>}
                </div>
            </div>
        );
    }

    return (
        <div className="team">
            {content}
        </div>
    );
};

export default Team;
