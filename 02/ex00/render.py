import sys
import os

def validate_input(argv):
    if len(argv) != 2:
        return False, "Error: wrong number of arguments.", None
    template_path = argv[1]
    if not template_path.endswith(".template"):
        return False, "Error: file extension must be .template.", None
    if not os.path.isfile(template_path):
        return False, "Error: template file does not exist.", None
    return True, "", template_path

def render_template(template_path):
    with open("settings.py", "r", encoding="utf-8") as settings_file:
        settings_content = settings_file.read()
        exec(settings_content, globals())
    with open(template_path, "r", encoding="utf-8") as template_file:
        template_content = template_file.read()
    html_content = template_content.format(**globals())
    html_path = template_path.replace(".template", ".html")
    with open(html_path, "w", encoding="utf-8") as html_out:
        html_out.write(html_content)
    print(f"Success: {html_path} file successfully generated.")

def render():
    valid_in, message, template_path = validate_input(sys.argv)
    if not valid_in:
        print(message)
        return
    try:
        render_template(template_path)
    except Exception:
        print("Error: unable to render template")

if __name__ == '__main__':
    render()