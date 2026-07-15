import React, { useState, useEffect } from 'react';

function PageTitle() {
  return (
    <div className="mb-8">
      <h1 className="text-4xl font-extrabold text-white tracking-normal">
        Player Analytics
      </h1>
      <div className="mt-2 h-1 w-24 rounded-full bg-orange-500" />
    </div>
  );
}

function Players() {
  const [players, setPlayers] = useState([]);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [playerStats, setPlayerStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPlayers();
  }, []);

  const fetchPlayers = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/players/');
      if (!response.ok) {
        throw new Error('Failed to fetch players');
      }
      const data = await response.json();
      setPlayers(data);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const fetchPlayerStats = async (playerId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/players/${playerId}/stats`);
      if (!response.ok) {
        throw new Error('Failed to fetch player stats');
      }
      const data = await response.json();
      setPlayerStats(data);
    } catch (err) {
      setError(err.message);
    }
  };

  const handlePlayerSelect = (player) => {
    setSelectedPlayer(player);
    fetchPlayerStats(player.id);
  };

  if (loading) {
    return (
      <div className="container">
        <PageTitle />
        <div className="card">
          <p className="text-black">Loading players...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <PageTitle />
        <div className="card">
          <p className="text-red-600">Error: {error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <PageTitle />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Players List */}
        <div className="card">
          <h2 className="text-xl font-semibold mb-4 text-black">Select a Player</h2>
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {players.map((player) => (
              <div
                key={player.id}
                onClick={() => handlePlayerSelect(player)}
                className={`p-3 border rounded-lg cursor-pointer transition-colors ${
                  selectedPlayer?.id === player.id
                    ? 'bg-blue-100 border-blue-500'
                    : 'bg-white border-gray-300 hover:bg-gray-50'
                }`}
              >
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className="font-medium text-black">{player.name}</h3>
                    <p className="text-sm text-gray-600">{player.team} • {player.role}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-black">Age: {player.age}</p>
                    <p className="text-sm text-gray-600">{player.country}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Player Stats */}
        <div className="card">
          {selectedPlayer ? (
            <>
              <h2 className="text-xl font-semibold mb-4 text-black">
                {selectedPlayer.name} - Statistics
              </h2>

              {/* Current Season Stats */}
              <div className="mb-6">
                <h3 className="text-lg font-medium mb-3 text-black">Season {selectedPlayer.stats.season} Performance</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gray-50 p-3 rounded">
                    <p className="text-sm text-gray-600">Matches Played</p>
                    <p className="text-lg font-semibold text-black">{selectedPlayer.stats.matches_played}</p>
                  </div>
                  <div className="bg-gray-50 p-3 rounded">
                    <p className="text-sm text-gray-600">Runs Scored</p>
                    <p className="text-lg font-semibold text-black">{selectedPlayer.stats.runs_scored}</p>
                  </div>
                  <div className="bg-gray-50 p-3 rounded">
                    <p className="text-sm text-gray-600">Strike Rate</p>
                    <p className="text-lg font-semibold text-black">{selectedPlayer.stats.strike_rate}</p>
                  </div>
                  <div className="bg-gray-50 p-3 rounded">
                    <p className="text-sm text-gray-600">Average</p>
                    <p className="text-lg font-semibold text-black">{selectedPlayer.stats.average}</p>
                  </div>
                  {selectedPlayer.stats.wickets > 0 && (
                    <>
                      <div className="bg-gray-50 p-3 rounded">
                        <p className="text-sm text-gray-600">Wickets</p>
                        <p className="text-lg font-semibold text-black">{selectedPlayer.stats.wickets}</p>
                      </div>
                      <div className="bg-gray-50 p-3 rounded">
                        <p className="text-sm text-gray-600">Economy Rate</p>
                        <p className="text-lg font-semibold text-black">{selectedPlayer.stats.economy_rate}</p>
                      </div>
                    </>
                  )}
                </div>
              </div>

              {/* Predicted Performance */}
              {playerStats && (
                <div className="border-t pt-4">
                  <h3 className="text-lg font-medium mb-3 text-black">Predicted Performance</h3>
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <div className="grid grid-cols-2 gap-4 mb-3">
                      <div>
                        <p className="text-sm text-gray-600">Predicted Runs</p>
                        <p className="text-xl font-bold text-blue-600">{playerStats.predicted_runs}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Predicted Wickets</p>
                        <p className="text-xl font-bold text-blue-600">{playerStats.predicted_wickets}</p>
                      </div>
                    </div>
                    <div className="mb-3">
                      <p className="text-sm text-gray-600">Confidence Score</p>
                      <div className="flex items-center">
                        <div className="flex-1 bg-gray-200 rounded-full h-2 mr-2">
                          <div
                            className="bg-blue-600 h-2 rounded-full"
                            style={{ width: `${playerStats.confidence_score * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-sm font-medium text-black">
                          {Math.round(playerStats.confidence_score * 100)}%
                        </span>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600 italic">{playerStats.match_context}</p>
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="text-center py-8">
              <p className="text-gray-500">Select a player to view their analytics</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Players;
