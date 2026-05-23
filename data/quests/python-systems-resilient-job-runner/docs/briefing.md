# Mission: Resilient Job Runner

In distributed systems, transient failures are inevitable. Network blips, database locks, and downstream rate limits can cause a task to fail temporarily. Instead of failing the entire workflow, systems use **Retry Policies** to stay resilient.

### The Backoff Strategy
Waiting a fixed amount of time between retries is rarely sufficient. Modern systems use **Exponential Backoff**—increasing the wait time after each failure to give the downstream system more time to recover and to prevent "thundering herd" issues.

### Your Objective
Implement a robust `run_with_retries` utility in `task.py`. 

You must ensure that:
1. Failed jobs are retried up to a `max_attempts` limit.
2. The sleep duration doubles after each failure (0.1s, 0.2s, 0.4s...).
3. If the final attempt fails, a custom `RetryError` is raised, preserving the original cause.
