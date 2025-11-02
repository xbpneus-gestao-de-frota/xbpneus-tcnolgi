import { Outlet } from 'react-router-dom';
import Header from './Header';
import ManutencaoSidebar from './ManutencaoSidebar';

export default function LayoutManutencaoDashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0b1220] via-[#1a1f3a] to-[#0b1220]">
      <Header />
      <ManutencaoSidebar />
      <main className="ml-64 pt-20 p-8">
        <Outlet />
      </main>
    </div>
  );
}

