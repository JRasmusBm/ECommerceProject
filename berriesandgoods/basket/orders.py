

from home.models import Orders
from home.models import Orderitems

class OrdersBackend:
    def createOrder (self, idUsers, product):
        """connect order to user and add first product"""
        """create order"""
        """add id to order"""
        """create orderitems connected to orders"""
        """add product to orderitems"""
        pass

    def addProduct (self, idOrders, product):
        """add product"""
        """lookup order from idOrders"""
        """add product to orderItems"""
        pass

    def removeProduct (self, idOrders, product):
        """remove product"""
        """lookup order from idOrders"""
        """remove product from orderItems"""
        pass

    def pay (self, idOrders):
        """set pay to true"""
        """lookup order from idOrders"""
        pass

    def handle (self, idOrders):
        """set handeled to true"""
        """lookup order from idOrders"""
        pass

    def changeAmount (self, idOrders, product, amount):
        """change amount of a product"""
        """lookup order from idOrders"""
        pass