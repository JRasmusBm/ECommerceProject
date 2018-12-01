from home.models import Users
from home.models import Orders
from home.models import Orderitems
from home.models import Product

class OrdersBackend: #TODO IF ORDER NOT PAID, UPDATE PRICE TO CURRENT

    def getOrder (self, email): #return current active order
        user = Users.objects.get(email=email)
        userOrder = Orders.objects.filter(idusers=user.idusers)
        userOrder = userOrder.filter(payment=False)
        if not userOrder.exists():
            userOrder = self.createOrder(user)
        else: userOrder = userOrder.get()
        return userOrder

    def getProducts (self, orderId): #returns the products of an order
        #try:
        i = Orderitems.objects.filter(idorders=orderId)
        p = []
        for product in i:
            p.append(product.idproduct)
        return [i, p]
        #except:
        #   return []

    def createOrder (self, user): #connect new order to user
        n = Orders.objects.all().count()
        if n != 0:
            n = Orders.objects.all()[n-1].idorders + 1
        o = Orders(idorders=n, payment=False, status=False, price=0, idusers=user)
        o.save()
        return o

    def addProduct (self, username, productId, amount): #add product to order
        user = Users.objects.get(email=username)
        product = Product.objects.get(idproduct=productId)
        userOrder = Orders.objects.filter(idusers=user.idusers)
        userOrder = userOrder.filter(payment=False)
        if not userOrder.exists():
            userOrder = self.createOrder(user.idusers)
        userItems = Orderitems.objects.filter(idproduct=productId)
        userItem = userItems.filter(idusers=user.idusers)
        if userItem.exists():
            userItem.amount = userItem.amount + 1
            userItem.save()
        else:
            userItem = Orderitems(amount=amount, idproduct=productId, idorders=userOrder.idorders, priceorderitems=product.priceproduct)
            userItem.save()
        userOrder.price = userOrder.price + (product.priceproduct * amount)
        userOrder.save()


    def removeProduct (self, orderId, productId): #remove product from order
        order = Orders.objects.filter(idOrders=orderId)
        orderProducts = Orderitems.objects.filter(idorders=orderId)
        orderProducts = orderProducts.filter(idproduct=productId) #querryset with item (if exists)
        if orderProducts.exists():
            orderProduct = orderProducts.get(idproduct=productId) #object instead of querryset
            order.price = order.price - orderProduct.priceorderitems #lower price of order with the amount of the product
            order.save()
            orderProducts.delete() #delete product
        else:
            pass

    def pay (self, orderId): #set order to payed
        order = Orders.objects.get(idOrders=orderId)
        order.payment = True
        order.save()
        
    def handle (self, orderId): #set order to handeled
        order = Orders.objects.get(idOrders=orderId)
        order.status = True
        order.save()

    def changeAmount (self, idOrders, product, amount): #change amount of a product TODO
        #lookup order from idOrders
        #
        #change the order price
        pass

    def delOrder (self, parameter_list): #Delete order TODO
        #if handeled, dont delete
        pass