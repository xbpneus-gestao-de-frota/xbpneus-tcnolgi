import { Outlet } from 'react-router-dom';
import Header from './Header';
import RastreamentoSidebar from './RastreamentoSidebar';

export default function LayoutRastreamentoDashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0b1220] via-[#1a1f3a] to-[#0b1220]">
      <Header />
      <RastreamentoSidebar />
      <main className="ml-64 pt-20 p-8">
        <Outlet />
      </main>
    </div>
  );
}

