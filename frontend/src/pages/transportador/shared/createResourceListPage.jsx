import { useEffect, useMemo, useState } from 'react';
import api from '@/api/http';
import Loader from '@/components/Loader';
import ErrorState from '@/components/ErrorState';
import EmptyState from '@/components/EmptyState';
import DataTable from '@/components/DataTable';

function toTitle(label = '') {
  return label
    .replace(/_/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/^(.)/, (char) => char.toUpperCase())
    .replace(/\b(\w)(\w*)/g, (_, first, rest) => `${first.toUpperCase()}${rest}`);
}

function normalizeRows(payload, transformRow) {
  const baseArray = Array.isArray(payload)
    ? payload
    : payload && typeof payload === 'object'
      ? [payload]
      : [];

  return baseArray
    .filter((item) => item && typeof item === 'object')
    .map((item, index) => {
      const candidate = transformRow ? transformRow(item, index) : item;
      if (!candidate || typeof candidate !== 'object') {
        return { valor: candidate };
      }

      return Object.entries(candidate).reduce((acc, [key, value]) => {
        if (value === null || value === undefined) {
          acc[key] = '';
        } else if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') {
          acc[key] = value;
        } else {
          try {
            acc[key] = JSON.stringify(value);
          } catch (_err) {
            acc[key] = String(value);
          }
        }
        return acc;
      }, {});
    });
}

function extractErrorMessage(error, fallback) {
  if (!error) return fallback;
  if (typeof error === 'string') return error;
  const detail = error?.response?.data?.detail;
  if (typeof detail === 'string') return detail;
  if (error?.message) return error.message;
  return fallback;
}

export default function createResourceListPage({
  title,
  description = '',
  resource = '',
  endpoints = null,
  columns = [],
  emptyMessage = 'Nenhum registro encontrado.',
  transformRow,
}) {
  const endpointList = useMemo(() => {
    if (Array.isArray(endpoints) && endpoints.length > 0) {
      return endpoints;
    }

    if (resource) {
      return [
        `/api/transportador/${resource}/`,
        `/api/transportador/${resource}`,
      ];
    }

    return [];
  }, [endpoints, resource]);

  return function ResourceListPage() {
    const [state, setState] = useState({
      loading: true,
      errorMessage: '',
      rows: [],
      usedEndpoint: '',
      raw: null,
    });
    const [refreshToken, setRefreshToken] = useState(0);

    useEffect(() => {
      let cancelled = false;

      async function load() {
        if (!endpointList.length) {
          setState({
            loading: false,
            errorMessage: 'Nenhum endpoint configurado para este módulo.',
            rows: [],
            usedEndpoint: '',
            raw: null,
          });
          return;
        }

        setState((prev) => ({ ...prev, loading: true, errorMessage: '' }));

        for (const endpoint of endpointList) {
          try {
            const response = await api.get(endpoint);
            if (cancelled) return;

            const payload = response?.data?.results ?? response?.data ?? [];
            const rows = normalizeRows(payload, transformRow);

            setState({
              loading: false,
              errorMessage: '',
              rows,
              usedEndpoint: endpoint,
              raw: payload,
            });
            return;
          } catch (error) {
            if (cancelled) return;

            if (error?.response?.status === 404) {
              continue;
            }

            setState({
              loading: false,
              errorMessage: extractErrorMessage(error, 'Erro ao carregar dados.'),
              rows: [],
              usedEndpoint: endpoint,
              raw: null,
            });
            return;
          }
        }

        if (!cancelled) {
          setState({
            loading: false,
            errorMessage: 'Nenhum dos endpoints configurados retornou dados.',
            rows: [],
            usedEndpoint: '',
            raw: null,
          });
        }
      }

      load();
      return () => {
        cancelled = true;
      };
    }, [endpointList, refreshToken, transformRow]);

    const derivedColumns = useMemo(() => {
      if (columns && columns.length) {
        return columns;
      }

      const sample = state.rows.find((row) => row && typeof row === 'object' && Object.keys(row).length > 0);
      if (!sample) {
        return [];
      }

      return Object.keys(sample)
        .slice(0, 8)
        .map((key) => ({ key, label: toTitle(key) }));
    }, [columns, state.rows]);

    const handleRefresh = () => setRefreshToken((prev) => prev + 1);

    return (
      <div className="p-6 space-y-6">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="space-y-2">
            <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
            {description && <p className="text-sm text-gray-500 max-w-3xl">{description}</p>}
            {state.usedEndpoint && (
              <p className="text-xs text-gray-400">
                Fonte de dados:
                {' '}
                <code className="rounded bg-gray-100 px-1 py-0.5 text-gray-600">{state.usedEndpoint}</code>
              </p>
            )}
          </div>

          <button
            type="button"
            onClick={handleRefresh}
            className="inline-flex items-center gap-2 rounded-lg border border-blue-600 px-3 py-2 text-sm font-medium text-blue-600 hover:bg-blue-50"
          >
            Atualizar
          </button>
        </div>

        {state.loading ? (
          <Loader />
        ) : state.errorMessage ? (
          <ErrorState message={state.errorMessage} />
        ) : state.rows.length > 0 ? (
          derivedColumns.length > 0 ? (
            <DataTable columns={derivedColumns} rows={state.rows} />
          ) : (
            <pre className="max-h-[480px] overflow-auto rounded-lg bg-slate-900/90 p-4 text-xs text-slate-100">
              {JSON.stringify(state.raw ?? state.rows, null, 2)}
            </pre>
          )
        ) : (
          <EmptyState message={emptyMessage} />
        )}
      </div>
    );
  };
}
