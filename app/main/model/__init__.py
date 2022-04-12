from enum import Enum, auto


class PaymentStatus(Enum):
    INITIALIZED = auto()
    CONFIRMED = auto()
    VERIFIED = auto()
    COMPLETED = auto()
    EXPIRED = auto()
    CANCELED = auto()
    FAILED = auto()
