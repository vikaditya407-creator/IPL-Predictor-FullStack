import React, { useEffect, useState } from 'react';
import { predictionAPI } from '../services/api';
import { FiTrendingUp, FiBarChart, FiUsers, FiCalendar } from 'react-icons/fi';

function Dashboard() {
  const [stats, setStats] = useState({
    totalMatches: 245,
    totalPlayers: 892,
    accuracyRate: 78.5,
    lastUpdate: new Date().toLocaleDateString(),
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [matchForm, setMatchForm] = useState({
    teamA: '',
    teamB: '',
    matchDate: '',
    stadium: '',
  });
  const [matchPrediction, setMatchPrediction] = useState(null);
  const [predictingMatch, setPredictingMatch] = useState(false);
  const [matchPredictionError, setMatchPredictionError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        setStats({
          totalMatches: 232,
          totalPlayers: 1200,
          accuracyRate: 87.5,
          lastUpdate: new Date().toLocaleDateString(),
        });
      } catch (err) {
        setError('Failed to fetch statistics');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const handleMatchFormChange = (field, value) => {
    setMatchForm((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleTomorrowMatchPredict = async (event) => {
    event.preventDefault();
    setPredictingMatch(true);
    setMatchPredictionError(null);
    setMatchPrediction(null);

    try {
      const response = await predictionAPI.predictTomorrowMatch(matchForm);
      setMatchPrediction(response.data);
    } catch (err) {
      setMatchPredictionError(
        err.response?.data?.detail || 'Failed to predict match result. Please check if the backend is running.'
      );
    } finally {
      setPredictingMatch(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gradient mb-2">IPL Prediction Dashboard</h1>
        <p className="text-lg font-medium text-white">Real-time predictions powered by machine learning</p>
      </div>

      {error && (
        <div className="bg-red-500 bg-opacity-20 border border-red-500 rounded-lg p-4 mb-8">
          <p className="text-black">{error}</p>
        </div>
      )}

      <div className="card mb-8">
        <h2 className="text-2xl font-extrabold text-orange-500 mb-4">
          Predict Tomorrow Match Result
        </h2>
        <form onSubmit={handleTomorrowMatchPredict} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-black mb-1">
                Team A name
              </label>
              <input
                type="text"
                value={matchForm.teamA}
                onChange={(event) => handleMatchFormChange('teamA', event.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md bg-white text-black focus:outline-none focus:ring-2 focus:ring-orange-500"
                placeholder="MI"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-black mb-1">
                Team B name
              </label>
              <input
                type="text"
                value={matchForm.teamB}
                onChange={(event) => handleMatchFormChange('teamB', event.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md bg-white text-black focus:outline-none focus:ring-2 focus:ring-orange-500"
                placeholder="CSK"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-black mb-1">
                Match date
              </label>
              <input
                type="date"
                value={matchForm.matchDate}
                onChange={(event) => handleMatchFormChange('matchDate', event.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md bg-white text-black focus:outline-none focus:ring-2 focus:ring-orange-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-black mb-1">
                Stadium name
              </label>
              <input
                type="text"
                value={matchForm.stadium}
                onChange={(event) => handleMatchFormChange('stadium', event.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md bg-white text-black focus:outline-none focus:ring-2 focus:ring-orange-500"
                placeholder="Wankhede Stadium"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={predictingMatch}
            className="bg-orange-500 hover:bg-orange-600 disabled:bg-orange-300 text-white font-bold py-2 px-5 rounded-lg transition-colors"
          >
            {predictingMatch ? 'Predicting...' : 'Predict'}
          </button>
        </form>

        {matchPredictionError && (
          <div className="mt-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {matchPredictionError}
          </div>
        )}

        {matchPrediction && (
          <div className="mt-6 border-t pt-5">
            <h3 className="text-xl font-bold text-black mb-3">Prediction Result</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-5">
              <div className="border border-blue-500 bg-blue-50 rounded-lg p-4">
                <p className="text-sm font-semibold text-gray-700">{matchForm.teamA}</p>
                <p className="text-3xl font-extrabold text-black">
                  {matchPrediction.prediction.teamA}%
                </p>
              </div>
              <div className="border border-red-500 bg-red-50 rounded-lg p-4">
                <p className="text-sm font-semibold text-gray-700">{matchForm.teamB}</p>
                <p className="text-3xl font-extrabold text-black">
                  {matchPrediction.prediction.teamB}%
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <FactorItem title="Team form" value={matchPrediction.factors.team_form} />
              <FactorItem title="Stadium history" value={matchPrediction.factors.stadium_history} />
              <FactorItem title="Toss impact" value={matchPrediction.factors.toss} />
              <FactorItem title="Pitch type" value={matchPrediction.factors.pitch_type} />
              <FactorItem title="Player form" value={matchPrediction.factors.player_form} />
            </div>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Matches"
          value={stats.totalMatches}
          icon={<FiBarChart className="w-8 h-8" />}
          color="blue"
        />
        <StatCard
          title="Players Tracked"
          value={stats.totalPlayers}
          icon={<FiUsers className="w-8 h-8" />}
          color="purple"
        />
        <StatCard
          title="Prediction Accuracy"
          value={`${stats.accuracyRate}%`}
          icon={<FiTrendingUp className="w-8 h-8" />}
          color="green"
        />
        <StatCard
          title="Last Updated"
          value={stats.lastUpdate}
          icon={<FiCalendar className="w-8 h-8" />}
          color="orange"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <FeatureCard
          title="Score Prediction"
          description="Estimate final scores based on current match state"
          link="/score-simulator"
        />
        <FeatureCard
          title="Player Performance"
          description="Predict individual player statistics and performance"
          link="/players"
        />
        <FeatureCard
          title="Viewership Analytics"
          description="Estimate potential audience reach and engagement"
          link="/"
        />
      </div>
    </div>
  );
}

function StatCard({ title, value, icon, color }) {
  const colorClasses = {
    blue: 'bg-blue-500 bg-opacity-10 border-blue-500',
    purple: 'bg-purple-500 bg-opacity-10 border-purple-500',
    green: 'bg-green-500 bg-opacity-10 border-green-500',
    orange: 'bg-orange-500 bg-opacity-10 border-orange-500',
  };

  return (
    <div className={`card border ${colorClasses[color]}`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-black text-sm font-medium">{title}</h3>
        <div className="text-black">{icon}</div>
      </div>
      <p className="text-3xl font-bold text-black">{value}</p>
    </div>
  );
}

function FeatureCard({ title, description, link }) {
  return (
    <div className="card group cursor-pointer hover:bg-opacity-80">
      <h3 className="text-lg font-semibold text-black mb-2">{title}</h3>
      <p className="text-black mb-4">{description}</p>
      <a href={link} className="text-black hover:text-black font-medium">
        Explore
      </a>
    </div>
  );
}

function FactorItem({ title, value }) {
  return (
    <div className="bg-gray-50 rounded-lg p-3 border border-gray-200">
      <p className="text-sm font-bold text-black mb-1">{title}</p>
      <p className="text-sm text-gray-700">{value}</p>
    </div>
  );
}

export default Dashboard;
