import {
  Activity,
  Bell,
  Briefcase,
  Calendar,
  Calculator,
  Circle,
  Cog,
  CreditCard,
  DollarSign,
  FileBarChart,
  FileSignature,
  FileSpreadsheet,
  FileText,
  Fuel,
  GraduationCap,
  Gavel,
  Hammer,
  HardHat,
  Home,
  Building2,
  Layers,
  Map,
  MapPin,
  Navigation,
  Network,
  Package,
  PackageCheck,
  Route,
  ScrollText,
  Settings,
  Shield,
  ShieldCheck,
  ShoppingCart,
  Truck,
  Users,
  UserCheck,
  AlertTriangle,
  Archive,
  Boxes,
  Brain,
  Wrench,
} from 'lucide-react';

import IndexTransportador from '@/pages/transportador/Index';
import Frota from '@/pages/transportador/Frota';
import Pneus from '@/pages/transportador/Pneus';
import Estoque from '@/pages/transportador/Estoque';
import Manutencao from '@/pages/transportador/Manutencao';
import IADashboard from '@/pages/transportador/ia/Dashboard';
import Financeiro from '@/pages/transportador/Financeiro';
import Faturamento from '@/pages/transportador/Faturamento';
import Compras from '@/pages/transportador/Compras';
import Custos from '@/pages/transportador/Custos';
import Combustivel from '@/pages/transportador/Combustivel';
import Eventos from '@/pages/transportador/Eventos';
import Relatorios from '@/pages/transportador/Relatorios';
import Configuracoes from '@/pages/transportador/Configuracoes';
import EmpresasDashboard from '@/pages/transportador/empresas-dashboard/EmpresasDashboard';
import EmpresasDashboardEmpresas from '@/pages/transportador/empresas-dashboard/EmpresasList';
import EmpresasDashboardFiliais from '@/pages/transportador/empresas-dashboard/FiliaisList';
import EmpresasDashboardAgregados from '@/pages/transportador/empresas-dashboard/AgregadosList';
import FiliaisDashboard from '@/pages/transportador/filiais-dashboard/FiliaisDashboard';

import VeiculosList from '@/pages/transportador/frota/VeiculosList';
import VeiculoCreate from '@/pages/transportador/frota/VeiculoCreate';
import VeiculoEdit from '@/pages/transportador/frota/VeiculoEdit';
import VehicleDetail from '@/pages/transportador/frota/VehicleDetail';
import PosicoesList from '@/pages/transportador/frota/PosicoesList';
import Motoristas from '@/pages/transportador/Motoristas';
import Implementos from '@/pages/transportador/Implementos';
import Documentos from '@/pages/transportador/Documentos';
import Rastreamento from '@/pages/transportador/Rastreamento';
import Clientes from '@/pages/transportador/Clientes';
import Fornecedores from '@/pages/transportador/Fornecedores';
import Seguros from '@/pages/transportador/Seguros';
import Contratos from '@/pages/transportador/Contratos';
import AlertasList from '@/pages/transportador/alertas/AlertasList';
import AlmoxarifadoList from '@/pages/transportador/almoxarifado/AlmoxarifadoList';
import AuditoriaList from '@/pages/transportador/auditoria/AuditoriaList';
import CargasList from '@/pages/transportador/cargas/CargasList';
import ComplianceList from '@/pages/transportador/compliance/ComplianceList';
import EpisList from '@/pages/transportador/epis/EpisList';
import FerramentasList from '@/pages/transportador/ferramentas/FerramentasList';
import IntegracoesList from '@/pages/transportador/integracoes/IntegracoesList';
import NotasFiscaisList from '@/pages/transportador/notas_fiscais/NotasFiscaisList';
import PecasList from '@/pages/transportador/pecas/PecasList';
import TreinamentosList from '@/pages/transportador/treinamentos/TreinamentosList';
import Pagamentos from '@/pages/transportador/Pagamentos';
import Multas from '@/pages/transportador/Multas';
import Telemetria from '@/pages/transportador/Telemetria';
import Rotas from '@/pages/transportador/Rotas';
import Entregas from '@/pages/transportador/Entregas';
import Notificacoes from '@/pages/transportador/Notificacoes';
import Viagens from '@/pages/transportador/Viagens';

import PneusList from '@/pages/transportador/pneus/PneusList';
import PneuCreate from '@/pages/transportador/pneus/PneuCreate';
import PneuEdit from '@/pages/transportador/pneus/PneuEdit';
import AplicacoesList from '@/pages/transportador/pneus/AplicacoesList';
import ManutencaoPneus from '@/pages/transportador/ManutencaoPneus';
import AnaliseDesgaste from '@/pages/transportador/AnaliseDesgaste';
import Garantias from '@/pages/transportador/Garantias';
import EventosPneus from '@/pages/transportador/EventosPneus';

import MovimentacoesList from '@/pages/transportador/estoque/MovimentacoesList';
import ItensEstoque from '@/pages/transportador/ItensEstoque';
import EntradasSaidas from '@/pages/transportador/EntradasSaidas';
import RelatoriosEstoque from '@/pages/transportador/RelatoriosEstoque';

import OSList from '@/pages/transportador/manutencao/OSList';
import OSCreate from '@/pages/transportador/manutencao/OSCreate';
import OSEdit from '@/pages/transportador/manutencao/OSEdit';
import OSDetail from '@/pages/transportador/manutencao/OSDetail';
import TestesList from '@/pages/transportador/manutencao/TestesList';
import HistoricoManutencao from '@/pages/transportador/HistoricoManutencao';
import PlanejamentoPreventivo from '@/pages/transportador/PlanejamentoPreventivo';

import IAAnalise from '@/pages/transportador/ia/Analise';
import IAGamificacao from '@/pages/transportador/ia/Gamificacao';
import IAGarantias from '@/pages/transportador/ia/Garantias';

import RelatoriosFrota from '@/pages/transportador/RelatoriosFrota';
import RelatoriosPneus from '@/pages/transportador/RelatoriosPneus';
import RelatoriosManutencao from '@/pages/transportador/RelatoriosManutencao';
import RelatoriosFinanceiros from '@/pages/transportador/RelatoriosFinanceiros';

import MinhaEmpresa from '@/pages/transportador/MinhaEmpresa';
import MotoristasDashboard from '@/pages/transportador/motoristas-dashboard/MotoristasDashboard';
import ComprasDashboard from '@/pages/transportador/compras-dashboard/ComprasDashboard';
import EventosDashboard from '@/pages/transportador/eventos-dashboard/EventosDashboard';
import FinanceiroDashboard from '@/pages/transportador/financeiro-dashboard/FinanceiroDashboard';
import ConfiguracoesDashboard from '@/pages/transportador/configuracoes-dashboard/ConfiguracoesDashboard';

export const TRANSPORTADOR_MENU_ROUTES = [
  { path: '', label: 'Início', icon: Home, component: IndexTransportador, index: true },
  { path: 'frota', label: 'Frota', icon: Truck, component: Frota },
  { path: 'motoristas', label: 'Motoristas', icon: Users, component: MotoristasDashboard },
  { path: 'implementos', label: 'Implementos', icon: Layers, component: Implementos },
  { path: 'documentos', label: 'Documentos', icon: FileText, component: Documentos },
  { path: 'rastreamento', label: 'Rastreamento', icon: Map, component: Rastreamento },
  { path: 'pneus', label: 'Pneus', icon: Circle, component: Pneus },
  { path: 'estoque', label: 'Estoque', icon: Package, component: Estoque },
  { path: 'manutencao', label: 'Manutenção', icon: Wrench, component: Manutencao },
  { path: 'ia', label: 'IA - Análise', icon: Brain, component: IADashboard, highlight: true },
  { path: 'financeiro', label: 'Financeiro', icon: DollarSign, component: Financeiro },
  { path: 'faturamento', label: 'Faturamento', icon: FileBarChart, component: Faturamento },
  { path: 'pagamentos', label: 'Pagamentos', icon: CreditCard, component: Pagamentos },
  { path: 'custos', label: 'Custos', icon: Calculator, component: Custos },
  { path: 'combustivel', label: 'Combustível', icon: Fuel, component: Combustivel },
  { path: 'multas', label: 'Multas', icon: Gavel, component: Multas },
  { path: 'compras', label: 'Compras', icon: ShoppingCart, component: Compras },
  { path: 'eventos', label: 'Eventos', icon: Calendar, component: Eventos },
  { path: 'relatorios', label: 'Relatórios', icon: FileText, component: Relatorios },
  { path: 'configuracoes', label: 'Configurações', icon: Settings, component: Configuracoes },
  { path: 'empresas', label: 'Empresas', icon: Building2, component: EmpresasDashboard },
  { path: 'filiais', label: 'Filiais', icon: MapPin, component: FiliaisDashboard },
  { path: 'clientes', label: 'Clientes', icon: UserCheck, component: Clientes },
  { path: 'fornecedores', label: 'Fornecedores', icon: Briefcase, component: Fornecedores },
  { path: 'seguros', label: 'Seguros', icon: Shield, component: Seguros },
  { path: 'contratos', label: 'Contratos', icon: FileSignature, component: Contratos },
  { path: 'viagens', label: 'Viagens', icon: Navigation, component: Viagens },
  { path: 'rotas', label: 'Rotas', icon: Route, component: Rotas },
  { path: 'entregas', label: 'Entregas', icon: PackageCheck, component: Entregas },
  { path: 'alertas', label: 'Alertas', icon: AlertTriangle, component: AlertasList },
  { path: 'telemetria', label: 'Telemetria', icon: Activity, component: Telemetria },
  { path: 'notificacoes', label: 'Notificações', icon: Bell, component: Notificacoes },
  { path: 'auditoria', label: 'Auditoria', icon: ScrollText, component: AuditoriaList },
  { path: 'almoxarifado', label: 'Almoxarifado', icon: Archive, component: AlmoxarifadoList },
  { path: 'cargas', label: 'Cargas', icon: Boxes, component: CargasList },
  { path: 'compliance', label: 'Compliance', icon: ShieldCheck, component: ComplianceList },
  { path: 'epis', label: 'EPIs', icon: HardHat, component: EpisList },
  { path: 'ferramentas', label: 'Ferramentas', icon: Hammer, component: FerramentasList },
  { path: 'integracoes', label: 'Integrações', icon: Network, component: IntegracoesList },
  { path: 'notas-fiscais', label: 'Notas Fiscais', icon: FileSpreadsheet, component: NotasFiscaisList },
  { path: 'pecas', label: 'Peças', icon: Cog, component: PecasList },
  { path: 'treinamentos', label: 'Treinamentos', icon: GraduationCap, component: TreinamentosList },
];

export const TRANSPORTADOR_ADDITIONAL_ROUTES = [
  { path: 'frota/motoristas', component: MotoristasDashboard },
  { path: 'frota/veiculos', component: VeiculosList },
  { path: 'frota/veiculos/create', component: VeiculoCreate },
  { path: 'frota/veiculos/:id/edit', component: VeiculoEdit },
  { path: 'frota/veiculos/:id', component: VehicleDetail },
  { path: 'frota/posicoes', component: PosicoesList },
  { path: 'frota/motoristas/lista', component: Motoristas },
  { path: 'frota/implementos', component: Implementos },
  { path: 'frota/documentos', component: Documentos },
  { path: 'frota/rastreamento', component: Rastreamento },

  { path: 'pneus/lista', component: PneusList },
  { path: 'pneus/create', component: PneuCreate },
  { path: 'pneus/:id/edit', component: PneuEdit },
  { path: 'pneus/aplicacoes', component: AplicacoesList },
  { path: 'pneus/manutencao-pneus', component: ManutencaoPneus },
  { path: 'pneus/analise-desgaste', component: AnaliseDesgaste },
  { path: 'pneus/garantias', component: Garantias },
  { path: 'pneus/eventos-pneus', component: EventosPneus },

  { path: 'estoque/movimentacoes', component: MovimentacoesList },
  { path: 'estoque/itens', component: ItensEstoque },
  { path: 'estoque/entradas-saidas', component: EntradasSaidas },
  { path: 'estoque/relatorios-estoque', component: RelatoriosEstoque },

  { path: 'manutencao/ordens-servico', component: OSList },
  { path: 'manutencao/ordens-servico/create', component: OSCreate },
  { path: 'manutencao/ordens-servico/:id/edit', component: OSEdit },
  { path: 'manutencao/ordens-servico/:id', component: OSDetail },
  { path: 'manutencao/testes-pos-manutencao', component: TestesList },
  { path: 'manutencao/historico', component: HistoricoManutencao },
  { path: 'manutencao/planejamento-preventivo', component: PlanejamentoPreventivo },

  { path: 'ia/analise', component: IAAnalise },
  { path: 'ia/gamificacao', component: IAGamificacao },
  { path: 'ia/garantias', component: IAGarantias },

  { path: 'relatorios/frota', component: RelatoriosFrota },
  { path: 'relatorios/pneus', component: RelatoriosPneus },
  { path: 'relatorios/estoque', component: RelatoriosEstoque },
  { path: 'relatorios/manutencao', component: RelatoriosManutencao },
  { path: 'relatorios/financeiro', component: RelatoriosFinanceiros },

  { path: 'minha-empresa', component: MinhaEmpresa },
  { path: 'empresas-dashboard/empresas', component: EmpresasDashboardEmpresas },
  { path: 'empresas-dashboard/filiais', component: EmpresasDashboardFiliais },
  { path: 'empresas-dashboard/agregados', component: EmpresasDashboardAgregados },
  { path: 'financeiro/visao-geral', component: FinanceiroDashboard },
  { path: 'compras/dashboard', component: ComprasDashboard },
  { path: 'eventos/visao-geral', component: EventosDashboard },
  { path: 'configuracoes/visao-geral', component: ConfiguracoesDashboard },
];
