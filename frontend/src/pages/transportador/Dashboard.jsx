import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../../api/http";
import { 
  Truck, 
  Circle, 
  Package, 
  Wrench, 
  TrendingUp, 
  AlertTriangle,
  CheckCircle,
  Clock,
  DollarSign,
  Activity,
  Building2
} from "lucide-react";

function StatCard({ title, value, icon: Icon, trend, color = "blue" }) {
  const colors = {
    blue: "from-blue-500 to-blue-600",
    green: "from-green-500 to-green-600",
    orange: "from-orange-500 to-orange-600",
    red: "from-red-500 to-red-600",
    purple: "from-purple-500 to-purple-600",
    cyan: "from-cyan-500 to-cyan-600"
  };

  return (
    <div className="relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/5 to-white/10 p-6 backdrop-blur-sm transition-all hover:scale-105 hover:shadow-xl">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-white/70">{title}</p>
          <h3 className="mt-2 text-3xl font-bold text-white">{value}</h3>
          {trend && (
            <div className="mt-2 flex items-center gap-1 text-sm">
              <TrendingUp className="h-4 w-4 text-green-400" />
              <span className="text-green-400">{trend}</span>
            </div>
          )}
        </div>
        <div className={`rounded-xl bg-gradient-to-br ${colors[color]} p-3`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
      </div>
    </div>
  );
}

function QuickAction({ title, description, icon: Icon, to, color = "blue" }) {
  const colors = {
    blue: "from-blue-500/20 to-blue-600/20 hover:from-blue-500/30 hover:to-blue-600/30",
    green: "from-green-500/20 to-green-600/20 hover:from-green-500/30 hover:to-green-600/30",
    orange: "from-orange-500/20 to-orange-600/20 hover:from-orange-500/30 hover:to-orange-600/30",
    purple: "from-purple-500/20 to-purple-600/20 hover:from-purple-500/30 hover:to-purple-600/30"
  };

  return (
    <Link
      to={to}
      className={`group relative overflow-hidden rounded-xl border border-white/10 bg-gradient-to-br ${colors[color]} p-6 backdrop-blur-sm transition-all hover:scale-105 hover:shadow-lg`}
    >
      <div className="flex items-start gap-4">
        <div className="rounded-lg bg-white/10 p-3">
          <Icon className="h-6 w-6 text-white" />
        </div>
        <div className="flex-1">
          <h4 className="font-semibold text-white">{title}</h4>
          <p className="mt-1 text-sm text-white/70">{description}</p>
        </div>
      </div>
    </Link>
  );
}

function AlertCard({ type, message, time }) {
  const types = {
    warning: { icon: AlertTriangle, color: "text-orange-400", bg: "bg-orange-500/10" },
    error: { icon: AlertTriangle, color: "text-red-400", bg: "bg-red-500/10" },
    success: { icon: CheckCircle, color: "text-green-400", bg: "bg-green-500/10" },
    info: { icon: Activity, color: "text-blue-400", bg: "bg-blue-500/10" }
  };

  const config = types[type] || types.info;
  const Icon = config.icon;

  return (
    <div className={`flex items-start gap-3 rounded-lg border border-white/10 ${config.bg} p-4`}>
      <Icon className={`h-5 w-5 ${config.color} mt-0.5`} />
      <div className="flex-1">
        <p className="text-sm text-white">{message}</p>
        <p className="mt-1 text-xs text-white/50">{time}</p>
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;

    const fetchMetrics = async () => {
      try {
        const response = await api.get("/api/transportador/dashboard/");
        if (mounted) {
          setMetrics(response.data);
          setLoading(false);
        }
      } catch (err) {
        if (mounted) {
          setError(err.message);
          setLoading(false);
        }
      }
    };

    fetchMetrics();
    return () => { mounted = false; };
  }, []);

  if (loading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="text-center">
          <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-white/20 border-t-white"></div>
          <p className="mt-4 text-white/70">Carregando dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-xl border border-red-500/20 bg-red-500/10 p-6">
        <div className="flex items-center gap-3">
          <AlertTriangle className="h-6 w-6 text-red-400" />
          <div>
            <h3 className="font-semibold text-red-400">Erro ao carregar dashboard</h3>
            <p className="mt-1 text-sm text-red-400/70">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white">Dashboard</h1>
        <p className="mt-2 text-white/70">Visão geral da sua frota e operações</p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Total de Veículos"
          value={metrics?.total_veiculos || 0}
          icon={Truck}
          trend="+5% este mês"
          color="blue"
        />
        <StatCard
          title="Veículos Ativos"
          value={metrics?.veiculos_ativos || 0}
          icon={CheckCircle}
          trend="100% operacional"
          color="green"
        />
        <StatCard
          title="Total de Pneus"
          value={metrics?.total_pneus || 0}
          icon={Circle}
          color="purple"
        />
        <StatCard
          title="OS Abertas"
          value={metrics?.os_abertas || 0}
          icon={Wrench}
          color="orange"
        />
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="mb-4 text-xl font-semibold text-white">Ações Rápidas</h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <QuickAction
            title="Empresas"
            description="Gerenciar empresas, filiais e agregados"
            icon={Building2}
            to="/dashboard/empresas-dashboard"
            color="blue"
          />
            <QuickAction
              title="Frota"
              description="Gerenciar veículos, motoristas e rastreamento"
              icon={Truck}
              to="/dashboard/frota-dashboard"
              color="cyan"
            />
            <QuickAction
              title="Pneus"
              description="Gerenciar o ciclo de vida dos pneus da frota"
              icon={Circle}
              to="/dashboard/pneus-dashboard"
              color="purple"
            />
            <QuickAction
              title="Estoque"
              description="Gerenciar movimentações e inventário do estoque"
              icon={Package}
              to="/dashboard/estoque-dashboard"
              color="orange"
            />
            <QuickAction
              title="Manutenção"
              description="Gerenciar ordens de serviço e testes pós-manutenção"
              icon={Wrench}
              to="/dashboard/manutencao-dashboard"
              color="purple"
            />
          <QuickAction
            title="Adicionar Veículo"
            description="Cadastrar novo veículo na frota"
            icon={Truck}
            to="/dashboard/frota/veiculos"
            color="green"
          />
          <QuickAction
            title="Registrar Pneu"
            description="Adicionar pneu ao estoque"
            icon={Circle}
            to="/dashboard/pneus/lista"
            color="purple"
          />
          <QuickAction
            title="Nova OS"
            description="Abrir ordem de serviço"
            icon={Wrench}
            to="/dashboard/manutencao/os"
            color="orange"
          />
        </div>
      </div>

      {/* Alerts and Activity */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Alerts */}
        <div>
          <h2 className="mb-4 text-xl font-semibold text-white">Alertas Recentes</h2>
          <div className="space-y-3">
            <AlertCard
              type="warning"
              message="Veículo ABC1234 próximo da manutenção preventiva"
              time="Há 2 horas"
            />
            <AlertCard
              type="info"
              message="3 pneus com sulco abaixo do recomendado"
              time="Há 5 horas"
            />
            <AlertCard
              type="success"
              message="Manutenção do veículo DEF5678 concluída"
              time="Há 1 dia"
            />
          </div>
        </div>

        {/* Recent Activity */}
        <div>
          <h2 className="mb-4 text-xl font-semibold text-white">Atividade Recente</h2>
          <div className="space-y-3">
            <div className="flex items-start gap-3 rounded-lg border border-white/10 bg-white/5 p-4">
              <Clock className="h-5 w-5 text-blue-400 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm text-white">Veículo NEW9845 cadastrado</p>
                <p className="mt-1 text-xs text-white/50">Há 30 minutos</p>
              </div>
            </div>
            <div className="flex items-start gap-3 rounded-lg border border-white/10 bg-white/5 p-4">
              <Activity className="h-5 w-5 text-green-400 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm text-white">Pneu PN001 aplicado no veículo ABC1234</p>
                <p className="mt-1 text-xs text-white/50">Há 2 horas</p>
              </div>
            </div>
            <div className="flex items-start gap-3 rounded-lg border border-white/10 bg-white/5 p-4">
              <DollarSign className="h-5 w-5 text-purple-400 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm text-white">Compra de 10 pneus registrada</p>
                <p className="mt-1 text-xs text-white/50">Há 1 dia</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

