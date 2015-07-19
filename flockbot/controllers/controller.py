from flockbot import Callback
from functools import partial

class ControllerMeta(type):
    def __new__(cls, name, bases, namespace, **kwargs):
        instance = type.__new__(cls, name, bases, dict(namespace))
        instance.callbacks = {}
        for obj in namespace.values():
            callbacks = Controller.get_callbacks(instance, obj)
            if callbacks:
                for editable, callback in callbacks.items():
                    instance.callbacks.setdefault(editable, [])\
                        .extend(callback)
        return instance
    def get_callbacks(instance, function):
        if not hasattr(function, '_callbacks'):
            return None
        callbacks = {}
        for editable, regices in function._callbacks.items():
            for regex in regices:
                function = partial(function, instance) # Pass the instance as self to the function
                callback = Callback(regex=regex, function=function)
                callbacks.setdefault(editable, [])\
                    .append(callback)
        return callbacks