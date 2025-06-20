class DocstringRequiredMeta(type):
    """Метакласс требующий dockstring у классов"""

    def __new__(mcs, name, bases, namespaces, **kwargs):
        cls = super().__new__(mcs, name, bases, namespaces, **kwargs)

        if not cls.__doc__ or not cls.__doc__.strip():
            raise TypeError(f"Class {name} must have a docstring")

        return cls
