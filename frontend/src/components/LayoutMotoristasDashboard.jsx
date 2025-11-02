import React from 'react';
import { Outlet } from 'react-router-dom';
import MotoristasSidebar from './MotoristasSidebar';

export default function LayoutMotoristasDashboard() {
  return (
    <div className="flex h-screen bg-gray-900 text-white">
      <MotoristasSidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-800 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

