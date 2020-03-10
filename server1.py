# python -m Pyro4.naming before running
import Pyro4

@Pyro4.expose
class JustHungry(object):

    # List of categories and products
    categories = ["starter", "main course", "drink", "dessert"]
    products = [["salad", categories[0] , 4],
            ["soup", categories[0], 4],
            ["salmon", categories[0], 3],
            ["sandwich", categories[1], 7],
            ["mac and cheese", categories[1], 11],
            ["peperoni pizza",categories[1], 10],
            ["coca-cola", categories[2], 1],
            ["fanta", categories[2], 1.3],
            ["water", categories[2], 1.5],            
            ["yogurt", categories[3], 3],
            ["apple", categories[3], 2],
            ["chocolate cake", categories[3], 4]]

    orders = []
    primary = 0
    def setPrimary(self):
        self.primary = 1
    def setSlave(self):
        self.primary = 0
    def isPrimary(self):
        return self.primary
    # Get method for categories
    def getCategories(self):
        return self.categories
    # Get method for products of a specific category
    def getProducts(self,category):
        category_products = []
        for product in self.products:
            if product[1]==category:
                category_products.append(product)
        return category_products
    
    # Get method for the last Id in the orders array
    def getLastId(self):
        # Check if orders is not empty
        if len(self.orders)>0:
            return self.orders[len(self.orders)-1][0]
        else:
            return 0

    # Sets an order (only used for the primary server) and then replicates the data onto the other 2 servers
    def setOrder(self,order_Id, order_list, order_price,order_time,name,postcode):
        # Sets the order
        self.orders.append([order_Id,order_list, order_price,order_time,name,postcode])
        print("An order was added")
        print(self.orders)
        # Update the other 2 servers
        try:
            server = Pyro4.Proxy("PYRONAME:server2")
            server.updateOrders(self.orders)
        except:
            print("Can't update Server2 as it is not running")
            pass
        try:
            server = Pyro4.Proxy("PYRONAME:server3")
            server.updateOrders(self.orders)
        except:
            print("Can't update Server3 as it is not running")
            pass
        return "Your order has been placed"

    # Get method for the orders
    def getOrders(self):
        return self.orders
    
    # Update orders from primary server onto a secondary one
    def updateOrders(self, orders):
        try:
            self.orders.extend([order for order in orders if order not in self.orders])
            print(self.orders)
            return "ok"
        except:
            return "Error"




daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(JustHungry)   # register the greeting maker as a Pyro object
ns.register("server1", uri)   # register the object with a name in the name server

print("Ready")      # print the uri so we can use it in the client later
daemon.requestLoop()                   # start the event loop of the server to wait for calls
