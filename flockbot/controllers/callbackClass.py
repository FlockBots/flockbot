from flockbot import Callback

class CallbackClass(type):
    def __new__(metacls, name, bases, namespace, **kwargs):
        instance = type.__new__(metacls, name, bases, dict(namespace))
        instance.callbacks = {}
        for obj in namespace.values():
            callbacks = metacls.get_callbacks(obj)
            if callbacks:
                for editable, callback in callbacks.items():
                    instance.callbacks.setdefault(editable, [])\
                        .extend(callback)
        return instance

    def get_callbacks(function):
        if not hasattr(function, '_callbacks'):
            return None
        callbacks = {}
        for editable, regex in function._callbacks.items():
            callback = Callback(regex=regex, function=function)
            callbacks.setdefault(editable, [])\
                .append(callback)
        return callbacks