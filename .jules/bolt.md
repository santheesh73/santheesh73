## 2024-03-24 - Python Script I/O Optimization
**Learning:** `scripts/update_streak.py` sequentially fetched data from two external endpoints (GitHub GraphQL and a custom SVG renderer). These blocking network requests constituted the main execution time bottleneck of the script.
**Action:** Always identify sequential blocking I/O calls (e.g. `urllib.request`) in maintenance scripts and wrap them in a `concurrent.futures.ThreadPoolExecutor` when they are independent of each other.
