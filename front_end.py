import Pyro4
import requests

def connect():
    server_names =  ["server1", "server2", "server3"]
    #active_servers = []
    active = []
    last_server = ""
    for name in server_names:
        try:
            server = Pyro4.Proxy("PYRONAME:%s" % name)
            active.append([name,server.getLastId()])
        except:
            print("the server %s is not available" % name)
            pass
    if len(active)==3:
        active_lastId = [active[0][1],active[1][1],active[2][1]]
        ind = active_lastId.index(max(active_lastId))
        last_server = server_names[ind]
    elif len(active)==2:
        if active[0][1]>=active[1][1]:
            last_server = active[0][0]
        else:
            last_server = active[1][0]
    elif len(active)==1:
        last_server = active[0][0]
    else:
        print("Error: no server is available right now")
        return "No server is running/available right now"

    server_names.remove(last_server)
    server_names = [last_server] + server_names
    for name in server_names:
        try:
            server = Pyro4.Proxy("PYRONAME:%s" % name)
            print("Connecting to %s" % name)
            print(server.isPrimary())
            return server,name
        except Exception:
            print(Exception)
            print("Cant connect to %s" % name)
            pass


@Pyro4.expose
class FrontEnd(object):
    # last_server='hey'
    server,last_server = connect()  
    #print(last_server)

    def getCategories(self):
        self.server,self.last_server = connect()
        return self.server.getCategories()

    def getProducts(self, category):
        self.server,self.last_server = connect()
        return self.server.getProducts(category)

    def setOrder(self, order_list, order_price,order_time,name,postcode):
        print("last server: " + self.last_server)
        try:
            self.server = Pyro4.Proxy("PYRONAME:%s" % self.last_server)
            iD = self.server.getLastId()
            order = self.server.setOrder(iD + 1 , order_list,order_price,order_time,name,postcode)
            return order
        except:
            # Last server not working
            print("Last server %s not working, moving to another server" % self.last_server)
            pass
        servers = ['server1','server2','server3']
        servers.remove(self.last_server)
        active = []
        for name in servers:
            try:
                self.server = Pyro4.Proxy("PYRONAME:%s" % name)
                print([name,self.server.getLastId()])
                active.append([name,self.server.getLastId()])
            except:
                print("the server %s is not available either" % name)
                pass
        if len(active)==2:
            if active[0][1]>=active[1][1]:
                self.server = Pyro4.Proxy("PYRONAME:%s" % active[0][0])
                return self.server.setOrder(active[0][1] + 1, order_list,order_price,order_time,name,postcode)
            else:
                self.server = Pyro4.Proxy("PYRONAME:%s" % active[1][0])
                return self.server.setOrder(active[1][1]+1, order_list,order_price,order_time,name,postcode)
        elif len(active)==1:
            self.server = Pyro4.Proxy("PYRONAME:%s" % active[0][0])
            return self.server.setOrder(active[0][1]+1, order_list,order_price,order_time,name,postcode)
        else:
            return "No servers are active"

                
    def checkAddress(self,postcode):
        r = requests.get('https://api.postcodes.io/postcodes/'+postcode)
        if r.json()['status'] != 200:
            return 1
        else:
            return 0
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