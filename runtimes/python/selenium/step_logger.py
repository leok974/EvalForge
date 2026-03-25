"""
EvalForge Selenium Step Logger
Provides lightweight structured step logging for Selenium quests.
Steps are emitted as a JSON sentinel to stdout at the end of execution,
which is captured by the code runner and surfaced in the run result.
"""
import json
import sys
import time


TRACE_START = "<<EVALFORGE_SELENIUM_TRACE_START>>"
TRACE_END = "<<EVALFORGE_SELENIUM_TRACE_END>>"


class SeleniumStepLogger:
    """
    Collects structured step events during a Selenium quest run.
    
    Usage:
        logger = SeleniumStepLogger()
        logger.step("navigate", "Open page: /login", url="/login")
        logger.pass_step()  # mark last step as passed
        logger.emit()       # print trace sentinel to stdout
    """

    def __init__(self):
        self._steps: list[dict] = []
        self._counter = 0
        self._current: dict | None = None

    # ------------------------------------------------------------------
    # Core API
    # ------------------------------------------------------------------

    def step(self, action: str, label: str, *, selector: str = None, url: str = None) -> None:
        """Record the start of a new step (status=started)."""
        self._counter += 1
        self._current = {
            "step": self._counter,
            "action": action,
            "label": label,
            "status": "started",
        }
        if selector:
            self._current["selector"] = selector
        if url:
            self._current["url"] = url
        self._steps.append(self._current)

    def pass_step(self) -> None:
        """Mark the current pending step as passed."""
        if self._current:
            self._current["status"] = "passed"

    def fail_step(self, error: str = "") -> None:
        """Mark the current pending step as failed, optionally with an error message."""
        if self._current:
            self._current["status"] = "failed"
            if error:
                self._current["error"] = error

    def emit(self) -> None:
        """Write the step trace sentinel to stdout for capture by the runner."""
        payload = json.dumps({"steps": self._steps})
        print(f"\n{TRACE_START}{payload}{TRACE_END}\n", flush=True)

    # ------------------------------------------------------------------
    # Context manager helpers (for use inside try/finally blocks)
    # ------------------------------------------------------------------

    @property
    def steps(self) -> list[dict]:
        return self._steps
