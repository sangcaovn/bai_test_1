from app.main import db
from app.main.model.product import Product
from app.main.model.order import Order

def add_new_order(order_id, user_id, quantity, subtotal_ex_tax, tax_total, total):
    order = Order.query.filter_by(user_id=user_id).first()
    if not order:
        new_order = Order(
            order_id = order_id,
            user_id = user_id,
            quantity = quantity,
            subtotal_ex_tax = subtotal_ex_tax,
            tax_total = tax_total,
            total = total,
        )
        save_changes(new_order)
        response_object = {
            'status': 'success',
            'message': 'successfully add new order.',
            'order': {
                "order_id" : new_order.order_id,
                "user_id" : new_order.user_id,
                "quantity" : new_order.quantity,
                "subtotal_ex_tax" : new_order.subtotal_ex_tax,
                "tax_total" : new_order.tax_total,
                "total" : new_order.total
            }
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Product name already exists.',
        }
        return response_object, 409

def save_changes(data: Order):
    db.session.add(data)
    db.session.commit()