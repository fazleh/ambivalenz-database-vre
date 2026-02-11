import requests
import json
import csv


def find_dbpedia_entities(text, confidence=0.5):
    """
    Find DBpedia entities in the given text using DBpedia Spotlight API (German).

    Args:
        text (str): Input text to analyze.
        confidence (float): Confidence threshold for entity recognition.

    Returns:
        list of dict: Entities with 'surface_form', 'dbpedia_uri', and 'wikipedia_link'.
    """
    url = 'https://api.dbpedia-spotlight.org/de/annotate'
    headers = {'Accept': 'application/json'}
    params = {'text': text, 'confidence': confidence}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        resources = data.get('Resources', [])

        entities = []
        for res in resources:
            surface_form = res['@surfaceForm']
            dbpedia_uri = res['@URI']
            wikipedia_link = dbpedia_uri.replace(
                'http://dbpedia.org/resource/',
                'https://de.wikipedia.org/wiki/'
            )
            entities.append({
                'surface_form': surface_form,
                'dbpedia_uri': dbpedia_uri,
                'wikipedia_link': wikipedia_link
            })
        return entities

    except requests.RequestException as e:
        print(f"Error querying DBpedia Spotlight API: {e}")
    except (ValueError, KeyError):
        print("Error parsing response or no entities found.")
    return []


def main():
    input_file = '../data/input_1.csv'  # Input CSV file
    output_file = '../data/output_1.json'  # Output JSON file

    results = []
    try:
        with open(input_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for idx, row in enumerate(reader):
                text = row.get('Object', '').strip()
                if text:
                    print(f"Processing row #{idx + 1}: {text[:50]}...")
                    entities = find_dbpedia_entities(text)
                    results.append({
                        'text': text,
                        'entities': entities
                    })
                else:
                    print(f"Row #{idx + 1} is missing a text field.")
    except FileNotFoundError:
        print(f"Input file '{input_file}' not found.")
        return
    except KeyError:
        print(f"Column 'text' not found in '{input_file}'.")
        return

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print(f"Successfully saved results for {len(results)} texts to '{output_file}'.")
    except IOError as e:
        print(f"Error writing to output file '{output_file}': {e}")


if __name__ == '__main__':
    main()
