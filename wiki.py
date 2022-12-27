import requests
from spacy.lang.en import English
from bs4 import BeautifulSoup
from pprint import pprint

nlp = English()
nlp.add_pipe('sentencizer')

found = False
gods = [' god ', ' god.', ' god,', ' god?', ' god!', ' god;', ' god:', ' god"', ' god-', ' gods ']

def finder():
    r = requests.get("https://en.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=100&format=json")
    r_data = r.json()
    for item in r_data['query']['random']:
        title = item['title']
        t = requests.get("http://en.wikipedia.org/w/api.php?action=parse&prop=text&page=" + title + "&format=json")
        t_data = t.json()
        try:
            html = t_data['parse']['text']['*']
        except KeyError:
            return False
        cleaned_text = BeautifulSoup(html, 'lxml').get_text()
        stripped_text = cleaned_text.rstrip()  
        doc = nlp(stripped_text)
        sentences = [sent.text.strip() for sent in doc.sents]
        for sentence in sentences:
            if len(sentence) < 350:
                if "\n" not in sentence:
                    if any(god in sentence.lower() for god in gods):
                        print(sentence)
                        return True
        else:
            print('none')
            return False

while not found:
    found = finder()
