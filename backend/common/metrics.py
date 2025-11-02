import time, threading
from collections import defaultdict

class Metrics:
    def __init__(self):
        self.lock = threading.Lock()
        self.counters = defaultdict(int)
        self.sums = defaultdict(float)
        self.hist_buckets = [0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10]
        self.hist = defaultdict(lambda: [0]*(len(self.hist_buckets)+1))  # last bucket is +Inf

    def inc(self, key, amount=1):
        with self.lock:
            self.counters[key] += amount

    def observe(self, key, value):
        with self.lock:
            self.sums[key + "_sum"] += float(value)
            buckets = self.hist[key]
            placed = False
            for i, b in enumerate(self.hist_buckets):
                if value <= b:
                    buckets[i] += 1
                    placed = True
                    break
            if not placed:
                buckets[-1] += 1

        with self.lock:
            buckets = self.hist[key]
            placed = False
            for i, b in enumerate(self.hist_buckets):
                if value <= b:
                    buckets[i] += 1
                    placed = True
                    break
            if not placed:
                buckets[-1] += 1

    def export_prometheus(self):
        lines = []
        lines = []
        # counters
        for k, v in sorted(self.counters.items()):
            lines.append(f"# TYPE {k} counter")
            lines.append(f"{k} {v}")
        # sums
        for k, v in sorted(self.sums.items()):
            lines.append(f"# TYPE {k} gauge")
            lines.append(f"{k} {v}")
        # histograms
        for key, buckets in self.hist.items():
            total = 0
            for i, b in enumerate(self.hist_buckets + ["+Inf"]):
                c = buckets[i]
                total += c
                lines.append(f'{key}_bucket{{le="{b}"}} {c}')
            lines.append(f"{key}_count {total}")
        return "\n".join(lines) + "\n"

metrics = Metrics()

class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        start = time.time()
        resp = self.get_response(request)
        dur = time.time() - start
        path = getattr(request, "path", "unknown").replace("/", "_").strip("_")
        method = getattr(request, "method", "GET")
        status = getattr(resp, "status_code", 200)
        metrics.inc(f"http_requests_total")
        metrics.inc(f"http_requests_total_method_{method}")
        metrics.inc(f"http_responses_total_status_{status}")
        metrics.inc(f"http_responses_total_family_{int(status/100)}xx")
        metrics.observe(f"http_request_duration_seconds", dur)
        metrics.observe(f"http_request_duration_seconds_path_{path}", dur)
        return resp

        start = time.time()
        resp = self.get_response(request)
        dur = time.time() - start
        path = getattr(request, "path", "unknown").replace("/", "_").strip("_")
        method = getattr(request, "method", "GET")
        metrics.inc(f"http_requests_total")
        metrics.inc(f"http_requests_total_method_{method}")
        metrics.observe(f"http_request_duration_seconds", dur)
        metrics.observe(f"http_request_duration_seconds_path_{path}", dur)
        return resp
