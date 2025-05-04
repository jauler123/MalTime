#Imports
from flask import Flask, render_template
from datetime import datetime
import argparse, os
from collections import defaultdict, Counter

# Initialize Flask app
app = Flask(__name__)
LOG_PATH = None  # Will be set via command-line argument

def parse_log():
    """
    Reads the analysis log file line by line, parses timestamp, level, module, and description,
    and returns a sorted list of event dicts.
    """
    events = []
    with open(LOG_PATH, 'r') as f:
        for line in f:
            # Split into up to 4 parts: date, time, module, and remainder (level+message)
            parts = line.strip().split(maxsplit=3)
            if len(parts) < 3:
                continue  # skip malformed lines

            raw_date  = parts[0]                 # e.g. "2025-04-06"
            raw_time  = parts[1]                 # e.g. "12:34:56,789"
            module    = parts[2].strip("[]")     # e.g. "[analyzer]" -> "analyzer"
            remainder = parts[3] if len(parts) == 4 else "(no details)"

            # Split the remainder into level and message if possible
            if ":" in remainder:
                level, msg = remainder.split(":", 1)
                level = level.strip()            # e.g. "INFO"
                desc  = msg.strip()              # e.g. "Loaded module X"
            else:
                level, desc = "UNKNOWN", remainder

            # Parse the timestamp into a datetime object
            try:
                dt = datetime.strptime(
                    f"{raw_date} {raw_time}",
                    "%Y-%m-%d %H:%M:%S,%f"
                )
            except ValueError:
                continue  # skip lines with invalid timestamps

            # Convert microseconds to milliseconds, append to formatted string
            ms = dt.microsecond // 1000
            readable = dt.strftime("%Y-%m-%d %H:%M:%S") + f".{ms:03d}"

            # Append structured event
            events.append({
                "time":   readable,
                "type":   level,
                "module": module,
                "desc":   desc
            })

    # Sort events chronologically by the formatted time string
    events.sort(key=lambda e: e["time"])
    return events

def aggregate_per_minute(events):
    """
    Buckets events into 1-minute intervals, counts total events per bucket,
    determines the most common module in each bucket, and returns both:
      - aggregated: list of dicts for vis.js (id, start, content, title)
      - buckets: mapping from bucket id to the list of events in that bucket
    """
    bins = defaultdict(list)
    for e in events:
        # Parse back into datetime for bucketing
        dt     = datetime.strptime(e["time"], "%Y-%m-%d %H:%M:%S.%f")
        # Zero out seconds & microseconds to get the minute boundary
        dt_bin = dt.replace(second=0, microsecond=0)
        bins[dt_bin].append(e)

    aggregated = []
    buckets    = {}
    # Enumerate sorted minute bins
    for idx, (dt_bin, evs) in enumerate(sorted(bins.items())):
        total = len(evs)
        # Count occurrences of each module within this bucket
        mod_counts = Counter(ev['module'] for ev in evs)
        top_mod, top_count = mod_counts.most_common(1)[0]

        # Prepare the item for vis.js timeline
        aggregated.append({
            "id":      idx,
            "start":   dt_bin.isoformat(),
            "content": f"{total} ev",  # label on the timeline
            "title":   f"Total: {total} events\nTop: {top_mod} ({top_count})"  # tooltip
        })
        # Store the raw events for later lookup when a bucket is clicked
        buckets[idx] = evs

    return aggregated, buckets

@app.route("/")
def index():
    """
    Main route:
     - Parse the log
     - Aggregate into per-minute buckets
     - Render the template with both detailed events and overview data
    """
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
    # Command-line argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--logpath",
        default="logs/analysis.log",
        help="Path to analysis.log"
    )
    args = parser.parse_args()
    LOG_PATH = args.logpath

    # Ensure the log file exists
    if not os.path.exists(LOG_PATH):
        raise FileNotFoundError(f"No such log: {LOG_PATH}")

    # Start Flask -> if debug mode needed, set to "True"
    app.run(debug=False)
