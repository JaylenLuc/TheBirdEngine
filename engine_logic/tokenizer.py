#get all relevant text
#get all the links
#get all the pictures -- but thats for later
#get all audio and their tags -- but thats for later
import bs4
import re
from krovetzstemmer import Stemmer
from QueryRanker import Ranker
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
    def tokenize(text : str) -> list[str]:
       
        #parsing

        unparsed_string = text.lower().replace('(',' ').replace(')',' ')

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
        
    @staticmethod
    def process_query(client_request : dict[str, str]) -> list[str] :
        print(client_request)
        #get query from 
        #tokenize
        text_query = Tokenizer.tokenize(client_request['text_query'])
        #for each token we conflate and stem
        
        for token in range(len(text_query)):
            text_query[token] = Tokenizer.stem_word(Tokenizer.token_conflation(text_query[token]))

        #here we have the modified text_qury List

        #for loop over list of terms and start ranking 

        #call retrieve_articles from Ranker
        return Ranker.vector_space_rank(text_query)

       