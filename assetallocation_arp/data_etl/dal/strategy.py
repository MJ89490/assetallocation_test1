class Strategy:
    def __init__(self, name: str):
        self._name = name
        self._description = ''
        self._version = None  # TODO check if valid case for None

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, x):
        self._description = x

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, x):
        self._version = x
