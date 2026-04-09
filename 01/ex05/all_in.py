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

def dicts_lookup(states, capital_cities):
    state_lookup = {}
    capital_lookup = {}
    for state, state_code in states.items():
        capital_city = capital_cities.get(state_code)
        if capital_city:
            state_lookup[state.lower()] = (state, capital_city)
            capital_lookup[capital_city.lower()] = (state, capital_city)
    return state_lookup, capital_lookup

def clear_expressions(arg_str):
    expressions = arg_str.split(",")
    cleaned_expressions = []
    for expr in expressions:
        clean_expr = " ".join(expr.split())
        if not clean_expr:
            continue
        cleaned_expressions.append(clean_expr)
    return cleaned_expressions

def check_and_print(cleaned_expressions, state_lookup, capital_lookup):
    for clean_expr in cleaned_expressions:
        lower_expr = clean_expr.lower()
        if lower_expr in state_lookup:
            found_state, found_city = state_lookup[lower_expr]
            print(f"{found_city} is the capital of {found_state}")
        elif lower_expr in capital_lookup:
            found_state, found_city = capital_lookup[lower_expr]
            print(f"{found_city} is the capital of {found_state}")
        else:
            print(f"{clean_expr} is neither a capital city nor a state")

def all_in():
    if len(sys.argv) != 2:
        return
    states, capital_cities = get_dicts()
    state_lookup, capital_lookup = dicts_lookup(states, capital_cities)
    cleaned_expressions = clear_expressions(sys.argv[1])
    check_and_print(cleaned_expressions, state_lookup, capital_lookup)

if __name__ == '__main__':
    all_in()
