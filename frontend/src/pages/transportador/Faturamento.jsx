import createResourceListPage from './shared/createResourceListPage';

export default createResourceListPage({
  title: 'Faturamento',
  description: 'Acesse faturas emitidas, itens faturados e notas fiscais sincronizadas com o backend.',
  endpoints: [
    '/api/transportador/faturamento/faturas/',
    '/api/transportador/faturamento/itens/',
    '/api/transportador/faturamento/notas-fiscais/',
  ],
});
