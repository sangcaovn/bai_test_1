import enum


class TypeEnum(enum.Enum):
    Order = "order"
    Cart = "cart"
    OrderDetail = "order-detail"
    CartItem = "cart-item"