import createResourceListPage from '../shared/createResourceListPage';

export default createResourceListPage({
  title: 'Ferramentas',
  description: 'Controle o cadastro de ferramentas, manutenções, calibrações e empréstimos.',
  endpoints: [
    '/api/transportador/ferramentas/ferramentas/',
    '/api/transportador/ferramentas/manutencaoferramentas/',
    '/api/transportador/ferramentas/emprestimoferramentas/',
    '/api/transportador/ferramentas/calibracaoferramentas/',
  ],
});
