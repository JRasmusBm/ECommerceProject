from django.db.models import Max

from home.models import Orders, Orderitems, Product


class OrdersBackend:
    def newOrderItemId(self):
        """Generate a new idorderitems. return the new id"""
        raw = Orderitems.objects.all().aggregate(Max("idorderitems"))
        return raw["idorderitems__max"] + 1 if raw else 0

    def newOrderId(self):
        """Generate a new idorders. Return the new id."""
        raw = Orders.objects.all().aggregate(Max("idorders"))
        return raw["idorders__max"] + 1 if raw else 0

    def hasOrder(self, user):
        """Checks if the user has an unpaid order. Return boolean value"""
        return Orders.objects.filter(
            idusers=user.idusers, payment=False
        ).exists()

    def isEmpty(self, order):
        """Checks if the order is empty. Return boolean value"""
        return not Orderitems.objects.filter(
            idorders=order.idorders
        ).exists()

    def hasProduct(self, idorders, idproduct):
        """Checks if the order contains the product. Return boolean value"""
        return idproduct in [
            product.idproduct for product, _ in self.getProducts(idorders)
        ]

    def createOrder(self, user):
        """Create a new order for the current user. Return the order."""
        order = Orders(
            idorders=self.newOrderId(),
            payment=False,
            status=False,
            price=0,
            idusers=user,
        )
        order.save()
        return order

    def getOrCreateOrder(self, user):
        """Get the current unpaid order for the user.
        Create a new order if none exists.
        Update with current product prices.
        Return the order."""
        if self.hasOrder(user=user):
            order = Orders.objects.get(idusers=user.idusers, payment=False)
            self.updatePrices(order)
            return order
        return self.createOrder(user)

    def addProduct(self, user, idproduct, amount):
        """Add product to the user's current unpaid order. Return None"""
        order = self.getOrCreateOrder(user=user)
        if self.hasProduct(idorders=order.idorders, idproduct=idproduct):
            self.changeAmount(idproduct=idproduct, user=user, amount=amount)
        else:
            product = Product.objects.get(idproduct=idproduct)
            userItem = Orderitems(
                idorderitems=self.newOrderItemId(),
                amount=amount,
                idproduct=product,
                idorders=order,
                priceorderitems=product.priceproduct,
            )
            userItem.save()
            self.updatePrices(order)

    def getOrders(self, user):
        """Get a list of all the user's orders."""
        return list(
            Orders.objects.filter(idusers=user.idusers, price__gt=0)
        )

    def getProducts(self, idorders):
        """Get the products form an order.
           Return a list of pairs (product, orderItem)"""
        return [
            (orderItem.idproduct, orderItem)
            for orderItem in Orderitems.objects.filter(
                idorders=idorders
            ).order_by("idproduct__nameproduct")
        ]

    def getEmail(self, order):
        """Get the e-mail of the user to whom the order belongs.
        Return None"""
        user = order.user
        if user.exists() and user.count() == 1:
            user = user.get()
            return user.email

    def pay(self, user):
        """Update prices, update availability and mark the order as paid.
        Do nothing if order empty.
        Return None"""
        order = self.getOrCreateOrder(user=user)
        if not self.isEmpty(order=order):
            self.changeAvailability(order=order)
            order.payment = True
            order.save()

    def handle(self, idorders):  # set order to handeled
        """Mark the order as handled. Return None"""
        order = Orders.objects.get(idorders=idorders)
        order.status = not order.status
        order.save()

    def changeAmount(self, user, idproduct, amount):
        """Change the amount of the product. Update prices. Return None."""
        order = self.getOrCreateOrder(user)
        if self.hasProduct(order.idorders, idproduct):
            orderItem = Orderitems.objects.get(
                idorders=order.idorders, idproduct=idproduct
            )
            orderItem.amount = amount
            orderItem.save()
            self.updatePrices(order=order)

    def changeAvailability(self, order, atCheckout=True):
        """Update availabilities of products according to the contents of the
        order. Decrease if order was checked out, increase if removed.
        Return None"""
        for product, orderItem in self.getProducts(idorders=order.idorders):
            if atCheckout:
                product.availability -= orderItem.amount
            else:
                product.availability += orderItem.amount
            product.save()

    def updatePrices(self, order):
        """Update the amounts according to availability, update the prices
        of the orderItems and updatethe total price of the order.
        Return None"""
        total_price = 0
        for product, orderItem in self.getProducts(idorders=order.idorders):
            if product.availability < orderItem.amount:
                orderItem.delete()
            else:
                orderItem.priceorderitems = product.priceproduct
                total_price += product.priceproduct * orderItem.amount
                orderItem.save()
        order.price = total_price
        order.save()

    def removeOrder(self, idorders):
        """Remove order and update availability. Return None"""
        order_collection = Orders.objects.filter(idorders=idorders)
        if order_collection.exists() and order_collection.count() == 1:
            order = order_collection.get()
            self.changeAvailability(order=order, atCheckout=False)
            Orderitems.objects.filter(idorders=idorders).delete()
            order.delete()

    def removeProduct(self, user, idproduct):
        """Remove product from the user's current unpaid order.  Return None"""
        order = self.getOrCreateOrder(user=user)
        if self.hasProduct(idorders=order.idorders, idproduct=idproduct):
            orderItem = Orderitems.objects.get(
                idproduct=idproduct, idorders=order.idorders
            )
            orderItem.delete()  # delete product
            self.updatePrices(order)


ordersBackend = OrdersBackend()
