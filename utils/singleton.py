from threading import Lock


def singleton(cls):
    cls.instances = None
    cls._lock = Lock()
    orig_new = cls.__new__

    def __new__(__class, *args, **kwargs):
        with __class._lock:
            if __class.instances is None:
                __class.instances = orig_new(__class, *args, **kwargs)

        return __class.instances

    cls.__new__ = __new__
    return cls
