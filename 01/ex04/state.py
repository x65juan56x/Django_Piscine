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

def print_state(capital_city):
    states, capital_cities = get_dicts()
    state_from_code = {}
    for state in states:
        state_code = states[state]
        state_from_code[state_code] = state
    found_code = None
    for looking_state_code in capital_cities:
        if capital_cities[looking_state_code] == capital_city:
            found_code = looking_state_code
            break
    if found_code is None:
        print("Unknown capital city")
        return
    print(state_from_code[found_code])

def state_by_cap():
    if len(sys.argv) != 2:
        return
    print_state(sys.argv[1])

if __name__ == '__main__':
    state_by_cap()
