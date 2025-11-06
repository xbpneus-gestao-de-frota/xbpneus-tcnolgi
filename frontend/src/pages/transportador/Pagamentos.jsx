import createResourceListPage from './shared/createResourceListPage';

export default createResourceListPage({
  title: 'Pagamentos',
  description: 'Concilie contas a pagar, receber e lançamentos de pagamento expostos pela API.',
  endpoints: [
    '/api/transportador/pagamentos/pagamentos/',
    '/api/transportador/pagamentos/contas-pagar/',
    '/api/transportador/pagamentos/contas-receber/',
  ],
});
