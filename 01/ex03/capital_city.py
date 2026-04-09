import sys

def get_dicts():
    states = {
        "Oregon" : "OR",
        "Alabama" : "AL",
        "New Jersey": "NJ",
        "Colorado" : "CO"
    }
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver"
    }
    return states, capital_cities

def print_capital(state):
    states, capital_cities = get_dicts()
    state_code = states.get(state)
    if state_code is None:
        print("Unknown state")
        return
    print(capital_cities[state_code])

def capital_city():
    if len(sys.argv) != 2:
        return
    print_capital(sys.argv[1])

if __name__ == '__main__':
    capital_city()
