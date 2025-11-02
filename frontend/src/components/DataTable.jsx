import { Link } from "react-router-dom";

export default function DataTable({ columns = [], rows = [] }) {
  function renderCell(col, row) {
    if (col.linkTo) {
      const href = col.linkTo.replace(":id", row.id);
      const label = col.linkLabel ? col.linkLabel(row) : "Ver";
      return (
        <Link 
          className="text-blue-600 hover:text-blue-800 underline font-medium" 
          to={href}
        >
          {label}
        </Link>
      );
    }
    let v = typeof col.render === "function" ? col.render(row) : row[col.key];
    if (typeof v === "boolean") v = v ? "✓" : "—";
    return v;
  }
  
  return (
    <div className="overflow-x-auto rounded-xl border border-gray-200 shadow-md bg-white">
      <table className="min-w-full text-sm">
        {/* Header com degradê azul-roxo */}
        <thead 
          className="text-white font-semibold"
          style={{
            background: 'linear-gradient(to right, #60a5fa, #6366f1, #7c3aed)'
          }}
        >
          <tr>
            {columns.map((c) => (
              <th 
                key={c.key || c.label} 
                className="text-left px-4 py-3"
              >
                {c.label}
              </th>
            ))}
          </tr>
        </thead>
        
        {/* Corpo da tabela */}
        <tbody>
          {rows.map((r, i) => (
            <tr 
              key={r.id || i} 
              className={`
                border-t border-gray-200 
                hover:bg-blue-50 
                transition-colors duration-150
                ${i % 2 === 0 ? 'bg-white' : 'bg-gray-50'}
              `}
            >
              {columns.map((c) => (
                <td 
                  key={c.key || c.label} 
                  className="px-4 py-3 text-gray-800"
                >
                  {renderCell(c, r)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      
      {/* Mensagem quando não há dados */}
      {rows.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          Nenhum registro encontrado
        </div>
      )}
    </div>
  );
}
