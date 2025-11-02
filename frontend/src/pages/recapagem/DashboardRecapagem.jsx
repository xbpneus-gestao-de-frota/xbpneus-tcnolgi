import { useState, useEffect } from "react";
import { getUserData } from "../../api/auth";

export default function DashboardRecapagem() {
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    const data = getUserData();
    setUserData(data);
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">
          Dashboard da Recapagem
        </h1>
        
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Bem-vindo, {userData?.username}!</h2>
          <p className="text-gray-600">
            Área exclusiva para recapagem. Gerencie processos de recapagem, pneus e clientes.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-2">Pneus</h3>
            <p className="text-gray-600">Pneus aguardando recapagem</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-2">Processos</h3>
            <p className="text-gray-600">Processos de recapagem em andamento</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-2">Clientes</h3>
            <p className="text-gray-600">Gerenciar clientes</p>
          </div>
        </div>
      </div>
    </div>
  );
}

