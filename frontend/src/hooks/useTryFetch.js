import { useEffect, useState } from "react";
import api from "../api/http";
export default function useTryFetch(
  candidates = [],
  { mock = null, params = {}, enabled = true, paginated = false, initialPage = 1, pageSize: initialPageSize = 20 } = {}
) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(!!enabled);
  const [used, setUsed] = useState(null);
  const [simulated, setSimulated] = useState(false);
  const [page, setPage] = useState(initialPage);
  const [pageSize, setPageSizeState] = useState(initialPageSize);
  const [meta, setMeta] = useState({ next: null, previous: null, count: null, page: initialPage, pageSize: initialPageSize });
  useEffect(() => {
    let cancelled = false;
    async function run() {
      if (!enabled) return;
      setLoading(true); setError(null); setSimulated(false);
      for (const url of candidates) {
        try {
          const resp = await api.get(url, { params: { ...params, page, page_size: pageSize } });
          if (resp && resp.status >= 200 && resp.status < 300) {
            if (!cancelled) {
              const d = resp.data;
              if (paginated && d && Array.isArray(d.results)) {
                setData(d.results);
                setMeta({ next: d.next || null, previous: d.previous || null, count: d.count ?? null, page, pageSize });
              } else {
                setData(d?.results || d);
                setMeta({ next: null, previous: null, count: Array.isArray(d) ? d.length : null, page, pageSize });
              }
              setUsed(url);
              setLoading(false);
            }
            return;
          }
        } catch (e) {
          if (e?.response?.status === 401) { if (!cancelled) { setError(e); setLoading(false); } return; }
        }
      }
      if (mock) {
        if (!cancelled) {
          const m = typeof mock === "function" ? mock() : mock;
          setData(m);
          setSimulated(true);
          setMeta({ next: null, previous: null, count: Array.isArray(m) ? m.length : null, page, pageSize });
          setLoading(false);
        }
      } else {
        if (!cancelled) { setError(new Error("Todos endpoints falharam")); setLoading(false); }
      }
    }
    run();
    return () => { cancelled = true; };
  }, [JSON.stringify(candidates), JSON.stringify(params), enabled, page, paginated, pageSize]);
  return {
    data,
    error,
    loading,
    usedEndpoint: used,
    simulated,
    meta,
    page,
    setPage,
    pageSize,
    setPageSize: (n) => {
      setPageSizeState(n);
      setMeta((prev) => ({ ...prev, pageSize: n }));
    }
  };
}
