from flask import Flask, render_template
from datetime import datetime
import argparse, os
from collections import defaultdict, Counter

app = Flask(__name__)
LOG_PATH = None

def parse_log():
    events = []
    with open(LOG_PATH, 'r') as f:
        for line in f:
            parts     = line.strip().split(maxsplit=3)
            if len(parts) < 3:
                continue

            raw_date  = parts[0]
            raw_time  = parts[1]
            module    = parts[2].strip("[]")
            remainder = parts[3] if len(parts) == 4 else "(no details)"

            if ":" in remainder:
                level, msg = remainder.split(":", 1)
                level, desc = level.strip(), msg.strip()
            else:
                level, desc = "UNKNOWN", remainder

            try:
                dt = datetime.strptime(
                    f"{raw_date} {raw_time}",
                    "%Y-%m-%d %H:%M:%S,%f"
                )
            except ValueError:
                continue

            ms       = dt.microsecond // 1000
            readable = dt.strftime("%Y-%m-%d %H:%M:%S") + f".{ms:03d}"

            events.append({
                "time":   readable,
                "type":   level,
                "module": module,
                "desc":   desc
            })

    events.sort(key=lambda e: e["time"])
    return events

def aggregate_per_minute(events):
    # bucket events by minute
    bins = defaultdict(list)
    for e in events:
        dt     = datetime.strptime(e["time"], "%Y-%m-%d %H:%M:%S.%f")
        dt_bin = dt.replace(second=0, microsecond=0)
        bins[dt_bin].append(e)

    aggregated = []
    buckets = {}
    for idx, (dt_bin, evs) in enumerate(sorted(bins.items())):
        total      = len(evs)
        mod_counts = Counter(ev['module'] for ev in evs)
        top_mod, top_count = mod_counts.most_common(1)[0]

        aggregated.append({
            "id":      idx,
            "start":   dt_bin.isoformat(),
            "content": f"{total} ev",
            "title":   f"Total: {total} events\nTop: {top_mod} ({top_count})"
        })
        buckets[idx] = evs

    return aggregated, buckets

@app.route("/")
def index():
    events       = parse_log()
    aggregated, buckets = aggregate_per_minute(events)
    log_filename = os.path.basename(LOG_PATH)
    entry_count  = len(events)
    return render_template(
        "index.html",
        events=events,
        aggregated=aggregated,
        buckets=buckets,
        log_filename=log_filename,
        entry_count=entry_count
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--logpath",
        default="logs/analysis.log",
        help="Path to analysis.log"
    )
    args = parser.parse_args()
    LOG_PATH = args.logpath
    if not os.path.exists(LOG_PATH):
        raise FileNotFoundError(f"No such log: {LOG_PATH}")
    app.run(debug=True)
  
