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
import urllib.error
import time 
from collections import defaultdict
import os 
import LocalitySensitiveHashing as LSH
hashseed = os.getenv('PYTHONHASHSEED')
os.environ['PYTHONHASHSEED'] = '0'
#stopwords we do at query time
#from nltk.corpus import stopwords
#stop_words = set(stopwords.words('english'))

class CrawlerThread:
    url_cache_hash = set()
    inverted_matrix = defaultdict(dict) #dict{term : dict{URLS : set(positions)}}



    def __init__(self) -> None:
        self.frontier = frontier.Frontier()
        self.robot_parser = urllib.robotparser.RobotFileParser()
    


    def _is_valid(self, current_url : urlparse) -> bool:
        #determine if the link should be crawled
        # if url.scheme not in ['http','https']: return False
        # else:
        #all things we do not want to match for now
        
        #if page is already scraped
        if current_url.geturl() in CrawlerThread.url_cache_hash: return False
       # print("PASSED1")
        #determine if its a frag
        if current_url.fragment : return False
        #print("PASSED2")
        try:
            return not re.match(
                    r".*\.(css|js|bmp|gif|jpe?g|ico\
                    |png|tiff?|mid|mp2|mp3|mp4\
                    |wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf\
                    |ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names\
                    |data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso\
                    |epub|dll|cnf|tgz|sha1\
                    |thmx|mso|arff|rtf|jar|csv\
                    |rm|smil|wmv|swf|wma|zip|rar|gz|ova|war|img|apk|java|py|json|db|txt)$", current_url.path.lower())
        except TypeError:
            return False



    def _add_to_indexer(self) -> None :
        #we deal with stopwords at query time but stemming at indexing and query 
        # we stem all indices and we stem the query and apply stopwords to the query
        #start1 = time.time()
        print(len(self.tokenized))
        print(self.current_url)
        for index, token in enumerate(self.tokenized):
            new_token = tokenizer.Tokenizer.token_conflation(token)
            #start stemming 
            stemmed_word = tokenizer.Tokenizer.stem_word(new_token)
           
            print(index, stemmed_word, "| ",end= "\r") #test prints
            #add to inverted term matrix
            #right now we are just doing positional lists and proximity matching, we could change this 

            if (not stemmed_word.isnumeric()) or ( len(stemmed_word) <= 10) :
                

                if len(stemmed_word) > 1: # if stemmed_word.is_numeric() -> if len(stemmed_word) <= 10 
                    #see if term exists
                    if self.current_url not in CrawlerThread.inverted_matrix[stemmed_word]:
                       CrawlerThread.inverted_matrix[stemmed_word][self.current_url] = [index]

                    else:
                        CrawlerThread.inverted_matrix[stemmed_word][self.current_url].append(index)
            break #TEMP
                        
                        
        print('Finished 1 article')
                       
       # start2 = time.time()
        #print("add to index : ", start2 - start1)
    


    def _extract_links(self ) -> None:
        for link in self.bs_obj.find_all('a'):
            current_crawl_link = link.get('href')
            current_crawl_urlparse = urlparse(current_crawl_link)
            #print("ALL URLS: ", current_crawl_urlparse.geturl())
            if self._is_valid(current_crawl_urlparse):
                #checking if its relative URL
                #print("ALL URLS: ", current_crawl_urlparse.geturl())
                if current_crawl_urlparse.netloc:
                    
                    self.frontier.queue.append(current_crawl_link)
                    
                else:
                    self.frontier.queue.append(urljoin(self.current_url, current_crawl_link))
                    #print("relative added: ",urljoin(self.current_url, current_crawl_link))



    def crawl(self) -> None:
   
        with open("log.txt","w") as log_file:
            count = 0 #TEMP FOR TEST
            
            while self.frontier.queue:
                self.current_url = self.frontier.dequeue()
                

                self.current_parsed = urlparse(self.current_url)
                CrawlerThread.url_cache_hash.add(self.current_parsed.geturl())
                robot_parse_url = urljoin(self.current_parsed.scheme + '://' + self.current_parsed.netloc ,  'robots.txt') 
                no_robot = False

                try:
                    self.robot_parser.set_url(robot_parse_url)
                    self.robot_parser.read()
                except (urllib.error.URLError, ValueError):

                    no_robot = True
                

                if self.robot_parser.can_fetch("*", self.current_url) or no_robot: #if it can be crawled 

                    #construct bs4 object
                    try:
                        self.bs_obj = bs4.BeautifulSoup(req.get(self.current_url).text, 'html.parser')
                    except Exception : #deal with this later
                        pass

                    #get the text
                    self.tokenized = False

                    if tokenizer.Tokenizer.check_relevance(self.bs_obj):
                        #parsing
                        self.tokenized = tokenizer.Tokenizer.tokenize(self.bs_obj.get_text())

                    if self.tokenized: #if list is empty then either it is not relevant or its empty

                        #check the simhash against the last 15 and decide whether to discard 
                        
                        self._add_to_indexer()
                        self._extract_links()
                            


                    log_file.write(f"{self.current_url}, {len(self.tokenized) if self.tokenized else self.tokenized }\n")

                    #FOR TEST --------------------
                    count += 1
                    if count >= 50 :
                        break
                    #END OF TEST ------------------
                    time.sleep(.5)





if __name__ == "__main__":
    current_crawl = CrawlerThread()
    current_crawl.crawl()


