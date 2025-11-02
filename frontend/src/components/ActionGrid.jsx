import { Link } from "react-router-dom";
export default function ActionGrid({ actions = [] }){
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {actions.map((a, i)=> (
        <Link key={i} to={a.to || "#"} className="rounded-xl border border-white/10 bg-white/5 p-4 hover:bg-white/10">
          <div className="text-lg font-semibold text-gray-800">{a.label}</div>
          {a.desc && <div className="text-sm text-gray-600">{a.desc}</div>}
          {a.disabled && <div className="text-xs opacity-50 mt-1">Em breve</div>}
        </Link>
      ))}
    </div>
  );
}
