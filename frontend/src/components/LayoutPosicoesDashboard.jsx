import { Outlet } from 'react-router-dom';
import Header from './Header';
import PosicoesSidebar from './PosicoesSidebar';

export default function LayoutPosicoesDashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0b1220] via-[#1a1f3a] to-[#0b1220]">
      <Header />
      <PosicoesSidebar />
      <main className="ml-64 pt-20 p-8">
        <Outlet />
      </main>
    </div>
  );
}

