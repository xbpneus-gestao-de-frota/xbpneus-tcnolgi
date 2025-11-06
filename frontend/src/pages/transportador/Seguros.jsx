import createResourceListPage from './shared/createResourceListPage';

export default createResourceListPage({
  title: 'Seguros',
  description: 'Monitore apólices, seguradoras e sinistros integrados ao módulo de seguros do transportador.',
  endpoints: [
    '/api/transportador/seguros/apolices/',
    '/api/transportador/seguros/seguradoras/',
    '/api/transportador/seguros/sinistros/',
  ],
});
