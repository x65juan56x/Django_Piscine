import random
from beverages import HotBeverage, Coffee, Tea, Chocolate, Cappuccino

class CoffeeMachine:
    def __init__(self):
        self.served = 0
        self.broken = False
    class EmptyCup(HotBeverage):
        price = 0.90
        name = "empty cup"
        def description(self):
            return "An empty cup?! Gimme my money back!"
    class BrokenMachineException(Exception):
        def __init__(self):
            super().__init__("This coffee machine has to be repaired.")
    def repair(self):
        self.served = 0
        self.broken = False
    def serve(self, beverage):
        if self.broken:
            raise CoffeeMachine.BrokenMachineException()
        self.served += 1
        if self.served > 10:
            self.broken = True
            raise CoffeeMachine.BrokenMachineException()
        if random.choice([True, False]):
            return beverage()
        return CoffeeMachine.EmptyCup()

def my_tests():
    machine = CoffeeMachine()
    beverages = [Coffee, Tea, Chocolate, Cappuccino]

    print("First round:\n")
    while True:
        try:
            print(machine.serve(random.choice(beverages)))
        except CoffeeMachine.BrokenMachineException as error:
            print(error)
            break
    print("\nMachine repairing...\n")
    machine.repair()

    print("Second round:\n")
    while True:
        try:
            print(machine.serve(random.choice(beverages)))
        except CoffeeMachine.BrokenMachineException as error:
            print(error)
            break

if __name__ == '__main__':
    try:
        my_tests()
    except Exception as error:
        print(f"Unexpected error: {error}")