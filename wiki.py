import re
import requests
from goose3 import Goose
from mastodon import Mastodon
from spacy.lang.en import English

nlp = English()
nlp.add_pipe('sentencizer')

found = False
gods = [' that ', ' god ', ' god.', ' god,', ' god?', ' god!', ' god;', ' god:', ' god"', ' god-', ' gods ']

def finder():
    r = requests.get("https://en.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=100&format=json")
    r_data = r.json()
    for item in r_data['query']['random']:
        title = item['title']
        g = Goose()
        article = g.extract("http://en.wikipedia.org/wiki/" + title)
        text = article.cleaned_text
        doc = nlp(text)
        sentences = [str(sent).strip() for sent in doc.sents]
        for sentence in sentences:
            sentence = re.sub('\[.*?\]','', sentence)
            sentence = re.sub('\(.*?\)','', sentence)
            sentence = re.sub('  ',' ', sentence)
            sentence = re.sub('\n','', sentence)
            if len(sentence) < 150:
                if any(god in sentence.lower() for god in gods):
                    print("yes: " + sentence)
                    return True
                else:
                    print("no god: " + str(len(sentence)))
            else:
                try:
                    print("no len: " + str(len(sentence)))
                except:
                    pass
        return False

while not found:
    found = finder()
