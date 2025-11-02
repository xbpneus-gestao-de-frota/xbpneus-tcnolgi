import { Link } from 'react-router-dom';
import { Building2, MapPin, Users, FileText, Settings, BarChart3 } from 'lucide-react';

function ModuleCard({ title, description, icon: Icon, to, color = "blue", stats }) {
  const colors = {
    blue: "from-blue-500/20 to-blue-600/20 hover:from-blue-500/30 hover:to-blue-600/30 border-blue-500/30",
    green: "from-green-500/20 to-green-600/20 hover:from-green-500/30 hover:to-green-600/30 border-green-500/30",
    purple: "from-purple-500/20 to-purple-600/20 hover:from-purple-500/30 hover:to-purple-600/30 border-purple-500/30",
    orange: "from-orange-500/20 to-orange-600/20 hover:from-orange-500/30 hover:to-orange-600/30 border-orange-500/30",
    indigo: "from-indigo-500/20 to-indigo-600/20 hover:from-indigo-500/30 hover:to-indigo-600/30 border-indigo-500/30"
  };

  const iconColors = {
    blue: "bg-blue-500/20 text-blue-400",
    green: "bg-green-500/20 text-green-400",
    purple: "bg-purple-500/20 text-purple-400",
    orange: "bg-orange-500/20 text-orange-400",
    indigo: "bg-indigo-500/20 text-indigo-400"
  };

  return (
    <Link
      to={to}
      className={`group relative overflow-hidden rounded-xl border bg-gradient-to-br ${colors[color]} p-6 backdrop-blur-sm transition-all hover:scale-105 hover:shadow-2xl`}
    >
      <div className="flex items-start justify-between mb-4">
        <div className={`rounded-xl ${iconColors[color]} p-4`}>
          <Icon className="h-8 w-8" />
        </div>
        {stats && (
          <div className="text-right">
            <p className="text-3xl font-bold text-white">{stats}</p>
            <p className="text-xs text-white/60">Total</p>
          </div>
        )}
      </div>
      <h3 className="text-xl font-bold text-white mb-2">{title}</h3>
      <p className="text-sm text-white/70">{description}</p>
      <div className="mt-4 flex items-center text-sm text-white/80 group-hover:text-white transition">
        <span>Acessar módulo</span>
        <svg className="ml-2 h-4 w-4 transform transition-transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
        </svg>
      </div>
    </Link>
  );
}

export default function EmpresasDashboard() {
  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white">Gestão de Empresas</h1>
        <p className="mt-2 text-white/70">Gerencie empresas, filiais, agregados e documentação</p>
      </div>

      {/* Stats Overview */}
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-xl border border-white/10 bg-gradient-to-br from-white/5 to-white/10 p-6 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-white/70">Total de Empresas</p>
              <p className="text-3xl font-bold text-white mt-2">5</p>
            </div>
            <Building2 className="h-10 w-10 text-blue-400" />
          </div>
        </div>
        <div className="rounded-xl border border-white/10 bg-gradient-to-br from-white/5 to-white/10 p-6 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-white/70">Total de Filiais</p>
              <p className="text-3xl font-bold text-white mt-2">12</p>
            </div>
            <MapPin className="h-10 w-10 text-green-400" />
          </div>
        </div>
        <div className="rounded-xl border border-white/10 bg-gradient-to-br from-white/5 to-white/10 p-6 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-white/70">Total de Agregados</p>
              <p className="text-3xl font-bold text-white mt-2">8</p>
            </div>
            <Users className="h-10 w-10 text-purple-400" />
          </div>
        </div>
        <div className="rounded-xl border border-white/10 bg-gradient-to-br from-white/5 to-white/10 p-6 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-white/70">Documentos</p>
              <p className="text-3xl font-bold text-white mt-2">45</p>
            </div>
            <FileText className="h-10 w-10 text-orange-400" />
          </div>
        </div>
      </div>

      {/* Module Cards */}
      <div>
        <h2 className="mb-6 text-2xl font-semibold text-white">Módulos Disponíveis</h2>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <ModuleCard
            title="Empresas"
            description="Cadastro e gerenciamento de empresas do grupo"
            icon={Building2}
            to="/dashboard/empresas-dashboard/empresas"
            color="blue"
            stats="5"
          />
          <ModuleCard
            title="Filiais"
            description="Gerenciar filiais e unidades operacionais"
            icon={MapPin}
            to="/dashboard/empresas-dashboard/filiais"
            color="green"
            stats="12"
          />
          <ModuleCard
            title="Agregados"
            description="Cadastro e gestão de motoristas agregados"
            icon={Users}
            to="/dashboard/empresas-dashboard/agregados"
            color="purple"
            stats="8"
          />
          <ModuleCard
            title="Documentos"
            description="Documentação e arquivos das empresas"
            icon={FileText}
            to="/dashboard/empresas-dashboard/documentos"
            color="orange"
            stats="45"
          />
          <ModuleCard
            title="Relatórios"
            description="Relatórios e análises de desempenho"
            icon={BarChart3}
            to="/dashboard/empresas-dashboard/relatorios"
            color="indigo"
          />
          <ModuleCard
            title="Configurações"
            description="Configurações gerais do módulo"
            icon={Settings}
            to="/dashboard/empresas-dashboard/configuracoes"
            color="blue"
          />
        </div>
      </div>

      {/* Quick Info */}
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-white/10 bg-gradient-to-br from-white/5 to-white/10 p-6 backdrop-blur-sm">
          <h3 className="text-lg font-semibold text-white mb-4">Empresas Recentes</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 rounded-lg bg-white/5">
              <div className="flex items-center gap-3">
                <Building2 className="h-5 w-5 text-blue-400" />
                <span className="text-white">Transportadora XYZ Ltda</span>
              </div>
              <span className="text-xs text-white/60">Ativa</span>
            </div>
            <div className="flex items-center justify-between p-3 rounded-lg bg-white/5">
              <div className="flex items-center gap-3">
                <Building2 className="h-5 w-5 text-blue-400" />
                <span className="text-white">Logística ABC S/A</span>
              </div>
              <span className="text-xs text-white/60">Ativa</span>
            </div>
          </div>
        </div>

        <div className="rounded-xl border border-white/10 bg-gradient-to-br from-white/5 to-white/10 p-6 backdrop-blur-sm">
          <h3 className="text-lg font-semibold text-white mb-4">Atividades Recentes</h3>
          <div className="space-y-3">
            <div className="flex items-start gap-3 p-3 rounded-lg bg-white/5">
              <div className="rounded-full bg-green-500/20 p-2">
                <Building2 className="h-4 w-4 text-green-400" />
              </div>
              <div className="flex-1">
                <p className="text-sm text-white">Nova empresa cadastrada</p>
                <p className="text-xs text-white/50 mt-1">Há 2 horas</p>
              </div>
            </div>
            <div className="flex items-start gap-3 p-3 rounded-lg bg-white/5">
              <div className="rounded-full bg-blue-500/20 p-2">
                <MapPin className="h-4 w-4 text-blue-400" />
              </div>
              <div className="flex-1">
                <p className="text-sm text-white">Filial atualizada</p>
                <p className="text-xs text-white/50 mt-1">Há 5 horas</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

