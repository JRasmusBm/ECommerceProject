
from home.models import Users
from home.models import Orders
from home.models import Orderitems

class OrdersBackend:

    """connect order to user and add first product"""
    def createOrder (self, idUsers):
        o = Orders(payment=false, status=false, price=0, idusers=idUsers)
        oi = Orderitems(amount=0, priceorderitems=0, idorders=order.idorders)
        o.
        oi.save()
        return o.idorders


        """add product"""
    def addProduct (self, username, product):
        user = Users.objects.get(email=username)
        userOrders = []
        for order in Orders.idusers=user.idusers:"""TODO"""
            userOrders.append(order.idOrders)

            """add product to orderItems"""
        """else:"""
            """idOrders = createOrder(idUsers)"""
            """add product to orderItems"""        
        pass


        """remove product"""
    def removeProduct (self, idOrders, product):
        """lookup order with idOrders"""
        """remove product from orderItems"""
        pass


        """set pay to true"""
    def pay (self, idOrders):
        """lookup order from idOrders"""
        pass


        """set handeled to true"""
    def handle (self, idOrders):
        """lookup order from idOrders"""
        pass


        """change amount of a product"""
    def changeAmount (self, idOrders, product, amount):
        """lookup order from idOrders"""
        pass