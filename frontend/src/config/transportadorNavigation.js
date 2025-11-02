import { Home, Truck, Circle, Package, Wrench, Brain, DollarSign, ShoppingCart, Calendar, FileText, Settings, Building2, MapPin } from 'lucide-react';

import IndexTransportador from '@/pages/transportador/Index';
import Frota from '@/pages/transportador/Frota';
import Pneus from '@/pages/transportador/Pneus';
import Estoque from '@/pages/transportador/Estoque';
import Manutencao from '@/pages/transportador/Manutencao';
import IADashboard from '@/pages/transportador/ia/Dashboard';
import Financeiro from '@/pages/transportador/Financeiro';
import Compras from '@/pages/transportador/Compras';
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
  { path: 'pneus', label: 'Pneus', icon: Circle, component: Pneus },
  { path: 'estoque', label: 'Estoque', icon: Package, component: Estoque },
  { path: 'manutencao', label: 'Manutenção', icon: Wrench, component: Manutencao },
  { path: 'ia', label: 'IA - Análise', icon: Brain, component: IADashboard, highlight: true },
  { path: 'financeiro', label: 'Financeiro', icon: DollarSign, component: Financeiro },
  { path: 'compras', label: 'Compras', icon: ShoppingCart, component: Compras },
  { path: 'eventos', label: 'Eventos', icon: Calendar, component: Eventos },
  { path: 'relatorios', label: 'Relatórios', icon: FileText, component: Relatorios },
  { path: 'configuracoes', label: 'Configurações', icon: Settings, component: Configuracoes },
  { path: 'empresas', label: 'Empresas', icon: Building2, component: EmpresasDashboard },
  { path: 'filiais', label: 'Filiais', icon: MapPin, component: FiliaisDashboard },
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
