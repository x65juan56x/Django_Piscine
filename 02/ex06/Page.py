from elements import Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br, Text


class Page:
    def __init__(self, root_node):
        self.root_node = root_node

    def __str__(self):
        if isinstance(self.root_node, Html):
            return '<!DOCTYPE html>\n' + str(self.root_node)
        return str(self.root_node)

    def write_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as out_html:
            out_html.write(str(self))

    def is_valid(self):
        return self._check_node(self.root_node)

    def _check_node(self, node):
        if not isinstance(node, (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br, Text)):
            return False
        if isinstance(node, Text):
            return True
        if isinstance(node, Html):
            if len(node.content) != 2:
                return False
            if not isinstance(node.content[0], Head) or not isinstance(node.content[1], Body):
                return False
        elif isinstance(node, Head):
            if len(node.content) != 1 or not isinstance(node.content[0], Title):
                return False
        elif isinstance(node, (Body, Div)):
            for node_content in node.content:
                if not isinstance(node_content, (H1, H2, Div, Table, Ul, Ol, Span, Text)):
                    return False
        elif isinstance(node, (Title, H1, H2, Li, Th, Td)):
            if len(node.content) != 1 or not isinstance(node.content[0], Text):
                return False
        elif isinstance(node, P):
            for node_content in node.content:
                if not isinstance(node_content, Text):
                    return False
        elif isinstance(node, Span):
            for node_content in node.content:
                if not isinstance(node_content, (Text, P)):
                    return False
        elif isinstance(node, (Ul, Ol)):
            if len(node.content) < 1:
                return False
            for node_content in node.content:
                if not isinstance(node_content, Li):
                    return False
        elif isinstance(node, Tr):
            if len(node.content) < 1:
                return False
            node_type = {type(node_content) for node_content in node.content}
            if node_type != {Th} and node_type != {Td}:
                return False

        for node_content in node.content:
            if not self._check_node(node_content):
                return False

        return True


def my_tests():
    valid_tree = Html([
        Head(Title(Text('Valid Page'))),
        Body([
            H1(Text('Hello World')),
            Div([
                Span([
                    P(Text('This paragraph is strictly inside a span.')),
                    Text('Another text in span')
                ])
            ]),
            Table([
                Tr([Th(Text('Col 1')), Th(Text('Col 2'))]),
                Tr([Td(Text('Data 1')), Td(Text('Data 2'))])
            ]),
            Ul([Li(Text('Item 1')), Li(Text('Item 2'))])
        ])
    ])
    page = Page(valid_tree)

    assert page.is_valid() == True, "Error: A perfectly valid page was marked as False!"
    print("Valid Page: OK\n")

    print("--- 2. Structural Errors ---")

    # Missing Head (Html only has Body)
    bad_html = Html([Body(H1(Text('No head')))])
    assert Page(bad_html).is_valid() == False, "Error: Html without Head should be False"

    # Head with wrong content (Rule: ONLY one Title)
    bad_head = Html([Head([Title(Text('T')), Meta()]), Body(Text('text'))])
    assert Page(bad_head).is_valid() == False, "Error: Head containing Meta should be False"
    print("Structural Errors: OK\n")

    print("--- 3. Content Errors ---")

    # H1 containing a Span instead of strict Text
    bad_h1 = Html([Head(Title(Text('T'))), Body(H1(Span(Text('Error'))))])
    assert Page(bad_h1).is_valid() == False, "Error: H1 containing Span should be False"

    # P containing a Div
    bad_p = Html([Head(Title(Text('T'))), Body(P(Div(Text('Error'))))])
    assert Page(bad_p).is_valid() == False, "Error: P containing Div should be False"
    print("Content Errors: OK\n")

    print("--- 4. Misc Rules ---")

    # Mixing Th and Td in the same Tr
    bad_tr = Html([
        Head(Title(Text('T'))), 
        Body(Table(Tr([Th(Text('Header')), Td(Text('Data'))])))
    ])
    assert Page(bad_tr).is_valid() == False, "Error: Tr mixing Th and Td should be False"

    # Empty Ul (Rule: must contain at least one Li)
    bad_ul = Html([Head(Title(Text('T'))), Body(Ul())])
    assert Page(bad_ul).is_valid() == False, "Error: Empty Ul should be False"
    print("Tricky Rules: OK\n")

    print("ALL TESTS PASSED")


if __name__ == '__main__':
    try:
        my_tests()
    except AssertionError as e:
        print(f"TEST FAILED: {e}")
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")
