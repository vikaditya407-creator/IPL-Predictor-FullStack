import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import MatchPredictor from './pages/MatchPredictor';
import ScoreSimulator from './pages/ScoreSimulator';
import Players from './pages/Players';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-900 text-black">
        <Navbar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/match-predictor" element={<MatchPredictor />} />
          <Route path="/score-simulator" element={<ScoreSimulator />} />
          <Route path="/players" element={<Players />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
