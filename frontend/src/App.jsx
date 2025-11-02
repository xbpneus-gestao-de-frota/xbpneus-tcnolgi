import { Routes, Route, Navigate, useParams } from 'react-router-dom';

import Login from './pages/Login';
import Cadastro from './pages/Cadastro';
import CadastroTipoCliente from './pages/CadastroTipoCliente';
import PosCadastro from './pages/PosCadastro';

import HubLayout from './pages/Hub/HubLayout';
import PilarPage from './pages/Hub/PillarPage';
import SubPage from './pages/Hub/SubPage';

import RequireAuth from '@/components/RequireAuth';
import ProtectedRoute from '@/components/ProtectedRoute';
import LayoutTransportador from '@/components/LayoutTransportador';

import DashboardMotorista from './pages/motorista/DashboardMotorista';
import DashboardRevenda from './pages/revenda/DashboardRevenda';
import DashboardBorracharia from './pages/borracharia/DashboardBorracharia';
import DashboardRecapagem from './pages/recapagem/DashboardRecapagem';

import { TRANSPORTADOR_MENU_ROUTES, TRANSPORTADOR_ADDITIONAL_ROUTES } from '@/config/transportadorNavigation';

function renderRoutes(routes) {
  return routes.map((route) => {
    const Component = route.component;
    const element = (
      <RequireAuth>
        <Component />
      </RequireAuth>
    );

    if (route.index) {
      return <Route index element={element} key="transportador-index" />;
    }

    return <Route path={route.path} element={element} key={route.path} />;
  });
}

function LegacyTransportadorRedirect() {
  const params = useParams();
  const rest = params['*'] ?? '';
  const normalized = rest.replace(/^\/+/, '');

  if (!normalized || normalized === 'transportador') {
    return <Navigate to="/transportador/dashboard" replace />;
  }

  return <Navigate to={`/transportador/dashboard/${normalized}`} replace />;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/cadastro" element={<Cadastro />} />
      <Route path="/pos-cadastro" element={<PosCadastro />} />
      <Route path="/cadastro/tipo" element={<CadastroTipoCliente />} />

      <Route
        path="/transportador/dashboard"
        element={
          <ProtectedRoute allowedRoles={["transportador"]}>
            <RequireAuth>
              <LayoutTransportador />
            </RequireAuth>
          </ProtectedRoute>
        }
      >
        {renderRoutes(TRANSPORTADOR_MENU_ROUTES)}
        {renderRoutes(TRANSPORTADOR_ADDITIONAL_ROUTES)}
      </Route>

      <Route
        path="/motorista/dashboard"
        element={
          <ProtectedRoute allowedRoles={["motorista"]}>
            <RequireAuth>
              <DashboardMotorista />
            </RequireAuth>
          </ProtectedRoute>
        }
      />

      <Route
        path="/revenda/dashboard"
        element={
          <ProtectedRoute allowedRoles={["revenda"]}>
            <RequireAuth>
              <DashboardRevenda />
            </RequireAuth>
          </ProtectedRoute>
        }
      />

      <Route
        path="/borracharia/dashboard"
        element={
          <ProtectedRoute allowedRoles={["borracharia"]}>
            <RequireAuth>
              <DashboardBorracharia />
            </RequireAuth>
          </ProtectedRoute>
        }
      />

      <Route
        path="/recapagem/dashboard"
        element={
          <ProtectedRoute allowedRoles={["recapagem"]}>
            <RequireAuth>
              <DashboardRecapagem />
            </RequireAuth>
          </ProtectedRoute>
        }
      />

      <Route path="/" element={<Login />} />

      <Route
        path="/hub"
        element={
          <RequireAuth>
            <HubLayout />
          </RequireAuth>
        }
      >
        <Route index element={<Navigate to="/hub/frota" replace />} />
        <Route path=":pillar" element={<PilarPage />} />
        <Route path=":pillar/:sub" element={<SubPage />} />
      </Route>

      <Route path="/dashboard" element={<Navigate to="/transportador/dashboard" replace />} />
      <Route path="/dashboard/*" element={<LegacyTransportadorRedirect />} />

      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}
