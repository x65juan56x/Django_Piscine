from elem import Text, Elem

class Html(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('html', attr, content, 'double')

class Head(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('head', attr, content, 'double')

class Body(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('body', attr, content, 'double')

class Title(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('title', attr, content, 'double')

class Meta(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('meta', attr, content, 'simple')

class Img(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('img', attr, content, 'simple')

class Table(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('table', attr, content, 'double')

class Th(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('th', attr, content, 'double')

class Tr(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('tr', attr, content, 'double')

class Td(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('td', attr, content, 'double')

class Ul(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('ul', attr, content, 'double')

class Ol(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('ol', attr, content, 'double')

class Li(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('li', attr, content, 'double')

class H1(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('h1', attr, content, 'double')

class H2(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('h2', attr, content, 'double')

class P(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('p', attr, content, 'double')

class Div(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('div', attr, content, 'double')

class Span(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('span', attr, content, 'double')

class Hr(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('hr', attr, content, 'simple')

class Br(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('br', attr, content, 'simple')


def my_tests():
    print(Html())

    full_html = Html([
        Head([
            Meta(attr={'charset': 'utf-8'}),
            Title(Text('Demo')),
        ]),
        Body([
            H1(Text('Header 1')),
            H2(Text('Header 2')),
            Div([
                P(Text('Paragraph inside div.')),
                Span([Text('Span text'), P(Text('Paragraph in span'))]),
                Hr(),
                Br(),
            ]),
            Table([
                Tr([Th(Text('A'), attr={'style': 'border: 1px solid black; padding: 5px;'}),
                    Th(Text('B'), attr={'style': 'border: 1px solid black; padding: 5px;'})]),
                Tr([Td(Text('C'), attr={'style': 'border: 1px solid black; padding: 5px;'}),
                    Td(Text('D'), attr={'style': 'border: 1px solid black; padding: 5px;'})]),
            ]),
            Ul([Li(Text('u1')), Li(Text('u1'))]),
            Ol([Li(Text('o1')), Li(Text('o1'))]),
            Img(attr={'src': 'http://i.imgur.com/pfp3T.jpg'})
        ])
    ])
    print(full_html)

    hello_ground = Html([
        Head([
            Title([Text("Hello Ground!")]),
        ]),
        Body([
            H1([Text("Oh no, not again!")]),
            Img(attr={'src': 'http://i.imgur.com/pfp3T.jpg'})
        ])
    ])
    print(hello_ground)

if __name__ == '__main__':
    try:
        my_tests()
    except Exception as error:
        print(f'Unexpected error in tests: {error}')