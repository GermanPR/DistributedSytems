# saved as client.py
import Pyro4

def connect():
    server_names =  ["server1", "server2", "server3"]
    prim_servers = []
    active_servers = []
    orders = []
    print("here")
    if 1:
        print("onto")
    for name in server_names:
        try:
            server = Pyro4.Proxy("PYRONAME:%s" % name)
            print("Connected to %s" % name)
            print(server.isPrimary())            
            if server.isPrimary():
                print("+1")
                prim_servers.append(name)
            else:
                active_servers.append(name)
            # active_servers.append(name)
            # return server
        except:
            pass
    print(prim_servers)
    if len(prim_servers)>1:
        for name in prim_servers:
            server = Pyro4.Proxy("PYRONAME:%s" % name)
            orders.append(server.getOrders())
        biggest = 0
        for i in range(len(orders)):
            if len(orders[i])>len(orders[biggest]):
                biggest = i
        server = Pyro4.Proxy("PYRONAME:%s" % prim_servers[biggest])
        server.setPrimary()
    elif len(prim_servers)==1:
        server = Pyro4.Proxy("PYRONAME:%s" % prim_servers[0])
        server.setPrimary()
    else:       
        for name in active_servers:
            try:
                server = Pyro4.Proxy("PYRONAME:%s" % name)
                orders.append(server.getOrders())
            except:
                pass
        biggest = 0
        print(orders)
        for i in range(len(orders)):
            if len(orders[i])>len(orders[biggest]):
                biggest = i
        server = Pyro4.Proxy("PYRONAME:%s" % active_servers[biggest])
        server.setPrimary()
        print("Connected to %s" % name)
        print(server.isPrimary())

    print(server)
    return server
    


    # if len(active_servers)>0:
    #     for i in range(len(active_servers)):
    #         if i==0:
    #             server = Pyro4.Proxy("PYRONAME:%s" % active_servers[i])
    print("done")

@Pyro4.expose
class JustHungry(object):
    server = connect()  
    def getCategories(self):
        server = connect()
        return self.server.getCategories()

    def getProducts(self, category):
        server = connect()
        return self.server.getProducts(category)

    def setOrder(self, order_list, order_price):
        server = connect()
        return self.server.setOrder(order_list,order_price)
    
    def getOrders(self):
        #server = connect()
        return self.server.getOrders()

# uri1 = input("What is the Pyro uri of server1 ? ").strip()
# uri2 = input("What is the Pyro uri of server2 ? ").strip()
# # name = input("What is your name? ").strip()

# greeting_maker = Pyro4.Proxy(uri)         # get a Pyro proxy to the greeting object
# print(greeting_maker.get_fortune(name))   # call method normally

# server1 = Pyro4.Proxy("PYRONAME:server1") 
# server2 = Pyro4.Proxy("PYRONAME:server2")  

# print(server1.getmessage())
# print(server1.setmessage("newmessage"))
# print(server1.getmessage())


# print(server2.avg(1,2,3))
# print(server2.max(2,2,3))
daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(JustHungry)   # register the greeting maker as a Pyro object
ns.register("front_end", uri)
print("Ready")

daemon.requestLoop()      