def numbers_in_file():
    with open("numbers.txt", "r", encoding="utf-8") as file:
        content = file.read()
    numbers = content.split(",")
    for number in numbers:
        print(number)

if __name__ == '__main__':
    numbers_in_file()