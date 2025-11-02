import { useNavigate } from 'react-router-dom';

export default function Header() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  const empresa = user.transportador?.empresa || {};
  
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };
  
  return (
    <div className="bg-white shadow-sm px-6 py-4 flex justify-between items-center mb-6">
      <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
        Painel do Transportador
      </h1>
      
      <div className="flex items-center gap-4">
        <div className="text-right">
          <p className="text-sm font-medium text-gray-900">{user.nome || user.email}</p>
          <p className="text-xs text-gray-500">{empresa.nome || 'Empresa'}</p>
        </div>
        
        <button
          onClick={handleLogout}
          className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
        >
          Sair
        </button>
      </div>
    </div>
  );
}
