import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import DataTable from '../../../components/DataTable';
import { get } from '../../../api/http';

export default function NotasFiscaisList() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const response = await get('/api/transportador/notas_fiscais/');
      setData(response.data.results || response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'nome', label: 'Nome' },
    { key: 'criado_em', label: 'Criado em', type: 'datetime' },
  ];

  if (loading) return <div className="p-6">Carregando...</div>;
  if (error) return <div className="p-6 text-red-600">Erro: {error}</div>;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Notas Fiscais</h1>
        <Link
          to="/notas_fiscais/novo"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Novo
        </Link>
      </div>
      
      <DataTable
        data={data}
        columns={columns}
        onRefresh={loadData}
      />
    </div>
  );
}
