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
import urllib.robotparser
from urllib.parse import urlparse, urljoin
import tokenizer
import re
import requests as req
from krovetzstemmer import Stemmer
#stopwords we do at query time
#from nltk.corpus import stopwords
#stop_words = set(stopwords.words('english'))

class CrawlerThread:

    inverted_matrix = dict() #dict{term : dict{URLS : set(positions)}}

    def __init__(self) -> None:
        self.frontier = frontier.Frontier()
        self.robot_parser = urllib.robotparser.RobotFileParser()

    def crawl(self) -> None:
        _previous_domain = ""
        with open("log.txt","w") as log_file:
             
            while self.frontier.queue:
                current_url = self.frontier.dequeue()
                current_parsed = urlparse(current_url)
                current_domain = current_parsed.netloc
                #look at robot file
                if _previous_domain != current_domain:
                    self.robot_parser.set_url(urljoin(current_parsed.scheme + '://' + current_parsed.netloc ,  'robots.txt') )
                    
                    self.robot_parser.read()
                    _previous_domain = current_domain # str
                

                if self.robot_parser.can_fetch("*", current_url): #if it can be crawled 

                    #construct bs4 object
                    bs_obj = bs4.BeautifulSoup(req.get(current_url).text, 'html.parser')
                    #get the text
                    if tokenizer.Tokenizer.check_relevance(bs_obj):
                        #parsing
                        tokenized = tokenizer.Tokenizer.tokenize(bs_obj.get_text())
                    else: 
                        tokenized = [] 

                    if tokenized: #if list is empty then either it is not relevant or its empty
                        #get all links

                        #make sure to get the absolute URL using urllib somehow 
                        #what u do : combine the current_url with the relative 
                        self.frontier.queue.extend([link.get('href') for link in bs_obj.find_all('a')])

                        #we deal with stopwords at query time but stemming at indexing and query 
                        # we stem all indices and we stem the query and apply stopwords to the query
                        for index, token in enumerate(tokenized):
                            new_token = tokenizer.Tokenizer.token_conflation(token)
                            #start stemming 
                            stemmed_word = tokenizer.Tokenizer.stem_word(new_token)

                            #add to inverted term matrix
                            #right now we are just doing positional lists and proximity matching, we could change this 
                            if len(stemmed_word) > 0:
                                try:
                                    CrawlerThread.inverted_matrix[stemmed_word][current_url].append(index)

                                except KeyError:

                                    CrawlerThread.inverted_matrix[stemmed_word] = dict()
                                    CrawlerThread.inverted_matrix[stemmed_word][current_url] = list()
                                    CrawlerThread.inverted_matrix[stemmed_word][current_url].append(index)

                        log_file.write(f"{current_url}, {len(tokenized)}\n")






if __name__ == "__main__":
    current_crawl = CrawlerThread()
    current_crawl.crawl()


