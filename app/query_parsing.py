import spacy

# Load spaCy English model (ensure you've downloaded with: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

def extract_entities(query: str) -> dict:
    """
    Extracts entities such as AGE, GENDER, LOCATION, DATE, etc. from user query.
    You can customize based on your domain.

    Returns:
        dict: A dictionary of extracted entity type to value.
    """
    doc = nlp(query)
    entities = {}

    for ent in doc.ents:
        entities[ent.label_] = ent.text

    # Custom rules: Insurance specific fields (age, gender, etc.)
    query_lower = query.lower()
    if 'male' in query_lower or 'm,' in query_lower or 'm ' in query_lower:
        entities['GENDER'] = 'male'
    elif 'female' in query_lower or 'f,' in query_lower or 'f ' in query_lower:
        entities['GENDER'] = 'female'

    # Very naive age parsing, improve as needed
    import re
    match = re.search(r'(\d{2})[\s-]*year', query_lower)
    if match:
        entities['AGE'] = int(match.group(1))
    elif re.match(r'\d{2}[MF]', query.replace(" ", "")):
        # e.g. '46M'
        raw = query.replace(" ", "")
        age = raw[:2]
        entities['AGE'] = int(age)
        sex = raw[2]
        entities['GENDER'] = 'male' if sex == 'M' else 'female'
    
    return entities

# Example usage:
if __name__ == "__main__":
    test_query = "46-year-old male, knee surgery in Pune, 3-month-old insurance policy"
    print(extract_entities(test_query))
