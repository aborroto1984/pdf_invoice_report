import threading
import time


class Spinner:
    """A class to create a console-based spinner for indicating ongoing actions."""

    def __init__(self, spinner_chars="|/-\\", speed=0.1):
        """Initialize the spinner with custom characters and speed."""
        self._stop_spinner = threading.Event()
        self._spinner_chars = spinner_chars
        self._speed = speed
        self.bg_thread = None

    def _spinner_task(self, action):
        """Private method to handle the spinner animation."""
        while not self._stop_spinner.is_set():
            for char in self._spinner_chars:
                print(f"\r{action}... {char}   ", end="", flush=True)
                time.sleep(self._speed)
        print(f"\r{action}... Done!   ", end="", flush=True)

    def start(self, action):
        """Start the spinner for a given action."""
        if self._stop_spinner.is_set():
            self._stop_spinner.clear()
        self.bg_thread = threading.Thread(
            target=self._spinner_task,
            args=(action,),
        )
        self.bg_thread.start()

    def stop(self):
        """Stop the spinner."""
        self._stop_spinner.set()
        self.bg_thread.join()
        self.bg_thread = None
        self._stop_spinner.clear()
