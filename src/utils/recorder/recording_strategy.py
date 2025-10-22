from abc import ABC, abstractmethod

class RecordingStrategy(ABC):

    @abstractmethod
    def start(self, gesture_name):
        pass

    @abstractmethod
    def stop(self):
        pass