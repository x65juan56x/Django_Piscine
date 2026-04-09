def my_var():
    int_var = 42
    str_var = '42'
    str_var2 = 'quarante-deux'
    float_var = 42.0
    bool_var = True
    list_var = [42]
    dict_var = {42: 42}
    tuple_var = (42,)
    set_var = set()

    variables = [
        int_var,
        str_var,
        str_var2,
        float_var,
        bool_var,
        list_var,
        dict_var,
        tuple_var,
        set_var,
    ]

    for variable in variables:
        print(f"{variable} has a type {type(variable)}")

if __name__ == '__main__':
    my_var()
