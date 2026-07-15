import React from 'react';

interface ToastProps {
  message: string;
  type?: 'success' | 'error' | 'info';
  duration?: number;
  onClose: () => void;
}

const Toast: React.FC<ToastProps> = ({ message, type = 'info', duration = 3000, onClose }) => {
  React.useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  const toastStyles = {
    base: 'fixed bottom-5 right-5 p-4 rounded shadow-lg transition-opacity duration-300',
    success: 'bg-green-500 text-white',
    error: 'bg-red-500 text-white',
    info: 'bg-blue-500 text-white',
  };

  return (
    <div className={`${toastStyles.base} ${toastStyles[type]} opacity-100`}>
      {message}
      <button onClick={onClose} className="ml-4 text-white">
        &times;
      </button>
    </div>
  );
};

export default Toast;