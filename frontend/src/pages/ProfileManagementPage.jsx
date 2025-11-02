import React, { useState, useEffect } from 'react';
import { Edit, Key, Save, X } from 'lucide-react';
import axios from 'axios';
import { xbpneusClasses, xbpneusColors } from '../styles/colors';

const ProfileManagementPage = () => {
  const [editingProfile, setEditingProfile] = useState(false);
  const [editingPassword, setEditingPassword] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [profileData, setProfileData] = useState({
    nome_completo: '',
    email: '',
    telefone: '',
    empresa: '',
  });
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  useEffect(() => {
    fetchUserProfile();
  }, []);

  const fetchUserProfile = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('access_token');
      const response = await axios.get('/api/users/me/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      setProfileData(response.data);
    } catch (err) {
      console.error('Erro ao buscar perfil:', err);
      setError(err.response?.data?.message || 'Erro ao carregar perfil');
    } finally {
      setLoading(false);
    }
  };

  const handleProfileChange = (e) => {
    const { name, value } = e.target;
    setProfileData({ ...profileData, [name]: value });
  };

  const handlePasswordChange = (e) => {
    const { name, value } = e.target;
    setPasswordData({ ...passwordData, [name]: value });
  };

  const handleSaveProfile = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.put(
        '/api/users/me/',
        profileData,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      setSuccessMessage('Perfil atualizado com sucesso!');
      setEditingProfile(false);
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err) {
      console.error('Erro ao atualizar perfil:', err);
      setError(err.response?.data?.message || 'Erro ao atualizar perfil');
    }
  };

  const handleChangePassword = async () => {
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setError('As senhas não correspondem');
      return;
    }

    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.post(
        '/api/users/change-password/',
        {
          old_password: passwordData.currentPassword,
          new_password: passwordData.newPassword
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      setSuccessMessage('Senha alterada com sucesso!');
      setEditingPassword(false);
      setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' });
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err) {
      console.error('Erro ao alterar senha:', err);
      setError(err.response?.data?.message || 'Erro ao alterar senha');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-6 flex items-center justify-center">
        <p className="text-gray-600">Carregando perfil...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-2xl mx-auto">
        {/* Cabeçalho */}
        <div className="mb-8">
          <h1 className={`${xbpneusClasses.cardTitle} text-3xl mb-2`}>
            Gerenciamento de Perfil
          </h1>
          <p className="text-gray-600">Atualize suas informações pessoais e segurança</p>
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

        {/* Seção de Edição de Perfil */}
        <div className={`${xbpneusClasses.card} p-6 mb-6`}>
          <div className="flex justify-between items-center mb-6">
            <h2 className={`${xbpneusClasses.cardTitle} text-xl`}>Informações Pessoais</h2>
            {!editingProfile && (
              <button
                onClick={() => setEditingProfile(true)}
                className={`${xbpneusClasses.buttonPrimary} px-4 py-2 rounded-lg flex items-center gap-2 text-sm`}
              >
                <Edit size={16} />
                Editar Perfil
              </button>
            )}
          </div>

          {editingProfile ? (
            <div className="space-y-4">
              <div>
                <label className={xbpneusClasses.inputLabel}>Nome Completo</label>
                <input
                  type="text"
                  name="nome_completo"
                  value={profileData.nome_completo || ''}
                  onChange={handleProfileChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Email</label>
                <input
                  type="email"
                  name="email"
                  value={profileData.email || ''}
                  onChange={handleProfileChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Telefone</label>
                <input
                  type="tel"
                  name="telefone"
                  value={profileData.telefone || ''}
                  onChange={handleProfileChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Empresa</label>
                <input
                  type="text"
                  name="empresa"
                  value={profileData.empresa || ''}
                  onChange={handleProfileChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                />
              </div>

              <div className="flex gap-2 pt-4">
                <button
                  onClick={handleSaveProfile}
                  className={`${xbpneusClasses.buttonPrimary} px-6 py-2 rounded-lg flex items-center gap-2`}
                >
                  <Save size={16} />
                  Salvar Alterações
                </button>
                <button
                  onClick={() => setEditingProfile(false)}
                  className={`${xbpneusClasses.buttonSecondary} px-6 py-2 rounded-lg flex items-center gap-2`}
                >
                  <X size={16} />
                  Cancelar
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-600">Nome Completo</p>
                <p className={`${xbpneusClasses.cardTitle}`}>{profileData.nome_completo || 'N/A'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Email</p>
                <p className={`${xbpneusClasses.cardTitle}`}>{profileData.email || 'N/A'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Telefone</p>
                <p className={`${xbpneusClasses.cardTitle}`}>{profileData.telefone || 'N/A'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Empresa</p>
                <p className={`${xbpneusClasses.cardTitle}`}>{profileData.empresa || 'N/A'}</p>
              </div>
            </div>
          )}
        </div>

        {/* Seção de Alteração de Senha */}
        <div className={`${xbpneusClasses.card} p-6`}>
          <div className="flex justify-between items-center mb-6">
            <h2 className={`${xbpneusClasses.cardTitle} text-xl`}>Segurança</h2>
            {!editingPassword && (
              <button
                onClick={() => setEditingPassword(true)}
                className={`${xbpneusClasses.buttonPrimary} px-4 py-2 rounded-lg flex items-center gap-2 text-sm`}
              >
                <Key size={16} />
                Alterar Senha
              </button>
            )}
          </div>

          {editingPassword ? (
            <div className="space-y-4">
              <div>
                <label className={xbpneusClasses.inputLabel}>Senha Atual</label>
                <input
                  type="password"
                  name="currentPassword"
                  value={passwordData.currentPassword}
                  onChange={handlePasswordChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                  style={{ color: xbpneusColors.text.primary }}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Nova Senha</label>
                <input
                  type="password"
                  name="newPassword"
                  value={passwordData.newPassword}
                  onChange={handlePasswordChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                  style={{ color: xbpneusColors.text.primary }}
                />
              </div>
              <div>
                <label className={xbpneusClasses.inputLabel}>Confirmar Nova Senha</label>
                <input
                  type="password"
                  name="confirmPassword"
                  value={passwordData.confirmPassword}
                  onChange={handlePasswordChange}
                  className={`${xbpneusClasses.input} w-full mt-1`}
                  style={{ color: xbpneusColors.text.primary }}
                />
              </div>

              <div className="flex gap-2 pt-4">
                <button
                  onClick={handleChangePassword}
                  className={`${xbpneusClasses.buttonPrimary} px-6 py-2 rounded-lg flex items-center gap-2`}
                >
                  <Save size={16} />
                  Alterar Senha
                </button>
                <button
                  onClick={() => setEditingPassword(false)}
                  className={`${xbpneusClasses.buttonSecondary} px-6 py-2 rounded-lg flex items-center gap-2`}
                >
                  <X size={16} />
                  Cancelar
                </button>
              </div>
            </div>
          ) : (
            <p className="text-gray-600">Clique em "Alterar Senha" para atualizar sua senha</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfileManagementPage;

