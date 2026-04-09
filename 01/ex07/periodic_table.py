def parse_element(line):
    
    name_side, attr_side = line.split("=")

    name = name_side.strip()
    element = {"name": name}

    attrs = attr_side.split(",")
    for attr in attrs:
        key, value = attr.split(":", 1) # The number 1: how many times the string shoud be splited
        element[key.strip()] = value.strip()

    return element

def generate_html_code(elements):
    html = [
        "<!Doctype html>",
        "<html lang=\"en\">",
        "<head>",
        "<meta charset=\"utf-8\">",
        "<title>Periodic Table</title>",
        "<style>",
        "    body { font-family: Arial, sans-serif; background-color: #2c3e50; color: #333; padding: 20px; }",
        "    table { border-collapse: collapse; margin: 0 auto; background-color: white; }",
        "    td { border: 1px solid #bdc3c7; padding: 10px; width: 100px; height: 120px; vertical-align: top; }",
        "    td.empty { border: none; background-color: transparent; }",
        "    h4 { margin: 0 0 10px 0; text-align: center; }",
        "    ul { list-style-type: none; padding: 0; margin: 0; font-size: 0.85em; }",
        "    li { margin-bottom: 4px; }",
        "    </style>",
        "</head>",
        "<body>",
        "    <table>",
        "        <tr>"
    ]

    curr_column = 0

    for element in elements:
        position = int(element.get("position", 0)) # The number 0: the fallback value
        if position < curr_column:
            html.append("        </tr>")
            html.append("        <tr>")
            curr_column = 0

        while curr_column < position:
            html.append("            <td class=\"empty\"></td>")
            curr_column += 1

        cell = [
            "            <td>",
            f"                <h4>{element['name']}</h4>",
            "                <ul>",
            f"                    <li>No {element['number']}</li>",
            f"                    <li>{element['small']}</li>",
            f"                    <li>{element['molar']}</li>",
            f"                    <li>{element['electron']} electron</li>",
            "                </ul>",
            "            </td>"
        ]
        html.extend(cell)
        curr_column += 1

    html.append("        </tr>")
    html.append("    </table>")
    html.append("</body>")
    html.append("</html>")

    return "\n".join(html)

def periodic_table():
    elements = []
    with open("periodic_table.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            element = parse_element(line)
            elements.append(element)

    full_html_code = generate_html_code(elements)
    with open("periodic_table.html", "w", encoding="utf-8") as html_file:
        html_file.write(full_html_code)

if __name__ == '__main__':
    periodic_table()