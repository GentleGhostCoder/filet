import sys
import threading
import time

from rich.console import Console


class LoadingAnimation(threading.Thread):
    def __init__(self, title="Loading", total_width=5, bar_char="■", sleep_time=0.1, silent=False):
        threading.Thread.__init__(self)
        self.title = title
        self.total_width = total_width
        self.bar_char = bar_char
        self.sleep_time = sleep_time
        self.console = Console()
        self.position = 0
        self.position_direction = 1
        self.silent = silent
        self._stop_event = threading.Event()

    @staticmethod
    def clear_last_line():
        sys.stdout.write("\x1b[1A")  # Move the cursor up by one line
        sys.stdout.write("\x1b[2K")  # Clear the current line
        sys.stdout.flush()  # Ensure the output is updated immediately

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        if self.silent:
            return
        while not self.stopped():
            self.move()
            time.sleep(self.sleep_time)

    def move(self):
        bar = (" " * self.position) + self.bar_char + (" " * (self.total_width - self.position - 1))
        self.console.print(self.title + " " + bar, end="\r", style="bold green")
        if not (self.position + 1) % self.total_width:
            self.position_direction *= -1
        self.position += self.position_direction
