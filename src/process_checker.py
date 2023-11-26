import time
import threading


class ProcessChecker(threading.Thread):
    def __init__(self, process, name, application):
        super().__init__()
        self.process = process
        self.name = name
        self.application = application
        self._is_running = True

    def run(self):
        while self._is_running:
            if self.process.poll() is not None:
                self.application.close_manual(self.name)
                break

    def stop(self):
        self._is_running = False
