import createResourceListPage from '../shared/createResourceListPage';

export default createResourceListPage({
  title: 'Peças',
  description: 'Integra catálogo, estoque, movimentações e fornecedores de peças.',
  endpoints: [
    '/api/transportador/pecas/pecas/',
    '/api/transportador/pecas/categoriapecas/',
    '/api/transportador/pecas/estoquepecas/',
    '/api/transportador/pecas/movimentacaopecas/',
    '/api/transportador/pecas/fornecedorpecas/',
  ],
});
