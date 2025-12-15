import threading
import time

class MyThread(threading.Thread):
    def __init__(self, name, daemon=False):
        super().__init__(daemon=daemon)
        self.name = name

    def run(self):
        for i in range(5):
            print(f"{self.name} running {i}")
            time.sleep(1)

# Daemon thread
t1 = MyThread("DaemonThread", daemon=True)
# Non-daemon thread
t2 = MyThread("NormalThread", daemon=False)

t1.start()
t2.start()

time.sleep(2)
print("Main program exiting...")
