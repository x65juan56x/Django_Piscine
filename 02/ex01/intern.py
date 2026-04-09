class Intern:
    def __init__(self, name="My name? I’m nobody, an intern, I have no name."):
        self.Name = name
    def __str__(self):
        return self.Name
    class Coffee:
        def __str__(self):
            return "This is the worst coffee you ever tasted."
    def work(self):
        raise Exception("I’m just an intern, I can’t do that...")
    def make_coffee(self):
        return Intern.Coffee()

def my_tests():
    noname_intern = Intern()
    mark_intern = Intern("Mark")

    print(noname_intern)
    print(mark_intern)

    print(mark_intern.make_coffee())
    try:
        noname_intern.work()
    except Exception as error:
        print(error)

if __name__ == '__main__':
    try:
        my_tests()
    except Exception as error:
        print(f"Unexpected error: {error}")