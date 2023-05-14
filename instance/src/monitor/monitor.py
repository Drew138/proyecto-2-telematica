class Monitor:
    load: int = 15

    @classmethod
    def set_metric(cls, metrics: int) -> None:
        cls.load: int = metrics

    @classmethod
    def get_metric(cls) -> int:
        return cls.load

