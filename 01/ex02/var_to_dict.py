def get_list():
    d = [
        ('Hendrix', '1942'),
        ('Allman', '1946'),
        ('King', '1925'),
        ('Clapton', '1945'),
        ('Johnson', '1911'),
        ('Berry', '1926'),
        ('Vaughan', '1954'),
        ('Cooder', '1947'),
        ('Page', '1944'),
        ('Richards', '1943'),
        ('Hammett', '1962'),
        ('Cobain', '1967'),
        ('Garcia', '1942'),
        ('Beck', '1944'),
        ('Santana', '1947'),
        ('Ramone', '1948'),
        ('White', '1975'),
        ('Frusciante', '1970'),
        ('Thompson', '1949'),
        ('Burton', '1939')
    ]
    return d

def list_to_dict(data_list):
    data_dict = {}
    for name, year in data_list:
        if year not in data_dict:
            data_dict[year] = []
        data_dict[year].append(name)
    return data_dict

def print_dict(data_dict):
    for year in data_dict:
        names = " ".join(data_dict[year])
        print(f"{year} : {names}")

def var_to_dict():
    data_list = get_list()
    data_dict = list_to_dict(data_list)
    print_dict(data_dict)

if __name__ == '__main__':
    var_to_dict()