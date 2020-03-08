# saved as client.py
import Pyro4

def connect():
    server_names =  ["server1", "server2", "server3"]
    #active_servers = []
    for name in server_names:
        try:
            server = Pyro4.Proxy("PYRONAME:%s" % name)
            print("Connecting to %s" % name)
            server.isPrimary()
            # active_servers.append(name)
            return server,name
        except:
            print("Cant connect to %s" % name)
            pass


@Pyro4.expose
class FrontEnd(object):
    last_server='hey'
    server,last_server = connect()  
    #print(last_server)

    def getCategories(self):
        server,self.last_server = connect()
        return self.server.getCategories()

    def getProducts(self, category):
        server,self.last_server = connect()
        return self.server.getProducts(category)

    def setOrder(self, order_list, order_price,order_time):
        print("last server: " + self.last_server)
        try:
            server = Pyro4.Proxy("PYRONAME:%s" % self.last_server)
            iD = server.getLastId()
            return self.server.setOrder(iD + 1 , order_list,order_price,order_time)
        except:
            # Last server not working
            print("Last server %s not working, moving to another server" % self.last_server)
            
        

        servers = ['server1','server2','server3']
        servers.remove(self.last_server)
        active = []
        for name in servers:
            try:
                server = Pyro4.Proxy("PYRONAME:%s" % name)
                active.append(server,server.getLastId())
            except:
                print("the server %s is not available either" % name)

        if len(active)==2:
            if active[0][1]>=active[1][1]:
                server = Pyro4.Proxy("PYRONAME:%s" % active[0][0])
                return self.server.setOrder(active[0][1] + 1, order_list,order_price,order_time)
            else:
                server = Pyro4.Proxy("PYRONAME:%s" % active[1][0])
                return self.server.setOrder(active[1][1]+1, order_list,order_price,order_time)
        elif len(active)==1:
            server = Pyro4.Proxy("PYRONAME:%s" % active[0][0])
            return self.server.setOrder(active[0][1]+1, order_list,order_price,order_time)
        else:
            return "No servers are active"

                
    
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
uri = daemon.register(FrontEnd)   # register the greeting maker as a Pyro object
ns.register("front_end", uri)
print("Ready")

daemon.requestLoop()      