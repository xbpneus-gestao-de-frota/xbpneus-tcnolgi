import createResourceListPage from './shared/createResourceListPage';

export default createResourceListPage({
  title: 'Telemetria',
  description: 'Consulte dispositivos, leituras e alertas recebidos dos serviços de telemetria.',
  endpoints: [
    '/api/transportador/telemetria/leituras/',
    '/api/transportador/telemetria/dispositivos/',
    '/api/transportador/telemetria/alertas/',
  ],
});
