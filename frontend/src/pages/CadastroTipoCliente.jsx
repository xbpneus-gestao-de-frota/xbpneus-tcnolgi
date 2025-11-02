import { useState } from "react";
import { Link } from "react-router-dom";
export default function CadastroTipoCliente(){
  const [tipo, setTipo] = useState("transportador");
  const tipos = ["transportador","oficina","revenda","recapadora","motorista"];
  return (
    <div className="min-h-screen bg-[#0b1220] text-[#e5e7eb] flex items-center justify-center p-6">
      <div className="w-full max-w-xl rounded-2xl border border-white/10 bg-white/5 p-6">
        <h1 className="text-2xl font-extrabold bg-clip-text text-transparent" style={{ backgroundImage: "var(--xbp-grad)" }}>Tipo de cliente</h1>
        <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-3">
          {tipos.map(t => (
            <label key={t} className="flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 p-3 cursor-pointer">
              <input type="radio" name="tipo" checked={tipo===t} onChange={()=>setTipo(t)} />
              <span className="capitalize">{t}</span>
            </label>
          ))}
        </div>
        <div className="mt-4 flex items-center gap-3">
          <button className="rounded-xl border border-white/10 bg-white/10 px-4 py-2 hover:bg-white/20">Continuar</button>
          <Link to="/cadastro" className="text-sm opacity-80 hover:opacity-100">Voltar</Link>
        </div>
      </div>
    </div>
  );}
