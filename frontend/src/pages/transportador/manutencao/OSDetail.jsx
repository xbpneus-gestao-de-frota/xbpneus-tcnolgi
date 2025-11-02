import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../../api/http';
import PageHeader from '../../../components/PageHeader';
import Loader from '../../../components/Loader';

const OSDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [os, setOS] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOS();
  }, [id]);

  const fetchOS = async () => {
    try {
      const response = await api.get(`/transportador/manutencao/ordens-servico/${id}/`);
      setOS(response.data);
    } catch (err) {
      console.error('Erro:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loader />;
  if (!os) return <div>OS não encontrada</div>;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-6">
      <PageHeader title={`Ordem de Serviço #${os.numero_os || id}`} />
      <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-lg p-8 mt-6">
        <div className="grid grid-cols-2 gap-4">
          <div><strong>Veículo:</strong> {os.veiculo_placa}</div>
          <div><strong>Tipo:</strong> {os.tipo}</div>
          <div><strong>Status:</strong> {os.status}</div>
          <div><strong>Prioridade:</strong> {os.prioridade}</div>
          <div className="col-span-2"><strong>Descrição:</strong> {os.descricao}</div>
        </div>
        <button onClick={() => navigate('/dashboard/manutencao/ordens-servico')} 
                className="mt-6 px-6 py-2 bg-blue-600 text-white rounded-lg">
          Voltar
        </button>
      </div>
    </div>
  );
};
export default OSDetail;
