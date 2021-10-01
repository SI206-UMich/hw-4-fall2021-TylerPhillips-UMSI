# Tyler Phillips, tjphilly, 16588817
# Partners: Oresti Dine, Jasper Tinoco

import unittest

# The Customer class
# The Customer class represents a customer who will order from the stalls.
class Customer:
    # Constructor
    def __init__(self, name, wallet = 100):
        self.name = name
        self.wallet = wallet

    # Reload some deposit into the customer's wallet.
    def reload_money(self,deposit):
        self.wallet += deposit

    # The customer orders the food and there could be different cases
    def validate_order(self, cashier, stall, item_name, quantity):
        if not(cashier.has_stall(stall)):
            print("Sorry, we don't have that vendor stall. Please try a different one.")
        elif not(stall.has_item(item_name, quantity)):
            print("Our stall has run out of " + item_name + " :( Please try a different stall!")
        elif self.wallet < stall.compute_cost(quantity):
            print("Don't have enough money for that :( Please reload more money!")
        else:
            bill = cashier.place_order(stall, item_name, quantity)
            self.submit_order(cashier, stall, bill)

    # Submit_order takes a cashier, a stall and an amount as parameters,
    # it deducts the amount from the customer’s wallet and calls the receive_payment method on the cashier object
    def submit_order(self, cashier, stall, amount):
        # customer pay the cashier the specified amount using the receive_payment method in the cashier class (i.e., it deducts money
        # from the customer’s wallet and adds it to the stall)

        self.wallet = self.wallet - amount
        cashier.receive_payment(stall, amount)

    # The __str__ method prints the customer's information.
    def __str__(self):
        return "Hello! My name is " + self.name + ". I have $" + str(self.wallet) + " in my payment card."


# The Cashier class
# The Cashier class represents a cashier at the market.
class Cashier:

    # Constructor
    def __init__(self, name, directory =[]):
        self.name = name
        self.directory = directory[:] # make a copy of the directory


    # Whether the stall is in the cashier's directory
    def has_stall(self, stall):
        return stall in self.directory

    # Adds a stall to the directory of the cashier.
    def add_stall(self, new_stall):
        self.directory.append(new_stall)

    # Receives payment from customer, and adds the money to the stall's earnings.
    def receive_payment(self, stall, money):
        stall.earnings += money

    # Places an order at the stall.
	# The cashier pays the stall the cost.
	# The stall processes the order
	# Function returns cost of the order, using compute_cost method
    def place_order(self, stall, item, quantity):
        stall.process_order(item, quantity)
        return stall.compute_cost(quantity)

    # string function.
    def __str__(self):

        return "Hello, this is the " + self.name + " cashier. We take preloaded market payment cards only. We have " + str(sum([len(category) for category in self.directory.values()])) + " vendors in the farmers' market."

## Complete the Stall class here following the instructions in HW_4_instructions_rubric
class Stall:

    def __init__(self, name, inventory, cost = 7, earnings = 0):
        self.name = name
        self.inventory = inventory
        self.cost = cost
        self.earnings = earnings

# takes the food name and the quantity and returns True if there is enough food left in the inventory
# and False otherwise.
    def has_item(self, name, quantity):

        if name in self.inventory.keys() and self.inventory[name] >= quantity:
            return True
        else:
            return False


# takes the food name and the quantity. If the stall has enough food, it will decrease the quantity of
# that food in the inventory. Questions for you to think about: should process_order take other actions?
# If so, add it in your code.
    def process_order(self, name, quantity):
        if self.has_item(name, quantity):
            self.inventory[name] -= quantity
            self.earnings += self.cost * quantity
            print("Your order is processed! Thank you!")
        else:
            pass


# takes the food name and the quantity. It will add the quantity to the existing quantity if the item
# exists in the inventory dictionary or create a new item in the inventory dictionary with the item name as the key and the quantity as the value.
    def stock_up(self, name, quantity):
        if name in self.inventory.keys():
            self.inventory[name] += quantity
        else:
            self.inventory[name] = quantity

# Takes the quantity and returns the total for an order. Since all the foods in one stall have the
# same cost, you only need to know the quantity of food items that the customer has ordered.
    def compute_cost(self, quantity):
        return quantity * self.cost

# string function.
    def __str__(self):

        return "Hello, we are " + self.name + ". This is the current menu " + ",".join(self.inventory.keys()) + ". We charge $" + str(self.cost_per_food) + " per item. We have $" + str(self.earnings) + " in total."

class TestAllMethods(unittest.TestCase):

    def setUp(self):
        inventory = {"Burger":40, "Taco":50}
        inventory2 = {"Pizza":20, "Froyo":25}
        self.f1 = Customer("Ted")
        self.f2 = Customer("Morgan", 150)
        self.s1 = Stall("The Grill Queen", inventory, cost = 10)
        self.s2 = Stall("Tamale Train", inventory, cost = 9)
        self.s3 = Stall("The Streatery", inventory)
        self.s4 = Stall("Mamma Mias", inventory2)
        self.c1 = Cashier("West")
        self.c2 = Cashier("East")
        self.c3 = Cashier("North") # not serving any stalls
        #the following codes show that the two cashiers have the same directory
        for c in [self.c1, self.c2]:
            for s in [self.s1,self.s2,self.s3]:
                c.add_stall(s)

	## Check to see whether constructors work
    def test_customer_constructor(self):
        self.assertEqual(self.f1.name, "Ted")
        self.assertEqual(self.f2.name, "Morgan")
        self.assertEqual(self.f1.wallet, 100)
        self.assertEqual(self.f2.wallet, 150)

	## Check to see whether constructors work
    def test_cashier_constructor(self):
        self.assertEqual(self.c1.name, "West")
        #cashier holds the directory - within the directory there are three stalls
        self.assertEqual(len(self.c1.directory), 3)

	## Check to see whether constructors work
    def test_truck_constructor(self):
        self.assertEqual(self.s1.name, "The Grill Queen")
        self.assertEqual(self.s1.inventory, {"Burger":40, "Taco":50})
        self.assertEqual(self.s3.earnings, 0)
        self.assertEqual(self.s2.cost, 9)

	# Check that the stall can stock up properly.
    def test_stocking(self):
        inventory = {"Burger": 10}
        s4 = Stall("Misc Stall", inventory)

		# Testing whether stall can stock up on items
        self.assertEqual(s4.inventory, {"Burger": 10})
        s4.stock_up("Burger", 30)
        self.assertEqual(s4.inventory, {"Burger": 40})

    def test_make_payment(self):
		# Check to see how much money there is prior to a payment
        previous_custormer_wallet = self.f2.wallet
        previous_earnings_stall = self.s2.earnings

        self.f2.submit_order(self.c1, self.s2, 30)

		# See if money has changed hands
        self.assertEqual(self.f2.wallet, previous_custormer_wallet - 30)
        self.assertEqual(self.s2.earnings, previous_earnings_stall + 30)


	# Check to see that the server can serve from the different stalls
    def test_adding_and_serving_stall(self):
        c3 = Cashier("North", directory = [self.s1, self.s2])
        self.assertTrue(c3.has_stall(self.s1))
        self.assertFalse(c3.has_stall(self.s3))
        c3.add_stall(self.s3)
        self.assertTrue(c3.has_stall(self.s3))
        self.assertEqual(len(c3.directory), 3)

	# Test that computed cost works properly.
    def test_compute_cost(self):
        #what's wrong with the following statements?
        #can you correct them?
        self.assertEqual(self.s1.compute_cost(5), 50)
        self.assertEqual(self.s3.compute_cost(6), 42)

	# Check that the stall can properly see when it is empty
    def test_has_item(self):
        # Set up to run test cases

        # Test to see if has_item returns True when a stall has enough items left
        # Please follow the instructions below to create three different kinds of test cases
        
        # has_item(self, food_name, quantity)
        # Test case 1: the stall does not have this food item:
        self.s4.has_item("Burger", 2) #()
        self.assertEqual(self.s4.has_item("Burger", 2), False)
        # Test case 2: the stall does not have enough food item:
        self.s3.has_item("Burger", 50)
        self.assertEqual(self.s3.has_item("Burger", 50), False)
        # Test case 3: the stall has the food item of the certain quantity:
        self.s3.has_item("Burger", 5)
        self.assertEqual(self.s3.has_item("Burger", 5), True)

        #self.assertEqual(Teds_wallet, self.f1.wallet)

	# Test validate order
    def test_validate_order(self):

		# case 1: test if a customer doesn't have enough money in their wallet to order
        Teds_wallet = self.f1.wallet
    
        self.f1.validate_order(self.c1, self.s1, "Burger", 30) # charging the wallet, there changing the wallets balance (cashier1, first stall, item is burger, ordering 30/40-totalinventory os 40)
        self.assertEqual(Teds_wallet, self.f1.wallet) # (amount that was there before the call, the amount that is actually there now)

		# case 2: test if the stall doesn't have enough food left in stock
        self.f1.validate_order(self.c1, self.s1, "Burger", 1000) #charging the wallet, there changing the wallets balance (cashier1, first stall, item is burger, ordering 1000/40-totalinventory os 40 - ordering more than the inventory allows)
        self.assertEqual(Teds_wallet, self.f1.wallet) # (amount that was there before the call, the amount that is actually there now)

		# case 3: check if the cashier can order item from that stall
        #self.assertFalse(self.f2.validate_order(self.c1, s5, "Burger", 10))
        self.f1.validate_order(self.c3, self.s1, "Burger", 5) #charging the wallet, there changing the wallets balance (cashier3, first stall- assigned no stalls above, could have, item is burger, ordering 30/40-totalinventory os 40)
        self.assertEqual(Teds_wallet, self.f1.wallet) # (amount that was there before the call, the amount that is actually there now)

    # Test if a customer can add money to their wallet
    def test_reload_money(self):
        Teds_wallet = self.f1.wallet
        self.f1.reload_money(50)

        new_amount_in_wallet = 50 + Teds_wallet
        self.assertEqual(new_amount_in_wallet, self.f1.wallet)
        
### Write main function
def main():
    #Create different objects
    inventory3 = {"Grilled Cheese": 5, "Toast": 20, "Jam Packets": 50}
    inventory4 = {"Donut": 13, "Dove Bar":10, "Orange pop": 15}

    f11 = Customer("Uncle Billy", 75)
    f12 = Customer("Mr. Sleepy", 10)
    f13 = Customer("Molly", 60)

    s3 = Stall("The Place", inventory3, 10) #s5
    s4 = Stall("The Big Ol' Building", inventory4, 15) #s6

    c4 = Cashier("South") # cashier 4 is not assigned any stalls on purpose.
    c5 = Cashier("Northwest", [s3])
    c6 = Cashier("Bloopy", [s4])

    #Try all cases in the validate_order function
    #Below you need to have *each customer instance* try the four cases

    # validate_order(cashier, stall, item_name, quantity)
    # inventory = {"Burger":40, "Taco":50} - is a dictionary from setup, so all inventory.keys() are dictionaries looking at the keys.

    #case 1: the cashier does not have the stall
    print('\n')
    f11.validate_order(c4, s3, "Grilled Cheese", 1) #(cashier4, 3rd stall, item-key is "Grilled Cheese", ordering 1/40-totalinventory os 40)
    f12.validate_order(c4, s3, "Toast", 1)
    f13.validate_order(c4, s3, "Jam Packets", 1)

    #case 2: the casher has the stall, but not enough ordered food or the ordered food item
    print('\n')
    f11.validate_order(c5, s3, "Burger", 30) #(cashier1, first stall, item is burger, ordering 30/40-totalinventory os 40)
    f12.validate_order(c5, s3, "Burger", 30)
    f13.validate_order(c5, s3, "Burger", 30)
    #case 3: the customer does not have enough money to pay for the order:
    print('\n')
    f11.validate_order(c6, s4, "Dove Bar", 8)
    f12.validate_order(c6, s4, "Dove Bar",1)
    f13.validate_order(c5, s3, "Jam Packets", 10)
    #case 4: the customer successfully places an order
    print('\n')
    f11.validate_order(c6, s4, "Donut", 1) #(cashier1, first stall, item is burger, ordering 30/40-totalinventory os 40)
    f12.validate_order(c5, s3, "Grilled Cheese", 1)
    f13.validate_order(c6, s4, "Orange pop", 1)
    print('\n')

if __name__ == "__main__":
	main()
	print("\n")
	unittest.main(verbosity = 2)
