
from home.models import Users
from home.models import Orders
from home.models import Orderitems
from home.models import Product

class OrdersBackend:

    def createOrder (self, userId): #connect new order to user
        o = Orders(payment=False, status=False, price=0, idusers=userId)
        o.save()
        return o

    def addProduct (self, username, productId): #add product to order
        user = Users.objects.get(email=username)
        product = Product.objects.get(idproduct=productId)
        userOrder = Orders.objects.filter(idusers=user.idusers)
        userOrder = userOrder.objects.filter(payment=False)
        if not userOrder.exists():
            userOrder = self.createOrder(user.idusers)
        userItems = Orderitems.objects.filter(idproduct=productId)
        userItem = userItems.objects.filter(idusers=user.idusers)
        if userItem.exists():
            userItem.amount = userItem.amount + 1
            userItem.save()
        else:
            userItem = Orderitems(amount=1, idproduct=productId, idorders=userOrder.idorders, priceorderitems=product.priceproduct)
            userItem.save()
        userOrder.price = userOrder.price + product.priceproduct
        userOrder.save()


    def removeProduct (self, orderId, productId): #remove product
        #lookup order with idOrders
        #remove product from orderItems
        #TODO change the order price
        pass

    def pay (self, orderId): #set order to payed
        order = Orders.objects.get(idOrders=orderId)
        order.payment = True
        order.save()
        
    def handle (self, orderId): #set order to handeled
        order = Orders.objects.get(idOrders=orderId)
        order.status = True
        order.save()

    def changeAmount (self, idOrders, product, amount): #change amount of a product
        #lookup order from idOrders
        #TODO change the order price
        pass