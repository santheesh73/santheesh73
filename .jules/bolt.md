## 2024-05-15 - Concurrent GitHub API Rate Limiting
**Learning:** Using `concurrent.futures` to speed up GitHub API calls causes silent data loss because requests get rate-limited (403 Forbidden). The script's `except Exception: pass` swallows the errors, causing missing commits and incorrect streak calculations.
**Action:** Instead of concurrency, safely optimize by adding an early return / skip condition (e.g., checking `pushed_at` date) to avoid unnecessary API requests entirely.
