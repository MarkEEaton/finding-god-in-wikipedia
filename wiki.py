import re
import requests
from goose3 import Goose
from mastodon import Mastodon
from spacy.lang.en import English
from spacy.tokenizer import Tokenizer

nlp = English()
nlp.add_pipe('sentencizer')
tokenizer = Tokenizer(nlp.vocab)

found = False
#gods = [' that ', ' god ', ' god.', ' god,', ' god?', ' god!', ' god;', ' god:', ' god"', ' god-', ' gods ']
g_tokens = tokenizer("gods god that")

def finder():
    r = requests.get("https://en.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=100&format=json")
    r_data = r.json()
    for item in r_data['query']['random']:
        title = item['title']
        g = Goose()
        article = g.extract("http://en.wikipedia.org/wiki/" + title)
        text = article.cleaned_text
        doc = nlp(text)
        sentences = doc.sents
        for sentence in sentences:
            s_tokens = tokenizer(sentence.text)
            #sentence.text = re.sub('\[.*?\]','', sentence.text)
            #sentence.text = re.sub('\(.*?\)','', sentence.text)
            #sentence.text = re.sub('  ',' ', sentence.text)
            #sentence.text = re.sub('\n','', sentence.text)
            if len(sentence.text) < 150:
                if any(token in s_tokens for token in g_tokens):
                    print("yes: " + sentence.text)
                    return True
                else:
                    print("no god: " + str(len(sentence.text)))
            else:
                try:
                    print("no len: " + str(len(sentence.text)))
                except:
                    pass
        return False

while not found:
    found = finder()
