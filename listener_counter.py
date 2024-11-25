import threading


class ListenerCounter:
    def __init__(self) -> None:
        self.__listener = set()
        self.__lock = threading.Lock()

    def add_listener(self, listener_id: str):
        with self.__lock:
            self.__listener.add(listener_id)

    def remove_listener(self, listener_id: str):
        with self.__lock:
            self.__listener.discard(listener_id)

    def count(self) -> int:
        with self.__lock:
            return len(self.__listener)
