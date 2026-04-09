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


def my_html():
    head = Head([
        Meta(attr={'charset': 'utf-8'}),
        Title(Text('Ex00: Markdown Cheatsheet.'))
    ])

    body = Body([
        H1(Text('Ex00: Markdown Cheatsheet.')),
        
        Text('{% for category, items in cheatsheet.items %}'),
        
        H2(Text('{{ category }}')),
        
        Ul([
            Text('{% for item in items %}'),
            Li(Text('{{ item|safe }}')),
            Text('{% endfor %}')
        ]),
        
        Text('{% endfor %}')
    ])

    document = Html([head, body], attr={'lang': 'en'})

    file_path = '../ex00/templates/ex00/index.html'
    #file_path = 'index.html'
    
    with open(file_path, 'w') as f:
        f.write('<!DOCTYPE html>\n' + str(document))
    
    print(f"¡Éxito! Archivo generado en {file_path}")

if __name__ == '__main__':
    try:
        my_html()
    except Exception as error:
        print(f'Unexpected error in tests: {error}')