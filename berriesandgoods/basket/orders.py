from home.models import Users, Orders, Orderitems, Product


class OrdersBackend:  # TODO IF ORDER NOT PAID, UPDATE PRICE TO CURRENT

    def getOrder(self, email):  # return current active order
        user = Users.objects.get(email=email)
        userOrder = Orders.objects.filter(idusers=user.idusers)
        userOrder = userOrder.filter(payment=False)
        if not userOrder.exists():
            userOrder = self.createOrder(user)
        else:
            userOrder = userOrder.get()
        return userOrder

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

    def getPrice(self, orderId):
        pass

    def createOrder(self, user):  # connect new order to user
        n = Orders.objects.all().count()
        if n != 0:
            n = Orders.objects.all()[n - 1].idorders + 1
        o = Orders(
            idorders=n, payment=False, status=False, price=0, idusers=user
        )
        o.save()
        return o

    def addProduct(
        self, username, idproduct, amount
    ):  # add product to order
        user = Users.objects.get(email=username)
        product = Product.objects.get(idproduct=idproduct)
        userOrder = Orders.objects.filter(idusers=user.idusers)
        userOrder = userOrder.filter(payment=False)
        if userOrder.exists():
            userOrder = userOrder.get()
        else:
            userOrder = self.createOrder(user.idusers)
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

    def pay(self, userId):  # set order to payed
        order = Orders.objects.filter(idusers=userId)
        if order.exists():
            order = order.get()
            if Orderitems.objects.filter(idorders=order.idorders).exists:
                order.payment = True
                order.save()

    def handle(self, orderId):  # set order to handeled
        order = Orders.objects.get(idOrders=orderId)
        order.status = True
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

    def delOrder(self, parameter_list):  # Delete order TODO
        # if handeled, dont delete
        pass
