import createResourceListPage from '../shared/createResourceListPage';

export default createResourceListPage({
  title: 'Relatórios Avançados',
  description: 'Consulte templates, agendamentos e resultados gerados pelo módulo de relatórios.',
  endpoints: [
    '/api/transportador/relatorios/relatoriogerados/',
    '/api/transportador/relatorios/relatorioagendados/',
    '/api/transportador/relatorios/relatoriotemplates/',
    '/api/transportador/relatorios/dashboardpersonalizados/',
  ],
});
