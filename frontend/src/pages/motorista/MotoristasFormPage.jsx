import React, { useState, useEffect } from 'react';
import { ArrowLeft, Save } from 'lucide-react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { xbpneusClasses } from '../../styles/colors';

const MotoristasFormPage = () => {
  const { id } = useParams();
  const isEditing = !!id;
  const [loading, setLoading] = useState(isEditing);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [formData, setFormData] = useState({
    nome_completo: '',
    email: '',
    telefone: '',
    cpf: '',
    cnh: '',
    data_nascimento: '',
    endereco: {
      rua: '',
      numero: '',
      complemento: '',
      cidade: '',
      estado: '',
      cep: ''
    },
    ativo: true
  });

  useEffect(() => {
    if (isEditing) {
      fetchMotorista();
    }
  }, [id]);

  const fetchMotorista = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('access_token');
      const response = await axios.get(`/api/motorista/${id}/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      setFormData(response.data);
    } catch (err) {
      console.error('Erro ao buscar motorista:', err);
      setError(err.response?.data?.message || 'Erro ao carregar motorista');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    if (name.startsWith('endereco.')) {
      const field = name.split('.')[1];
      setFormData({
        ...formData,
        endereco: {
          ...formData.endereco,
          [field]: value
        }
      });
    } else {
      setFormData({
        ...formData,
        [name]: type === 'checkbox' ? checked : value
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const token = localStorage.getItem('access_token');
      
      if (isEditing) {
        await axios.put(`/api/motorista/${id}/`, formData, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        setSuccessMessage('Motorista atualizado com sucesso!');
      } else {
        await axios.post('/api/motorista/', formData, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        setSuccessMessage('Motorista criado com sucesso!');
      }
      
      setTimeout(() => {
        window.location.href = '/motorista';
      }, 2000);
    } catch (err) {
      console.error('Erro ao salvar motorista:', err);
      setError(err.response?.data?.message || 'Erro ao salvar motorista');
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
            onClick={() => window.location.href = '/motorista'}
            className={`${xbpneusClasses.buttonSecondary} px-4 py-2 rounded-lg flex items-center gap-2 mb-4`}
          >
            <ArrowLeft size={16} />
            Voltar
          </button>
          <h1 className={`${xbpneusClasses.cardTitle} text-3xl mb-2`}>
            {isEditing ? 'Editar Motorista' : 'Novo Motorista'}
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
          {/* Informações Pessoais */}
          <div className="mb-8">
            <h2 className={`${xbpneusClasses.cardTitle} text-xl mb-6`}>
              Informações Pessoais
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className={xbpneusClasses.inputLabel}>Nome Completo *</label>
                <input
                  type="text"
                  name="nome_completo"
                  value={formData.nome_completo}
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
                <label className={xbpneusClasses.inputLabel}>CPF *</label>
                <input
                  type="text"
                  name="cpf"
                  value={formData.cpf}
                  onChange={handleChange}
                  required
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>CNH *</label>
                <input
                  type="text"
                  name="cnh"
                  value={formData.cnh}
                  onChange={handleChange}
                  required
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Data de Nascimento</label>
                <input
                  type="date"
                  name="data_nascimento"
                  value={formData.data_nascimento}
                  onChange={handleChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
            </div>
          </div>

          {/* Endereço */}
          <div className="mb-8">
            <h2 className={`${xbpneusClasses.cardTitle} text-xl mb-6`}>
              Endereço
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="md:col-span-2">
                <label className={xbpneusClasses.inputLabel}>Rua</label>
                <input
                  type="text"
                  name="endereco.rua"
                  value={formData.endereco.rua}
                  onChange={handleChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Número</label>
                <input
                  type="text"
                  name="endereco.numero"
                  value={formData.endereco.numero}
                  onChange={handleChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Complemento</label>
                <input
                  type="text"
                  name="endereco.complemento"
                  value={formData.endereco.complemento}
                  onChange={handleChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Cidade</label>
                <input
                  type="text"
                  name="endereco.cidade"
                  value={formData.endereco.cidade}
                  onChange={handleChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Estado</label>
                <input
                  type="text"
                  name="endereco.estado"
                  value={formData.endereco.estado}
                  onChange={handleChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>CEP</label>
                <input
                  type="text"
                  name="endereco.cep"
                  value={formData.endereco.cep}
                  onChange={handleChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
            </div>
          </div>

          {/* Status */}
          <div className="mb-8">
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                name="ativo"
                checked={formData.ativo}
                onChange={handleChange}
                className="w-4 h-4"
              />
              <span className={xbpneusClasses.inputLabel}>Ativo</span>
            </label>
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
              onClick={() => window.location.href = '/motorista'}
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

export default MotoristasFormPage;

