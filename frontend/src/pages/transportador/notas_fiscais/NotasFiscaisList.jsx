import createResourceListPage from '../shared/createResourceListPage';

export default createResourceListPage({
  title: 'Notas Fiscais',
  description: 'Acompanhe notas fiscais emitidas, itens, impostos e anexos.',
  endpoints: [
    '/api/transportador/notas_fiscais/notas-fiscais/',
    '/api/transportador/notas_fiscais/itens/',
    '/api/transportador/notas_fiscais/impostos/',
    '/api/transportador/notas_fiscais/anexos/',
  ],
});
