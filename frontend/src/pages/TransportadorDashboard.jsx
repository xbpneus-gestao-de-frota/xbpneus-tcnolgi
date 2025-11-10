import React from 'react';
import { Link } from 'react-router-dom';
import './TransportadorDashboard.css';

const tiles = [
  'frota/motoristas',
  'frota/rastreamento',
  'pneus/manutencao-pneus',
  'estoque/movimentacoes',
  'manutencao/ordens-servico',
  'financeiro/visao-geral',
  'compras/dashboard',
  'eventos/visao-geral',
  'configuracoes/visao-geral',
]; // will be replaced programmatically

export default function TransportadorDashboard() {
  const links = tiles;
  return (
    <div className="tp-dash">
      <header className="tp-dash__header">
        <h1>Dashboard do Transportador</h1>
        <p>Selecione um módulo para continuar.</p>
      </header>
      <div className="tp-dash__grid">
        {links.map((to) => (
          <Link key={to} to={to} className="tp-dash__tile">
            <div className="tp-dash__tile-title">{to}</div>
          </Link>
        ))}
      </div>
    </div>
  );
}
