## 2024-09-30 - GitHub API Rate Limit Optimization
**Learning:** Making concurrent requests to the GitHub API (e.g., via ThreadPoolExecutor) can trigger secondary rate limits (403 Forbidden) and cause silent data loss. Fetching commit data for all repositories unconditionally scales poorly with the number of repositories.
**Action:** Optimize API usage by applying data filtering locally before making requests. Checking `pushed_at` timestamps allows us to skip commit queries for repositories that haven't been updated recently, preventing throttling and speeding up the overall execution.
