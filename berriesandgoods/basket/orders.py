from home.models import Users, Orders, Orderitems, Product


class OrdersBackend:  # TODO IF ORDER NOT PAID, UPDATE PRICE TO CURRENT
    
    def getOrders(self, user):  # return list of users orders
        userOrders = Orders.objects.filter(idusers=user.idusers, price__gt=0) #wont return empty order
        orders = []
        for order in userOrders:
            orders.append(order)
        return orders

    def getProducts(self, orderId):  # returns the products of an order
        i = Orderitems.objects.filter(idorders=orderId)
        o = []
        p = []
        if i.exists():
            for product in i:
                p.append(product.idproduct)
                o.append(product)
            return [p, o]
        return [p, o]

    def createOrder(self, user):  # connect new order to user
        n = Orders.objects.all().count()
        if n != 0:
            n = Orders.objects.all()[n - 1].idorders + 1
        o = Orders(
            idorders=n, payment=False, status=False, price=0, idusers=user
        )
        o.save()
        return o
    
    def getOrCreateOrder(self, user):
        if not Orders.objects.filter(idusers=user.idusers, payment=False).exists():
            return self.createOrder(user)
        return Orders.objects.get(idusers=user.idusers, payment=False)

    def addProduct(
        self, username, idproduct, amount
    ):  # add product to order
        user = Users.objects.get(email=username)
        product = Product.objects.get(idproduct=idproduct)
        userOrder = self.getOrCreateOrder(user)
        userItems = Orderitems.objects.filter(idproduct=idproduct)
        userItem = userItems.filter(idorders=userOrder.idorders)
        if userItem.exists():
            userItem = userItem.get()
            userItem.amount = userItem.amount + amount
            userItem.save()
        else:
            n = Orderitems.objects.all().count()
            if n != 0:
                n = Orders.objects.all()[n - 1].idorders + 1
            userItem = Orderitems(
                idorderitems=n,
                amount=amount,
                idproduct=Product.objects.get(idproduct=idproduct),
                idorders=userOrder,
                priceorderitems=product.priceproduct,
            )
            userItem.save()
        userOrder.price = userOrder.price + (product.priceproduct * amount)
        userOrder.save()

    def removeProduct(self, idproduct):  # remove product from order
        product = Orderitems.objects.filter(idorderitems=idproduct)
        if product.exists():
            product = product.get()
            order = Orders.objects.get(idorders=product.idorders.idorders)
            order.price = order.price - (
                product.priceorderitems * product.amount
            )  # lower price of order with the amount of the product
            order.save()
            product.delete()  # delete product
        else:
            pass

    def pay(self, userId):  # set order to paid
        order = Orders.objects.filter(idusers=userId, payment=False)
        if order.exists():
            order = order.get()
            if Orderitems.objects.filter(idorders=order.idorders).exists():
                order.payment = True
                order.save()

    def handle(self, orderId):  # set order to handeled
        order = Orders.objects.get(idorders=orderId)
        order.status = not order.status
        order.save()

    def changeAmount(self, idproduct, amount):  # change amount of a product
        product = Orderitems.objects.filter(idorderitems=idproduct)
        if product.exists():
            product = product.get()
            order = Orders.objects.get(idorders=product.idorders.idorders)
            order.price = order.price - (
                product.priceorderitems * product.amount
            )  # remove price of orderitem amount
            product.amount = amount
            product.priceorderitems = Product.objects.get(
                idproduct=product.idproduct.idproduct
            ).priceproduct  # update orderitem price
            order.price = order.price + (
                product.priceorderitems * amount
            )  # add new price of orderitem amount
            order.save()
            product.save()
        pass

    def removeOrder(self, idorders):  # Delete order
        order = Orders.objects.filter(idorders=idorders)
        if order.exists() and order.count() == 1:
            order = order.get()
            Orderitems.objects.filter(idorders=idorders).delete()
            order.delete()
    
    def getHandeled(self, idorders):
        order = Orders.objects.filter(idorders=idorders)
        if order.exists() and order.count() == 1:
            order = order.get()
            if order.status == True:
                return "Handeled"
            else:
                return "Not Handeled"
        pass
    
    def getPaid(self, idorders):
        order = Orders.objects.filter(idorders=idorders)
        if order.exists() and order.count() == 1:
            order = order.get()
            if order.payment == True:
                return "Paid"
            else:
                return "Not Paid"
        pass

    def getEmail(self, order):
        user = order.user
        if user.exists() and user.count() == 1:
            user = user.get()
            return user.email

