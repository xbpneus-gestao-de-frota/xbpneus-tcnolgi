export default function ServerExportButtons({ usedEndpoint, params = {}, filenameBase = "export" }){
  function buildURL(fmt){
    if (!usedEndpoint) return null;
    const url = new URL(usedEndpoint, window.location.origin);
    const q = new URLSearchParams(params || {});
    q.set("format", fmt);
    url.search = q.toString();
    // If usedEndpoint is relative, prepend API base from VITE_API_BASE
    const base = import.meta.env.VITE_API_BASE || "http://localhost:8000";
    return base.replace(/\/$/, "") + url.pathname + "?" + url.searchParams.toString();
  }
  return (
    <div className="flex gap-2">
      <button onClick={()=>{ const u = buildURL("csv"); if(u) window.open(u, "_blank"); }} className="px-3 py-2 rounded-lg border border-white/10 bg-white/10">CSV (server)</button>
      <button onClick={()=>{ const u = buildURL("xlsx"); if(u) window.open(u, "_blank"); }} className="px-3 py-2 rounded-lg border border-white/10 bg-white/10">XLSX (server)</button>
    </div>
  );
}
