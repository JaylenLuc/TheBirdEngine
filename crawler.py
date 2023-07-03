#initalize a queue of URLS (a seed) BFS
#get one url from the queue
#if a page can be crawled it will be fetched
#we must first download and parse the robot.txt
#store a text representation of the page
#extract urls from said page and add to the queue
#Queue = "frontier"

import bs4
import frontier
import urllib
import tokenizer
import re
from krovetzstemmer import Stemmer
#stopwords we do at query time
#from nltk.corpus import stopwords
#stop_words = set(stopwords.words('english'))

class CrawlerThread:

    inverted_matrix = dict() #dict{term : dict{URLS : list[positions]}}

    def __init__(self) -> None:
        self.frontier = frontier.Frontier()

    def crawl(self) -> None:
        
        while self.frontier.queue:
            current_url = self.frontier.dequeue()
            
            #look at robot file

            #construct bs4 object
            bs_obj = bs4.BeautifulSoup(current_url, 'html.parser')
            #get the text
            if tokenizer.Tokenizer.check_relevance(bs_obj):
                #parsing
                tokenized = tokenizer.Tokenizer.tokenize(bs_obj.get_text())
            else: 
                tokenized = []

            if not tokenized:
                #get all links
                self.frontier.queue.extend(bs_obj.find_all('a'))

                #we deal with stopwords at query time but stemming at indexing
                # we stem all indices and we stem the query adn apply stopwords to the query
                for index, token in enumerate(tokenized):
                    new_token = tokenizer.Tokenizer.token_conflation(token)
                    #start stemming 
                    stemmed_word = tokenizer.Tokenizer.stem_word(new_token)

                    #add to inverted term matrix
                    try:
                        CrawlerThread.inverted_matrix[stemmed_word][current_url].append(index)

                    except KeyError:
                        CrawlerThread.inverted_matrix[stemmed_word] = dict()
                        CrawlerThread.inverted_matrix[stemmed_word][current_url] = []
                        CrawlerThread.inverted_matrix[stemmed_word][current_url].append(index)


                
        






if __name__ == "__main__":
    current_crawl = CrawlerThread()


