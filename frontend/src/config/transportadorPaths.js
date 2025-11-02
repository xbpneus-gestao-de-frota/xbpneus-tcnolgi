export const TRANSPORTADOR_DASHBOARD_BASE = "/transportador/dashboard";

function normalizeSegment(segment) {
  return `${segment}`
    .trim()
    .replace(/^\/+/, "")
    .replace(/\/+$/, "");
}

export function transportadorPath(path = "") {
  if (!path) {
    return TRANSPORTADOR_DASHBOARD_BASE;
  }

  if (Array.isArray(path)) {
    const joined = path.filter(Boolean).map(normalizeSegment).join("/");
    return transportadorPath(joined);
  }

  const cleaned = normalizeSegment(path);
  if (!cleaned) {
    return TRANSPORTADOR_DASHBOARD_BASE;
  }

  return `${TRANSPORTADOR_DASHBOARD_BASE}/${cleaned}`;
}

export function transportadorRouteSegments(...segments) {
  return transportadorPath(segments);
}
