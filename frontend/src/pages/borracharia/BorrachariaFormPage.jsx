import React, { useState, useEffect } from 'react';
import { ArrowLeft, Save } from 'lucide-react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { xbpneusClasses } from '../../styles/colors';

const BorrachariaFormPage = () => {
  const { id } = useParams();
  const isEditing = !!id;
  const [loading, setLoading] = useState(isEditing);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [formData, setFormData] = useState({
    nome_empresa: '',
    cnpj: '',
    email: '',
    telefone: '',
    cidade: '',
    estado: '',
    endereco: '',
    contato_responsavel: {
      nome: '',
      email: ''
    }
  });

  useEffect(() => {
    if (isEditing) {
      fetchBorracharia();
    }
  }, [id]);

  const fetchBorracharia = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('access_token');
      const response = await axios.get(`/api/borracharia/${id}/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      setFormData(response.data);
    } catch (err) {
      console.error('Erro ao buscar borracharia:', err);
      setError(err.response?.data?.message || 'Erro ao carregar borracharia');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    if (name.startsWith('contato_responsavel.')) {
      const field = name.split('.')[1];
      setFormData({
        ...formData,
        contato_responsavel: {
          ...formData.contato_responsavel,
          [field]: value
        }
      });
    } else {
      setFormData({
        ...formData,
        [name]: value
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const token = localStorage.getItem('access_token');
      
      if (isEditing) {
        await axios.put(`/api/borracharia/${id}/`, formData, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        setSuccessMessage('Borracharia atualizada com sucesso!');
      } else {
        await axios.post('/api/borracharia/', formData, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        setSuccessMessage('Borracharia criada com sucesso!');
      }
      
      setTimeout(() => {
        window.location.href = '/borracharia';
      }, 2000);
    } catch (err) {
      console.error('Erro ao salvar borracharia:', err);
      setError(err.response?.data?.message || 'Erro ao salvar borracharia');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-6 flex items-center justify-center">
        <p className="text-gray-600">Carregando...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Cabeçalho */}
        <div className="mb-8">
          <button
            onClick={() => window.location.href = '/borracharia'}
            className={`${xbpneusClasses.buttonSecondary} px-4 py-2 rounded-lg flex items-center gap-2 mb-4`}
          >
            <ArrowLeft size={16} />
            Voltar
          </button>
          <h1 className={`${xbpneusClasses.cardTitle} text-3xl mb-2`}>
            {isEditing ? 'Editar Borracharia' : 'Nova Borracharia'}
          </h1>
        </div>

        {/* Mensagens */}
        {successMessage && (
          <div className="mb-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded">
            {successMessage}
          </div>
        )}
        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        {/* Formulário */}
        <form onSubmit={handleSubmit} className={`${xbpneusClasses.card} p-6`}>
          {/* Informações da Empresa */}
          <div className="mb-8">
            <h2 className={`${xbpneusClasses.cardTitle} text-xl mb-6`}>
              Informações da Empresa
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className={xbpneusClasses.inputLabel}>Nome da Empresa *</label>
                <input
                  type="text"
                  name="nome_empresa"
                  value={formData.nome_empresa}
                  onChange={handleChange}
                  required
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>CNPJ *</label>
                <input
                  type="text"
                  name="cnpj"
                  value={formData.cnpj}
                  onChange={handleChange}
                  required
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Email *</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Telefone *</label>
                <input
                  type="tel"
                  name="telefone"
                  value={formData.telefone}
                  onChange={handleChange}
                  required
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Cidade *</label>
                <input
                  type="text"
                  name="cidade"
                  value={formData.cidade}
                  onChange={handleChange}
                  required
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Estado *</label>
                <input
                  type="text"
                  name="estado"
                  value={formData.estado}
                  onChange={handleChange}
                  required
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div className="md:col-span-2">
                <label className={xbpneusClasses.inputLabel}>Endereço</label>
                <input
                  type="text"
                  name="endereco"
                  value={formData.endereco}
                  onChange={handleChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
            </div>
          </div>

          {/* Contato Responsável */}
          <div className="mb-8">
            <h2 className={`${xbpneusClasses.cardTitle} text-xl mb-6`}>
              Contato Responsável
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className={xbpneusClasses.inputLabel}>Nome</label>
                <input
                  type="text"
                  name="contato_responsavel.nome"
                  value={formData.contato_responsavel?.nome || ''}
                  onChange={handleChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Email</label>
                <input
                  type="email"
                  name="contato_responsavel.email"
                  value={formData.contato_responsavel?.email || ''}
                  onChange={handleChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
            </div>
          </div>

          {/* Botões */}
          <div className="flex gap-4">
            <button
              type="submit"
              className={`${xbpneusClasses.buttonPrimary} px-6 py-2 rounded-lg flex items-center gap-2`}
            >
              <Save size={16} />
              Salvar
            </button>
            <button
              type="button"
              onClick={() => window.location.href = '/borracharia'}
              className={`${xbpneusClasses.buttonSecondary} px-6 py-2 rounded-lg`}
            >
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default BorrachariaFormPage;

