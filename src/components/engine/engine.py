class PrintDecoratorMeta(type):
    def __new__(mcs, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and attr_name[0] != '_':
                def callback_decorator(self, *args, func=attr_value, func_name=attr_name, **kwargs):
                    if func_name in self._callbacks_before.keys():  # attr_name[0] != '_' and
                        for i in self._callbacks_before[func_name]:
                            i(self, *args, **kwargs)
                    # print(f"Calling {func_name} with args: {args}, kwargs: {kwargs}")
                    ret = func(self, *args, **kwargs)
                    if func_name in self._callbacks_after.keys():  # attr_name[0] != '_' and
                        for i in self._callbacks_after[func_name]:
                            i(self, *args, result=ret, **kwargs)
                    return ret

                attrs[attr_name] = callback_decorator
        return super(PrintDecoratorMeta, mcs).__new__(mcs, name, bases, attrs)


class AbstractEngine(metaclass=PrintDecoratorMeta):
    def __init__(self):
        self._callbacks_before = {}
        self._callbacks_after = {}

    def register_callback_before(self, name, callback):
        if name not in self._callbacks_before.keys():
            self._callbacks_before[name] = []
        self._callbacks_before[name].append(callback)

    def unregister_callback_before(self, name, callback):
        if name not in self._callbacks_before.keys():
            return
        self._callbacks_before[name].remove(callback)

    def register_callback_after(self, name, callback):
        if name not in self._callbacks_after.keys():
            self._callbacks_after[name] = []
        self._callbacks_after[name].append(callback)

    def unregister_callback_after(self, name, callback):
        if name not in self._callbacks_after.keys():
            return
        self._callbacks_after[name].remove(callback)


class MainEngine(AbstractEngine):

    def __init__(self) -> None:
        super().__init__()

    def foo(self, a):
        print(f"{a=}")

    def goo(self):
        print(f"d")


if __name__ == '__main__':
    engine = MainEngine()
    engine.goo()
    engine.register_callback_after("goo", lambda *args, result, **kwargs: print(result))
    engine.goo()
