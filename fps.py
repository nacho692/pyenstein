import datetime


class FPS:
    def __init__(self) -> None:
        self.queue = []
        self.sum = 0

    def update(self, time_delta: datetime.timedelta) -> None:
        self.queue.append(time_delta)
        self.sum += time_delta.total_seconds()
        if len(self.queue) > 100:
            self.sum -= self.queue.pop(0).total_seconds()

    def get_fps(self) -> float:
        return 1 / (self.sum / len(self.queue))
