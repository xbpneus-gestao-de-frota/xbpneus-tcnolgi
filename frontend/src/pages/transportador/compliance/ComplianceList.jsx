import createResourceListPage from '../shared/createResourceListPage';

export default createResourceListPage({
  title: 'Compliance',
  description: 'Acompanhe normas, auditorias e planos de ação definidos pelo módulo de compliance.',
  endpoints: [
    '/api/transportador/compliance/naoconformidades/',
    '/api/transportador/compliance/planoacaocompliances/',
    '/api/transportador/compliance/auditoriacompliances/',
    '/api/transportador/compliance/normacompliances/',
  ],
});
