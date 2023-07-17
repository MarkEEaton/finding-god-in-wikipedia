import requests
from goose3 import Goose
from mastodon import Mastodon
from spacy.lang.en import English

nlp = English()
nlp.add_pipe('sentencizer')

found = False
gods = [' god ', ' god.', ' god,', ' god?', ' god!', ' god;', ' god:', ' god"', ' god-', ' gods ']

def finder():
    r = requests.get("https://en.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=100&format=json")
    r_data = r.json()
    for item in r_data['query']['random']:
        title = item['title']
        g = Goose()
        article = g.extract("http://en.wikipedia.org/wiki/" + title)
        text = article.cleaned_text
        doc = nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]
        for sentence in sentences:
            if len(sentence) < 150:
                if "\n" not in sentence:
                    if any(god in sentence.lower() for god in gods):
                        print(sentence)
                        return True
        else:
            print('---- none ----')
            try:
                print(sentence)
            except:
                print("no sentence")
            return False

while not found:
    found = finder()
