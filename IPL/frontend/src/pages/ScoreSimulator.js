import React, { useState } from 'react';
import { FiTrendingUp, FiTarget, FiZap } from 'react-icons/fi';

function ScoreSimulator() {
  const [currentState, setCurrentState] = useState({
    current_runs: 120,
    current_wickets: 2,
    overs_completed: 12.4,
    runs_last_6_balls: 45,
    target: null
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (field, value) => {
    setCurrentState(prev => ({
      ...prev,
      [field]: parseFloat(value) || 0
    }));
  };

  const simulateScore = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/score', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(currentState),
      });

      if (!response.ok) {
        const errorData = await response.text();
        throw new Error(`API Error: ${response.status} - ${errorData}`);
      }

      const data = await response.json();
      setPrediction(data);
    } catch (err) {
      console.error('Score simulation error:', err);
      setError(`Failed to simulate score: ${err.message}. Please check if the backend is running.`);
    } finally {
      setLoading(false);
    }
  };

  const resetSimulator = () => {
    setCurrentState({
      current_runs: 120,
      current_wickets: 2,
      overs_completed: 12.4,
      runs_last_6_balls: 45,
      target: null
    });
    setPrediction(null);
    setError(null);
  };

  return (
    <div className="container">
      <div className="mb-8">
        <h1 className="text-4xl font-extrabold text-white tracking-normal">
          Score Simulator
        </h1>
        <div className="mt-2 h-1 w-24 rounded-full bg-orange-500" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <div className="card">
          <h2 className="text-xl font-semibold text-black mb-4">Current Match State</h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-black mb-1">
                Current Runs
              </label>
              <input
                type="number"
                value={currentState.current_runs}
                onChange={(e) => handleInputChange('current_runs', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-black"
                min="0"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-black mb-1">
                Wickets Lost
              </label>
              <input
                type="number"
                value={currentState.current_wickets}
                onChange={(e) => handleInputChange('current_wickets', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-black"
                min="0"
                max="10"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-black mb-1">
                Overs Completed
              </label>
              <input
                type="number"
                step="0.1"
                value={currentState.overs_completed}
                onChange={(e) => handleInputChange('overs_completed', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-black"
                min="0"
                max="20"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-black mb-1">
                Runs in Last 6 Balls
              </label>
              <input
                type="number"
                value={currentState.runs_last_6_balls}
                onChange={(e) => handleInputChange('runs_last_6_balls', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-black"
                min="0"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-black mb-1">
                Target (Optional)
              </label>
              <input
                type="number"
                value={currentState.target || ''}
                onChange={(e) => handleInputChange('target', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-black"
                min="0"
                placeholder="Leave empty if not chasing"
              />
            </div>
          </div>

          <div className="flex space-x-3 mt-6">
            <button
              onClick={simulateScore}
              disabled={loading}
              className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-black font-semibold py-2 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-black"></div>
                  <span>Simulating...</span>
                </>
              ) : (
                <>
                  <FiTarget className="w-4 h-4" />
                  <span>Simulate Score</span>
                </>
              )}
            </button>

            <button
              onClick={resetSimulator}
              className="px-4 py-2 border border-gray-300 text-black rounded-lg hover:bg-gray-50 transition-colors"
            >
              Reset
            </button>
          </div>
        </div>

        {/* Results */}
        <div className="card">
          <h2 className="text-xl font-semibold text-black mb-4">Prediction Results</h2>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          {prediction ? (
            <div className="space-y-4">
              {/* Main Prediction */}
              <div className="text-center p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border">
                <div className="flex items-center justify-center space-x-2 mb-2">
                  <FiTrendingUp className="w-6 h-6 text-blue-600" />
                  <span className="text-sm font-medium text-black">Predicted Final Score</span>
                </div>
                <div className="text-4xl font-bold text-black mb-1">{prediction.predicted_score}</div>
                <div className="text-sm text-black">
                  Confidence: {prediction.confidence_interval.lower} - {prediction.confidence_interval.upper} runs
                </div>
              </div>

              {/* Stats Grid */}
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-black">{prediction.predicted_wickets}</div>
                  <div className="text-sm text-black">Final Wickets</div>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-black">{prediction.projected_run_rate}</div>
                  <div className="text-sm text-black">Projected RPO</div>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-black">{prediction.current_run_rate}</div>
                  <div className="text-sm text-black">Current RPO</div>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-black">{prediction.remaining_overs}</div>
                  <div className="text-sm text-black">Remaining Overs</div>
                </div>
              </div>

              {/* Factors */}
              <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                <h4 className="text-black font-semibold mb-2 flex items-center">
                  <FiZap className="w-4 h-4 mr-2" />
                  Key Factors
                </h4>
                <ul className="text-sm text-black space-y-1">
                  {prediction.factors.map((factor, index) => (
                    <li key={index}>• {factor}</li>
                  ))}
                </ul>
              </div>

              {/* Model Info */}
              <div className="text-xs text-black text-center pt-2 border-t">
                Model: {prediction.model_used} | Updated: {new Date(prediction.timestamp).toLocaleString()}
              </div>
            </div>
          ) : (
            <div className="text-center text-black py-12">
              <FiTarget className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p>Enter match details and click "Simulate Score" to get predictions</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ScoreSimulator;
