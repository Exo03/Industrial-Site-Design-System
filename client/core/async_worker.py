import asyncio
from PySide6.QtCore import QObject, Signal, QRunnable, QThreadPool


class WorkerSignals(QObject):
    success = Signal(object)
    error = Signal(Exception)
    finished = Signal(object)


class AsyncWorker(QRunnable):
    def __init__(self, coro):
        super().__init__()
        self.coro = coro
        self.signals = WorkerSignals()
        self.setAutoDelete(True)

    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.coro)
            self.signals.success.emit(result)
            self.signals.finished.emit(result)
        except Exception as e:
            self.signals.error.emit(e)
            self.signals.finished.emit(None)

    @staticmethod
    def run_async(coro):
        worker = AsyncWorker(coro)
        QThreadPool.globalInstance().start(worker)
        return worker