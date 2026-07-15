import React from 'react';
import { Link } from 'react-router-dom';
import { FiMenu, FiHome, FiTarget, FiTrendingUp, FiUsers } from 'react-icons/fi';

function Navbar() {
  const [isOpen, setIsOpen] = React.useState(false);

  return (
    <nav className="bg-gray-800 border-b border-gray-700 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <div className="text-orange-500 text-2xl font-bold">🏏</div>
              <span className="text-xl font-bold text-white">IPL Predictor</span>
            </Link>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-1">
            <NavLink to="/" label="Dashboard" icon={<FiHome />} />
            <NavLink to="/match-predictor" label="Predictor" icon={<FiTarget />} />
            <NavLink to="/score-simulator" label="Score" icon={<FiTrendingUp />} />
            <NavLink to="/players" label="Players" icon={<FiUsers />} />
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700"
            >
              <FiMenu className="h-6 w-6" />
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden bg-gray-800 border-t border-gray-700">
          <div className="px-2 pt-2 pb-3 space-y-1">
            <MobileNavLink to="/" label="Dashboard" onClick={() => setIsOpen(false)} />
            <MobileNavLink to="/match-predictor" label="Match Predictor" onClick={() => setIsOpen(false)} />
            <MobileNavLink to="/score-simulator" label="Score Simulator" onClick={() => setIsOpen(false)} />
            <MobileNavLink to="/players" label="Players" onClick={() => setIsOpen(false)} />
          </div>
        </div>
      )}
    </nav>
  );
}

function NavLink({ to, label, icon }) {
  return (
    <Link
      to={to}
      className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium flex items-center space-x-1 transition"
    >
      {icon}
      <span>{label}</span>
    </Link>
  );
}

function MobileNavLink({ to, label, onClick }) {
  return (
    <Link
      to={to}
      className="text-gray-300 hover:bg-gray-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium"
      onClick={onClick}
    >
      {label}
    </Link>
  );
}

export default Navbar;
