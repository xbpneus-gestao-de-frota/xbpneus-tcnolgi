import createResourceListPage from '../shared/createResourceListPage';

export default createResourceListPage({
  title: 'Almoxarifado',
  description: 'Visualize almoxarifados, movimentações, inventários e requisições em aberto.',
  endpoints: [
    '/api/transportador/almoxarifado/almoxarifados/',
    '/api/transportador/almoxarifado/movimentacoes/',
    '/api/transportador/almoxarifado/inventarios/',
    '/api/transportador/almoxarifado/locais-estoque/',
    '/api/transportador/almoxarifado/requisicoes/',
    '/api/transportador/almoxarifado/itens-requisicao/',
    '/api/transportador/almoxarifado/itens-inventario/',
  ],
});
