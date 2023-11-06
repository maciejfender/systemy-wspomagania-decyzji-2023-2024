import functools

from components.engine.engineUtils import CheckData


class PrintDecoratorMeta(type):
    def __new__(mcs, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and attr_name[0] != '_':
                @functools.wraps(attr_value)
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


class Triggerable(metaclass=PrintDecoratorMeta):
    def __init__(self):
        self._callbacks_before = {}
        self._callbacks_after = {}

    def register_callback_before(self, name, callback):
        name = name.__name__
        if name not in self._callbacks_before.keys():
            self._callbacks_before[name] = []
        self._callbacks_before[name].append(callback)

    def unregister_callback_before(self, name, callback):
        name = name.__name__
        if name not in self._callbacks_before.keys():
            return
        self._callbacks_before[name].remove(callback)

    def register_callback_after(self, name, callback):
        name = name.__name__
        if name not in self._callbacks_after.keys():
            self._callbacks_after[name] = []
        self._callbacks_after[name].append(callback)

    def unregister_callback_after(self, name, callback):
        name = name.__name__
        if name not in self._callbacks_after.keys():
            return
        self._callbacks_after[name].remove(callback)


class Engine(Triggerable):

    def __init__(self, main_window) -> None:
        super().__init__()
        self.main_window = main_window
        self.dataset = None

        # self.register_callback_after(self.set_dataset, self.main_window.footer.update_view)

    def set_dataset(self, x):
        self.dataset = x

    def read_data_excel(self):
        CheckData(self.main_window, self.set_dataset).mainloop()
