import clsx from 'clsx';

export default function Button({ 
  children, 
  variant = 'primary', 
  size = 'md',
  className,
  disabled,
  ...props 
}) {
  const baseClasses = 'font-medium rounded-lg focus:outline-none focus:ring-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed';
  
  const variants = {
    // Botão primário com degradê azul-roxo (padrão XBPneus)
    primary: 'bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white hover:opacity-90 focus:ring-blue-500 shadow-lg',
    
    // Botão secundário com borda azul
    secondary: 'border-2 border-blue-500 text-blue-500 bg-transparent hover:bg-blue-50 focus:ring-blue-400',
    
    // Botão de sucesso (verde)
    success: 'bg-green-500 text-white hover:bg-green-600 focus:ring-green-400 shadow-md',
    
    // Botão de perigo (rosa/vermelho)
    danger: 'bg-gradient-to-r from-pink-500 to-red-500 text-white hover:opacity-90 focus:ring-red-400 shadow-md',
    
    // Botão de aviso (laranja)
    warning: 'bg-gradient-to-r from-yellow-400 to-orange-500 text-white hover:opacity-90 focus:ring-orange-400 shadow-md',
    
    // Botão neutro/ghost
    ghost: 'bg-transparent text-gray-700 hover:bg-gray-100 focus:ring-gray-300',
  };
  
  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };
  
  return (
    <button
      className={clsx(baseClasses, variants[variant], sizes[size], className)}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
}
