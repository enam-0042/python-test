from threading import Lock

def singleton(cls):
    instances = {}
    lock = Lock()
    class wrapper(cls):
        def __new__(cls, *args, **kwargs):
            with lock:
                if cls not in instances:
                    instances[cls]= super(wrapper, cls).__new__(cls, *args,**kwargs)
            return instances[cls]
    return wrapper
