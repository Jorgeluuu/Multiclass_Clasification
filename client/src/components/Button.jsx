import React from 'react';

const Button = ({ 
  children, 
  variant = 'primary', 
  type = 'button',
  onClick,
  className = ''
}) => {
  // Estilos base compartidos
  const baseStyles = "px-6 py-3 font-semibold text-base transition-colors duration-200 focus:outline-none";
  
  // Estilos específicos para cada variante
  const variantStyles = {
    primary: "bg-red-600 text-white hover:bg-red-700 active:bg-red-800",
    secondary: "border-2 border-gray-800 text-gray-800 bg-white hover:bg-gray-50 active:bg-gray-100"
  };

  return (
    <button
      type={type}
      onClick={onClick}
      className={`${baseStyles} ${variantStyles[variant]} ${className}`}
    >
      {children}
    </button>
  );
};

export default Button;