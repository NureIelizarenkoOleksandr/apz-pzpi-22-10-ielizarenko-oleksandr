session = Session()

# Створюємо нове замовлення
order = Order(customer_id=1)
session.add(order)

# Додаємо товар
item = OrderItem(order_id=order.id, product_id=5, quantity=2)
session.add(item)

# Помилка тут може залишити order без item
session.commit()




class UnitOfWork:
    def __init__(self, session_factory):
        self.session = session_factory()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if any(args):
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
# Використання:
with UnitOfWork(Session) as uow:
    order = Order(customer_id=1)
    uow.session.add(order)

    item = OrderItem(order_id=order.id, product_id=5, quantity=2)
    uow.session.add(item)
    # commit() виконається автоматично або rollback() у разі помилки
