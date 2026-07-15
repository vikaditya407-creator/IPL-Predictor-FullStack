import React, { useState } from 'react';
import { FiTrendingUp, FiTrendingDown } from 'react-icons/fi';

function MatchPredictor() {
  const [selectedMatch, setSelectedMatch] = useState('mi-vs-csk');
  const [prediction, setPrediction] = useState(null);

  const matches = [
    { id: 'mi-vs-csk', teams: 'Mumbai Indians vs Chennai Super Kings', date: '2024-04-20' },
    { id: 'rcb-vs-kkr', teams: 'Royal Challengers Bangalore vs Kolkata Knight Riders', date: '2024-04-21' },
    { id: 'dc-vs-srh', teams: 'Delhi Capitals vs Sunrisers Hyderabad', date: '2024-04-22' },
  ];

  const mockPredictions = {
    'mi-vs-csk': {
      team1: { name: 'Mumbai Indians', probability: 62, logo: '🏆' },
      team2: { name: 'Chennai Super Kings', probability: 38, logo: '🐯' },
      winner: 'Mumbai Indians',
      confidence: 'High',
      factors: ['Home advantage', 'Better recent form', 'Strong bowling attack']
    },
    'rcb-vs-kkr': {
      team1: { name: 'Royal Challengers Bangalore', probability: 55, logo: '🦁' },
      team2: { name: 'Kolkata Knight Riders', probability: 45, logo: '🐱' },
      winner: 'Royal Challengers Bangalore',
      confidence: 'Medium',
      factors: ['Strong batting lineup', 'Captain\'s experience', 'Venue familiarity']
    },
    'dc-vs-srh': {
      team1: { name: 'Delhi Capitals', probability: 48, logo: '🦅' },
      team2: { name: 'Sunrisers Hyderabad', probability: 52, logo: '🌞' },
      winner: 'Sunrisers Hyderabad',
      confidence: 'Low',
      factors: ['Pitch conditions', 'Weather forecast', 'Player availability']
    }
  };

  const handlePredict = () => {
    setPrediction(mockPredictions[selectedMatch]);
  };

  return (
    <div className="container">
      <div className="mb-8">
        <h1 className="text-4xl font-extrabold text-white tracking-normal">
          Match Winner Predictor
        </h1>
        <div className="mt-2 h-1 w-24 rounded-full bg-orange-500" />
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Match Selection */}
        <div className="card">
          <h2 className="text-xl font-semibold text-black mb-4">Select Match</h2>
          <div className="space-y-3">
            {matches.map((match) => (
              <div
                key={match.id}
                className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                  selectedMatch === match.id
                    ? 'border-blue-500 bg-blue-500 bg-opacity-10'
                    : 'border-gray-600 hover:border-gray-500'
                }`}
                onClick={() => setSelectedMatch(match.id)}
              >
                <div className="flex justify-between items-center">
                  <span className="text-black font-medium">{match.teams}</span>
                  <span className="text-black text-sm">{match.date}</span>
                </div>
              </div>
            ))}
          </div>
          <button
            onClick={handlePredict}
            className="w-full mt-4 bg-blue-600 hover:bg-blue-700 text-black font-semibold py-2 px-4 rounded-lg transition-colors"
          >
            Predict Winner
          </button>
        </div>

        {/* Prediction Results */}
        <div className="card">
          <h2 className="text-xl font-semibold text-black mb-4">Prediction Results</h2>
          {prediction ? (
            <div className="space-y-4">
              <div className="text-center">
                <h3 className="text-lg text-black mb-2">{matches.find(m => m.id === selectedMatch)?.teams}</h3>
                <p className="text-sm text-black">Prediction Confidence: <span className="text-black">{prediction.confidence}</span></p>
              </div>

              <div className="grid grid-cols-1 gap-4">
                <div className={`p-4 rounded-lg border ${
                  prediction.winner === prediction.team1.name
                    ? 'border-green-500 bg-green-500 bg-opacity-10'
                    : 'border-gray-600'
                }`}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <span className="text-2xl">{prediction.team1.logo}</span>
                      <div>
                        <h4 className="text-black font-semibold">{prediction.team1.name}</h4>
                        <p className="text-2xl font-bold text-black">{prediction.team1.probability}%</p>
                      </div>
                    </div>
                    {prediction.winner === prediction.team1.name && (
                      <FiTrendingUp className="w-6 h-6 text-black" />
                    )}
                  </div>
                </div>

                <div className={`p-4 rounded-lg border ${
                  prediction.winner === prediction.team2.name
                    ? 'border-green-500 bg-green-500 bg-opacity-10'
                    : 'border-gray-600'
                }`}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <span className="text-2xl">{prediction.team2.logo}</span>
                      <div>
                        <h4 className="text-black font-semibold">{prediction.team2.name}</h4>
                        <p className="text-2xl font-bold text-black">{prediction.team2.probability}%</p>
                      </div>
                    </div>
                    {prediction.winner === prediction.team2.name && (
                      <FiTrendingUp className="w-6 h-6 text-black" />
                    )}
                  </div>
                </div>
              </div>

              <div className="mt-4 p-3 bg-gray-700 rounded-lg">
                <h4 className="text-black font-semibold mb-2">Key Factors:</h4>
                <ul className="text-black text-sm space-y-1">
                  {prediction.factors.map((factor, index) => (
                    <li key={index}>• {factor}</li>
                  ))}
                </ul>
              </div>

              <div className="text-center">
                <p className="text-lg text-black">
                  Predicted Winner: <span className="text-black font-bold">{prediction.winner}</span>
                </p>
              </div>
            </div>
          ) : (
            <div className="text-center text-black py-8">
              <p>Select a match and click "Predict Winner" to see results</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default MatchPredictor;
