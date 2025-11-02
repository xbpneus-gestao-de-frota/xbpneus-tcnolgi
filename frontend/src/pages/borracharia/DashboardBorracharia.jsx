import { useState, useEffect } from "react";
import { getUserData } from "../../api/auth";

export default function DashboardBorracharia() {
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    const data = getUserData();
    setUserData(data);
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">
          Dashboard da Borracharia
        </h1>
        
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Bem-vindo, {userData?.username}!</h2>
          <p className="text-gray-600">
            Área exclusiva para borracharias. Gerencie serviços, clientes e estoque.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-2">Serviços</h3>
            <p className="text-gray-600">Gerenciar serviços prestados</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-2">Clientes</h3>
            <p className="text-gray-600">Gerenciar clientes</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-2">Estoque</h3>
            <p className="text-gray-600">Controle de estoque</p>
          </div>
        </div>
      </div>
    </div>
  );
}

