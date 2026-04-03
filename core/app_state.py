class AppState:
    app_state = None

    def __init__(self):
        self._listeners = []
        AppState.app_state = self

    def update_taskbar(self):
        self._notify()

    def subscribe(self, callback):
        self._listeners.append(callback)

    def _notify(self):
        for callback in self._listeners:
            callback()
