import createResourceListPage from './shared/createResourceListPage';

export default createResourceListPage({
  title: 'Custos Operacionais',
  description: 'Consulte categorias de custo, lançamentos e indicadores de custo por quilômetro expostos pelo backend.',
  endpoints: [
    '/api/transportador/custos/custos/',
    '/api/transportador/custos/categorias/',
    '/api/transportador/custos/custo-por-km/',
  ],
});
