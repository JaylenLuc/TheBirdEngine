#get all relevant text
#get all the links
#get all the pictures -- but thats for later
import bs4
import re
from nltk.corpus import stopwords
class Tokenizer:

    stop_words = set(stopwords.words('english'))

    @staticmethod
    def check_relevance(text : bs4.BeautifulSoup) -> bool:
        #check if bird is in title 
        if re.search(r'(bird|birds|avian|avians)+', text.title.string.lower() ):
            return True

        return re.search(r'(bird|birds|avian|avians)+',text.get_text().lower())
        
        
    
    @staticmethod
    def tokenize(text : bs4.BeautifulSoup) -> list:
        if Tokenizer.check_relevance(text):
            #parsing
            unparsed_tokens = text.get_text().lower().split()
        



            pass
        else: return []