import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

const rootApi = axios.create({
  baseURL: API_BASE_URL.replace(/\/api\/?$/, ''),
  timeout: 30000,
});

// Add request interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const predictionAPI = {
  // Match Winner Prediction
  predictWinner: (matchData) =>
    api.post('/predictions/match-winner', matchData),

  // Score Prediction
  predictScore: (scoreData) =>
    api.post('/predictions/score', scoreData),

  // Player Stats Prediction
  predictPlayerStats: (playerData) =>
    api.post('/predictions/player-stats', playerData),

  // Viewership Estimation
  estimateViewership: (eventData) =>
    api.post('/predictions/viewership', eventData),

  // Get all matches
  getMatches: () => api.get('/matches'),

  // Get match details
  getMatchDetails: (matchId) =>
    api.get(`/matches/${matchId}`),

  // Get player details
  getPlayer: (playerId) =>
    api.get(`/players/${playerId}`),

  // Get all players
  getPlayers: () => api.get('/players'),

  // Tomorrow match prediction
  predictTomorrowMatch: (matchData) =>
    rootApi.post('/predict_match', matchData),
};

export default api;
