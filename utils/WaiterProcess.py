import threading


class WaiterProcess:
    def __init__(self, callback, delay=2.0):
        self._callback = callback
        self._delay = delay
        self._timer = None

    def set_wait(self):
        # Restart delayed callback timer
        if self._timer:
            self._timer.cancel()
        self._timer = threading.Timer(self._delay, self._callback)
        self._timer.start()

    def stop(self):
        if self._timer:
            self._timer.cancel()
