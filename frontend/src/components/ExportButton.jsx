export default function ExportButton({ columns = [], rows = [], filename = "export.csv" }){
  function toCSV(){
    const headers = columns.map(c => c.label);
    const keys = columns.map(c => c.key);
    const lines = [headers.join(",")];
    (rows || []).forEach(r => {
      const vals = keys.map(k => {
        let v = r[k];
        if (typeof v === "boolean") v = v ? "1" : "0";
        if (v === null || v === undefined) v = "";
        v = String(v).replaceAll('"','""');
        if (v.includes(",") || v.includes('"') || v.includes("\n")) v = `"${v}"`;
        return v;
      });
      lines.push(vals.join(","));
    });
    const blob = new Blob([lines.join("\n")], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = filename; a.click();
    URL.revokeObjectURL(url);
  }
  return <button onClick={toCSV} className="px-3 py-2 rounded-lg border border-white/10 bg-white/10">Exportar CSV</button>;
}
