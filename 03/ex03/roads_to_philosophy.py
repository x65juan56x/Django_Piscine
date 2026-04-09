import sys
import requests
from bs4 import BeautifulSoup


def fetch_html(wiki_url):
    headers = {
        "User-Agent": "42-piscine-django/1.2 (educational script)"
    }
    try:
        response = requests.get(wiki_url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as error:
        raise Exception(f"Network or server error: {error}")


def get_title_and_url(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    title_tag = soup.find(id='firstHeading')
    if not title_tag:
        raise Exception("Invalid Wikipedia page format: Could not find the main title.")
    title = title_tag.text

    content = soup.find(id='mw-content-text')
    if not content:
        raise Exception("Invalid Wikipedia page format: Could not find content text.")

    parser_output = content.find(class_='mw-parser-output')
    if not parser_output:
        raise Exception("Invalid Wikipedia page format: Could not find parser output.")

    next_url = None
    for p in parser_output.find_all('p'):
        if p.find_parent('table'):
            continue

        open_parentheses = 0
        for element in p.descendants:
            if isinstance(element, str):
                open_parentheses += element.count('(') - element.count(')')
            elif element.name == 'a' and open_parentheses <= 0:
                href = element.get('href', '')
                if href.startswith('/wiki/') and ':' not in href and 'Main_Page' not in href:
                    next_url = href
                    break

        if next_url:
            break

    redirect = soup.find(class_='mw-redirectedfrom')
    redirect_title = None
    if redirect:
        a_tag = redirect.find('a')
        if a_tag:
            redirect_title = a_tag.text

    return title, next_url, redirect_title


def roads_to_philosophy(search_term):
    if not search_term.strip():
        raise Exception("Search parameter cannot be empty.")

    visited_articles = []
    formatted_term = search_term.replace(' ', '_')
    current_url = f"https://en.wikipedia.org/wiki/{formatted_term}"

    while True:
        html_content = fetch_html(current_url)
        title, next_url, redirect_title = get_title_and_url(html_content)

        if redirect_title:
            if redirect_title in visited_articles:
                print("It leads to an infinite loop !")
                break
            print(redirect_title)
            visited_articles.append(redirect_title)

        if title in visited_articles:
            print("It leads to an infinite loop !")
            break

        print(title)
        visited_articles.append(title)

        if title == 'Philosophy':
            print(f"{len(visited_articles)} roads from {search_term} to philosophy !")
            break

        if not next_url:
            print("It leads to a dead end !")
            break

        current_url = f"https://en.wikipedia.org{next_url}"


if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise Exception("Usage: python3 roads_to_philosophy.py <search_term>")
        roads_to_philosophy(sys.argv[1])
    except Exception as error:
        print(error)


# python3 -m venv philo_venv
# source philo_venv/bin/activate
# pip3 install -r requirement.txt
