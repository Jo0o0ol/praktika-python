import threading
import time

class Stopwatch:
    def __init__(self):
        self._lock = threading.Lock()
        self._start_time = 0
        self._elapsed_time = 0
        self.is_running = False

    def start(self):
        with self._lock:
            if not self.is_running:
                self.is_running = True
                self._start_time = time.time() - self._elapsed_time
                print("Секундомер запущен.")
                threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        while self.is_running:
            elapsed = time.time() - self._start_time
            print(f"\rПрошло времени: {elapsed:.2f} сек", end="")
            time.sleep(0.1)

    def stop(self):
        with self._lock:
            if self.is_running:
                self.is_running = False
                self._elapsed_time = time.time() - self._start_time
                print(f"\nСекундомер остановлен. Общее время: {self._elapsed_time:.2f} сек")

    def reset(self):
        with self._lock:
            self._elapsed_time = 0
            self.is_running = False
            print("Секундомер сброшен.")

def main():
    stopwatch = Stopwatch()
    while True:
        command = input("\nВведите команду (start/stop/reset/exit): ").strip().lower()
        if command == "start":
            stopwatch.start()
        elif command == "stop":
            stopwatch.stop()
        elif command == "reset":
            stopwatch.reset()
        elif command == "exit":
            if stopwatch.is_running:
                stopwatch.stop()
            print("Выход из программы.")
            break
        else:
            print("Неверная команда. Попробуйте снова.")

if __name__ == "__main__":
    main()
