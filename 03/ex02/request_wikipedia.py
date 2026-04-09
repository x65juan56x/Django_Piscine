import json
import sys
import requests
import dewiki


def fetch_wikipedia_data(search_term):
    api_url = "https://fr.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": 1,
        "redirects": 1,
        "generator": "search",
        "gsrsearch": search_term,
        "gsrlimit": 1,
        "utf8": 1
    }
    headers = {
        "User-Agent": "42-piscine-django/1.2 (educational script)"
    }

    try:
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        data = json.loads(response.text)
    except requests.RequestException as error:
        raise Exception(f"Network or server error: {error}")
    except json.JSONDecodeError:
        raise Exception("Failed to decode JSON response from the server.")

    return data


def extract_text(data):
    if 'error' in data:
        raise Exception(f"API error: {data['error'].get('info', 'Unknown error')}")

    pages = data.get('query', {}).get('pages', {})
    if not pages or "-1" in pages:
        raise Exception("No results found for the search request.")
    page_id = list(pages.keys())[0]
    try:
        raw_text = pages[page_id]['extract']
    except KeyError:
        raise Exception("Unexpected API response structure. Could not extract text.")

    clean_text = dewiki.from_string(raw_text)
    return clean_text


def save_to_file(search_term, content):
    filename = f"{search_term.replace(' ', '_')}.wiki"

    try:
        with open(filename, 'w', encoding='utf-8') as wiki_file:
            wiki_file.write(content)
    except IOError as error:
        raise Exception(f"Failed to write to file: {error}")


def request_wikipedia(search_term):
    if not search_term.strip():
        raise Exception("Search parameter cannot be empty.")

    data = fetch_wikipedia_data(search_term)
    clean_content = extract_text(data)
    save_to_file(search_term, clean_content)


if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise Exception("Usage: python3 request_wikipedia.py <search_term>")
        request_wikipedia(sys.argv[1])
    except Exception as error:
        print(error)

# python3 -m venv req_venv
# source req_venv/bin/activate
# pip3 install -r requirement.txt
