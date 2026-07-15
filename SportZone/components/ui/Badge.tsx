import React from 'react';

interface BadgeProps {
  text: string;
  color?: 'success' | 'error' | 'warning' | 'info';
}

const Badge: React.FC<BadgeProps> = ({ text, color = 'info' }) => {
  const colorClasses = {
    success: 'bg-green-500 text-white',
    error: 'bg-red-500 text-white',
    warning: 'bg-yellow-500 text-black',
    info: 'bg-blue-500 text-white',
  };

  return (
    <span className={`inline-flex items-center px-2 py-1 text-xs font-bold rounded-full ${colorClasses[color]}`}>
      {text}
    </span>
  );
};

export default Badge;