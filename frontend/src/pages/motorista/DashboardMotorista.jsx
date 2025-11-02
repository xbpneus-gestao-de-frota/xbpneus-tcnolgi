import { useState, useEffect } from "react";
import { getUserData } from "../../api/auth";

export default function DashboardMotorista() {
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    const data = getUserData();
    setUserData(data);
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">
          Dashboard do Motorista
        </h1>
        
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Bem-vindo, {userData?.username}!</h2>
          <p className="text-gray-600">
            Área exclusiva para motoristas. Aqui você pode acompanhar seu veículo, viagens e manutenções.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-2">Meu Veículo</h3>
            <p className="text-gray-600">Informações do caminhão atribuído</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-2">Minhas Viagens</h3>
            <p className="text-gray-600">Histórico de viagens realizadas</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-2">Manutenções</h3>
            <p className="text-gray-600">Manutenções agendadas e realizadas</p>
          </div>
        </div>
      </div>
    </div>
  );
}

