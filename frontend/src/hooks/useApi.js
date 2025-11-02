import { useState, useEffect } from 'react';
import api from '../api/http';

/**
 * Hook para facilitar chamadas à API
 * @param {string} url - URL do endpoint
 * @param {object} options - Opções da requisição
 */
export function useApi(url, options = {}) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!url) return;

    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await api.get(url, options);
        setData(response.data);
        setError(null);
      } catch (err) {
        setError(err.message || 'Erro ao carregar dados');
        setData(null);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url, JSON.stringify(options)]);

  return { data, loading, error };
}

export default useApi;
