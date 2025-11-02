import Sidebar from "../components/Sidebar";
import { Outlet } from "react-router-dom";

export default function TransportadorLayout() {
  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar com largura fixa */}
      <Sidebar />
      
      {/* Área principal de conteúdo */}
      <main className="flex-1 min-h-screen">
        <Outlet />
      </main>
    </div>
  );
}
