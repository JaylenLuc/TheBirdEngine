#get all relevant text
#get all the links
#get all the pictures -- but thats for later
#get all audio and their tags -- but thats for later
import bs4
import re
from krovetzstemmer import Stemmer
class Tokenizer:
    
    #our text classifier
    @staticmethod
    def check_relevance(text : bs4.BeautifulSoup) -> bool:
        #check if bird is in title 
        if text != None:
            if re.search(r'(bird|birds|avian|avians)+', text.title.string.lower() ):
                return True
            #if not in title then bird is checked for at least once in the text
            return  3 <= len(re.findall(r'(bird|birds|avian|avians)+',text.get_text().lower()))
        return False
        
        
    #should  be used to tokenize both query and html including token_conflation and stem_word
    @staticmethod
    def tokenize(text : str) -> list:
       
        #parsing

        unparsed_string = text.lower()

        return list(filter(None,re.split(r"\s|;|:|\"|\“|\”|,|-|—|\!|\?|\.\s+",unparsed_string)))
    
        #parsing leaves apotrophies and periods within words alone

    #probobly should be in for loop
    @staticmethod
    def token_conflation(token : str) -> str:
        #conflates all characters after the apotrophie and guts all periods 
        return re.sub("'", '', re.sub('\.', '', token))

    @staticmethod
    def stem_word(token : str) -> str:
        try:
            stemmer = Stemmer()
            return stemmer.stem(token)
        except UnicodeDecodeError:
            return token
         
       