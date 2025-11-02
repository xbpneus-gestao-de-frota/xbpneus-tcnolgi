import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";
import Header from "./Header";

export default function LayoutTransportador(){
  return (
    <div className="min-h-screen bg-[#0b1220] text-[#e5e7eb] flex">
      <Sidebar />
      <main className="flex-1 flex flex-col">
        <Header />
        <div className="flex-1 p-6"><Outlet /></div>
      </main>
    </div>
  );
}
