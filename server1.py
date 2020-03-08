# saved as server.py 
# python -m Pyro4.naming before running

import Pyro4

@Pyro4.expose
class JustHungry(object):
    categories = ["starter", "main course", "drink", "dessert"]
    products = [["salad", "starter", 4],
            ["soup", "starter", 4],
            ["salmon", "starter", 3],
            ["sandwich", "main course", 7],
            ["mac and cheese", "main course", 11],
            ["peperoni pizza", "main course", 10],
            ["coca-cola", "drink", 1],
            ["fanta", "drink", 1.3],
            ["water", "drink", 1.5],            
            ["yogurt", "dessert", 3],
            ["apple", "dessert", 2],
            ["chocolate cake", "dessert", 4]]

    orders = []
    primary = 0
    def setPrimary(self):
        self.primary = 1
    def setSlave(self):
        self.primary = 0
    def isPrimary(self):
        return self.primary
    def getCategories(self):
        return self.categories
    def getProducts(self,category):
        category_products = []
        for product in self.products:
            if product[1]==category:
                category_products.append(product)
        return category_products
    def getLastId(self):
        if len(self.orders)>0:
            print("in")
            return self.orders[len(self.orders)-1][0]
        else:
            print("here")
            return 0
    def setOrder(self,order_Id, order_list, order_price,order_time):
        self.orders.append([order_Id,order_list, order_price,order_time])
        print(self.orders)
        try:
            server = Pyro4.Proxy("PYRONAME:server2")
            server.updateOrders(self.orders)
        except:
            print("Server2 is not running")
            pass
        try:
            server = Pyro4.Proxy("PYRONAME:server3")
            server.updateOrders(self.orders)
        except:
            print("Server3 is not running")
            pass
        return "Your order has been placed"
    def getOrders(self):
        return self.orders
    
    def updateOrders(self, orders):
        try:
            self.orders.extend([order for order in orders if order not in self.orders])
            print(self.orders)
            return "ok"
        except:
            return "Error"


    # def get_fortune(self, name):
    #     return "Hello, {0}. Here is your fortune message:\n" \
    #            "Behold the warranty -- the bold print giveth and the fine print taketh away.".format(name)
    # def getmessage(self):
    #     return self.hello
    # def setmessage(self, newmessage):
    #     self.hello = newmessage
    #     server2 = Pyro4.Proxy("PYRONAME:server2")  

    #     print(server2.avg(1,2,3))
    #     print(server2.max(2,2,3))
    #     return "The value of message was changed correctly"

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(JustHungry)   # register the greeting maker as a Pyro object
ns.register("server1", uri)   # register the object with a name in the name server

print("Ready")      # print the uri so we can use it in the client later
daemon.requestLoop()                   # start the event loop of the server to wait for calls
