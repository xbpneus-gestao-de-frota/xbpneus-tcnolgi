import { Link } from "react-router-dom";

export default function PosCadastro() {
  return (
    <div
      className="flex items-center justify-center min-h-screen"
      style={{
        backgroundImage: "url(/static/pos_cadastro.png)",
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
      }}
    >
      <div
        className="bg-[#0f172a] p-7 rounded-2xl shadow-2xl w-full max-w-xl text-center"
        style={{
          boxShadow: "0 10px 25px rgba(0,0,0,0.25)",
        }}
      >
        <h1 className="text-3xl font-bold text-[#cfe3ff] mb-3">
          Cadastro enviado!
        </h1>
        <p className="text-lg text-[#cfe3ff] leading-relaxed">
          Seus dados estão em análise. Em breve você fará parte do{" "}
          <strong>Mundo XBPNEUS</strong>.
        </p>
        <Link
          to="/login"
          className="inline-block mt-4 text-[#93c5fd] border border-[#334155] px-4 py-2 rounded-lg hover:bg-[#334155] transition"
        >
          Voltar ao login
        </Link>
      </div>
    </div>
  );
}
