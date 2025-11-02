import { useEffect, useState } from "react";
export default function ColumnPicker({ columns = [], storageKey = "cols", value, onChange }){
  const labels = columns.map(c => c.label);
  const [open, setOpen] = useState(false);
  const [sel, setSel] = useState(value || labels);
  useEffect(()=>{ setSel(value || labels); }, [JSON.stringify(value), columns.length]);
  function toggle(lbl){
    const next = sel.includes(lbl) ? sel.filter(x=>x!==lbl) : [...sel, lbl];
    setSel(next); onChange && onChange(next);
    try { localStorage.setItem(storageKey, JSON.stringify(next)); } catch {}
  }
  return (
    <div className="relative">
      <button onClick={()=>setOpen(o=>!o)} className="px-3 py-2 rounded-lg border border-white/10 bg-white/10">Colunas</button>
      {open && (
        <div className="absolute z-10 mt-2 p-3 rounded-xl border border-white/10 bg-black/60 backdrop-blur min-w-[220px]">
          {labels.map(lbl => (
            <label key={lbl} className="flex items-center gap-2 py-1 text-sm">
              <input type="checkbox" checked={sel.includes(lbl)} onChange={()=>toggle(lbl)} />
              <span>{lbl}</span>
            </label>
          ))}
        </div>
      )}
    </div>
  );
}
