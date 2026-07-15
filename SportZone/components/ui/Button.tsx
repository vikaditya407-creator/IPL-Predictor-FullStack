import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline';
  loading?: boolean;
}

const Button: React.FC<ButtonProps> = ({ variant = 'primary', loading = false, children, ...props }) => {
  const baseStyles = 'px-4 py-2 rounded focus:outline-none transition duration-200';
  const variantStyles = {
    primary: 'bg-[#D85A30] text-white hover:bg-[#c74a25]',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
    outline: 'border border-[#D85A30] text-[#D85A30] hover:bg-[#D85A30] hover:text-white',
  };

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]}`}
      disabled={loading}
      {...props}
    >
      {loading ? 'Loading...' : children}
    </button>
  );
};

export default Button;