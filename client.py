import Pyro4
from time import gmtime, strftime
#strftime("%Y-%m-%d %H:%M:%S", gmtime())

fEnd = Pyro4.Proxy("PYRONAME:front_end")
confirmation = input("Welcome to JustHungry, do you want to order? (y/n)")
if confirmation=='y' or confirmation=='yes' or confirmation=='Y'or confirmation=='Yes':
    product = ''
    order = [[],0]
    name = input("What is your name?")
    print("Hello %s!"%name)

    while True:
    # Need retrieving throug RMI from Front-end now done localy
        categories = fEnd.getCategories()
        print("Choose a category number: (type \"quit\" to finish)")
        for i in range(len(categories)):
            print("%i. %s"%(i+1,categories[i]))
        catnum = input()
        if catnum.isdigit():
            catnum = int(catnum)
            if catnum > 0 and catnum <= len(categories):
                selected_category = categories[catnum-1]
                print("You have chosen %s"% selected_category)
                category_products = fEnd.getProducts(selected_category)
    
                print("Choose a product number: (type \"quit\" to finish)")
                for i in range(len(category_products)):
                    print("%i. %s (£%d)"%(i+1,category_products[i][0],category_products[i][2]))
                prodnum = input()
                if prodnum.isdigit():
                    prodnum = int(prodnum)
                    if prodnum > 0 and prodnum <= len(category_products):
                        selected_product = category_products[prodnum-1]
                        print("You have chosen %s for £%d"% (selected_product[0],selected_product[2]))
                        order[0].append(selected_product[0])
                        order[1] += selected_product[2]
                elif catnum == "quit":
                    break
                else:
                    print("You didnt type a number")
            else:
                print("Your category number doesnt exist, please choose one from the list")
        elif catnum == "quit":
            break
        else:
            print("You didnt type a number")

        again = input("Do you want to order something else?(y/n)")
        if again!='y' and again!='yes' and again!='Y' and again!='Yes':
            if order[0]==[]:
                print("Nothing was ordered")
                exit()
            print("Your order is:")
            for k in range(len(order[0])):
                print("%i. %s"%(k+1,order[0][k]))
            print("For the price of £%d\n" % order[1])
            orderconf = input("Is your order ok? (y/n)")
            if orderconf=='y' or orderconf=='yes' or orderconf=='Y'or orderconf=='Yes':
                #order is of the form order = [["salad","pizza","coca-cola"], 15.2]
                postcode = input("What is your postcode?")
                res = fEnd.checkAddress(postcode)
                print(res)
                while res:
                    print("Unvalid postcode (type quit to exit)")
                    
                    postcode = input("What is your postcode?")
                    res = fEnd.checkAddress(postcode)
                    if postcode == 'quit':
                        exit()
                
                print("Order registered")
                print(fEnd.setOrder(order[0],order[1],strftime("%Y-%m-%d %H:%M:%S", gmtime()),name,postcode))
                print(fEnd.getOrders())
            else:
                print("Your command was cancelled")
            break
