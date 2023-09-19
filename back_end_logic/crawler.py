#initalize a queue of URLS (a seed) BFS
#get one url from the queue
#if a page can be crawled it will be fetched
#we must first download and parse the robot.txt
#store a text representation of the page
#extract urls from said page and add to the queue
#Queue = "frontier"
import os 
import sys

import urllib
import urllib.robotparser
import urllib.error
import requests as req
from urllib.parse import urlparse, urljoin


from collections import defaultdict
from collections import OrderedDict
import json
import re
import time 

import  LocalitySensitiveHashing as LSH
import bs4
import frontier
import tokenizer
from krovetzstemmer import Stemmer
from pympler import asizeof
from pathlib import Path
import pymongo as mongo

hashseed = os.getenv('PYTHONHASHSEED')
os.environ['PYTHONHASHSEED'] = '0'
#stopwords we do at query time
#from nltk.corpus import stopwords
#stop_words = set(stopwords.words('english'))
#we can create a ancillary index that indexes the titles of the pages and remove stop words
class CrawlerThread:
    url_cache_hash = list() #keep last 15 hashes
    inverted_matrix = defaultdict(dict) #{'a' : {term : {URLS : list(positions)}}}
    visited_set = set() #all visited URLs
    site_maps_cache = dict()



    def __init__(self) -> None:
        self.frontier = frontier.Frontier()
        self.robot_parser = urllib.robotparser.RobotFileParser()
        self.client_connection = mongo.MongoClient()
    


    def _is_valid(self, current_url : urlparse) -> bool:
        #determine if the link should be crawled
        # if url.scheme not in ['http','https']: return False
        # else:
        #all things we do not want to match for now
        
        #if page is already scraped
        #if current_url.geturl() in CrawlerThread.url_cache_hash: return False
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

    def _add_to_indexer(self) -> None:

        for stemmed_word, positions in self.prelim_dict.items():

            regex_obj = re.search("[A-Za-z0-9]+",stemmed_word)

            if regex_obj != None:

                alphabet_to_index = stemmed_word.lower()[regex_obj.span()[0]]

                if alphabet_to_index not in CrawlerThread.inverted_matrix:
                        CrawlerThread.inverted_matrix[alphabet_to_index] = {}

                if stemmed_word not in  CrawlerThread.inverted_matrix[alphabet_to_index]:
                    CrawlerThread.inverted_matrix[alphabet_to_index][stemmed_word] = {}

                CrawlerThread.inverted_matrix[alphabet_to_index][stemmed_word][self.current_url] = positions

 

    def _prelim_parse(self) -> None :
        #we deal with stopwords at query time but stemming at indexing and query 
        # we stem all indices and we stem the query and apply stopwords to the query
        #start1 = time.time()
        self.prelim_dict = dict()
        print(len(self.tokenized))
        print(self.current_url)
        for index, token in enumerate(self.tokenized):

            new_token = tokenizer.Tokenizer.token_conflation(token)
            #start stemming 
            stemmed_word = tokenizer.Tokenizer.stem_word(new_token)


            if (( stemmed_word.isnumeric() and len(stemmed_word) <= 10) or 
                (len(stemmed_word) > 0 and len(stemmed_word) <= 45) ):
                    print(index," ",stemmed_word,end = '\r')
                    # if stemmed_word == 'adélie':
                    #     print()
                    if stemmed_word not in self.prelim_dict:
                       #print("------>", stemmed_word)
                       self.prelim_dict[stemmed_word] = [index]

                    else:
                        #print(" ADDED : ", stemmed_word)
                        self.prelim_dict[stemmed_word].append(index)
                
            #break #TEMP

                        
                        
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

                if self.current_url in CrawlerThread.visited_set:
                    continue
                else:
                    CrawlerThread.visited_set.add(self.current_url)
                

                self.current_parsed = urlparse(self.current_url)
                #CrawlerThread.url_cache_hash.append(self.current_parsed.geturl())
                robot_parse_url = urljoin(self.current_parsed.scheme + '://' + self.current_parsed.netloc ,  'robots.txt') 

                no_robot = False
                try:
                    self.robot_parser.set_url(robot_parse_url)
                    if robot_parse_url not in CrawlerThread.site_maps_cache:
                        print("NEWW CACHE")
                        site_maps_lines = urllib.request.urlopen(robot_parse_url)
                        self.robot_parser.read()
                        CrawlerThread.site_maps_cache[robot_parse_url] = site_maps_lines.read()
                    else:
                        site_map =  CrawlerThread.site_maps_cache[robot_parse_url]
                        #print(type(site_map))
                        self.robot_parser.parse(site_map.decode('utf-8'))
                        print("ALREADY VISITED")
                        
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
                    similar = False
                    matrix_size_bytes = None
                    if self.tokenized: #if list is empty then either it is not relevant or its empty
                        self._prelim_parse()
                        hash_byte_string = LSH.LocalitySensitiveHasher.simHash(self.current_url, self)
                        for hash in CrawlerThread.url_cache_hash:
                            if LSH.LocalitySensitiveHasher.simHashSimilarityScore(hash_byte_string, hash):
                                similar = True
                                print("TOO SIMILAR for : ", self.current_url)
                                print("current byte string : ",hash_byte_string)
                                print("compared : ", hash)
                                print()
                                break

                        if not similar: 
                            if len(CrawlerThread.url_cache_hash) >= 15 : 
                                CrawlerThread.url_cache_hash.pop(0)

                            CrawlerThread.url_cache_hash.append(hash_byte_string)

                            self._add_to_indexer()
                            matrix_size_bytes = asizeof.asizeof(CrawlerThread.inverted_matrix)
                            print("inverted matrix size in bytes : ", matrix_size_bytes)
                            self._extract_links()
                            #profile it -- 500MB to 1GB of RAM then write to disk

                    

                    log_file.write(f"{self.current_url}, IS RELEVANT : {False if not self.tokenized else True} IS INDEXED : \
                                   {True if self.tokenized and not similar else False},\n")

                    #FOR TEST --------------------
                    count += 1
                    if count >= 80 :
                        self.write_to_disk() #TEMP
                        break
                    #END OF TEST ------------------

                    #PROFILING 
                    
                    matrix_size_bytes = asizeof.asizeof(CrawlerThread.inverted_matrix)
                    if matrix_size_bytes >= 200000000:
                        
                        self.write_to_disk()

                    time.sleep(.5)
            
            self.write_to_disk() #write to disk when done
            self.single_thread_binary_merger()
            try:
                log_file.write(f"{os.path.getsize('partial_indexes')}")
            except FileNotFoundError :
                print("fuck")



    def write_to_disk(self) -> None:
        #binary disk write 
        # echo {file you want to ignore} >> .gitignore

        if not os.path.exists("partial_indexes"):
            os.makedirs("partial_indexes")
            for letters in range(26):
                os.makedirs(f'partial_indexes/{chr(97 + letters)}')
            for number in range(10):
                os.makedirs(f'partial_indexes/{number}')
        

        else:
            print("partial_indexes dir already exists")
        

        for letter, terms_dict in CrawlerThread.inverted_matrix.items():

            partial_ordered = OrderedDict(sorted(terms_dict.items()))

            
            #print(letter, terms_dict)
            with open(f"partial_indexes/{letter}/_{len(os.listdir(f'partial_indexes/{letter}'))}.json",'w') as fp:
                
                fp.write(json.dumps(partial_ordered, indent = 2))
        

        CrawlerThread.inverted_matrix = {}
    
    def single_thread_binary_merger(self) -> None:
        #merges files to a single merged json file
        #goes through each alpahbet and each partial for each alphabet, joins dicts together then merges dup keys 

        def is_empty(file_list) -> bool:
            if type(file_list) == list:
                if len(file_list) > 0 : return False
                else : return True
            else:
                file_list.seek(0)
                char = file_list.read(1)
                file_list.seek(0)
                return char != '{'

        path = "partial_indexes"
        for alphabet in os.listdir(path):
            print(alphabet)
            
            cur_path = Path(os.path.join(path,alphabet))
            list_of_partials = list(cur_path.iterdir())
            final_merge = Path(list_of_partials[0])


            new_dict = OrderedDict()
            with open(final_merge, "r+") as final_merged_file:
                final_merged_is_empty = False

                if is_empty(final_merged_file): 
                    print('is empty for final merge')
                    final_merged_is_empty = True

                for partial_index in list_of_partials[1:]:
                    print(partial_index)
                    # if partial_index == Path(r"partial_indexes\0\_62.json"):
                    #     print("WTF")
                        
                    #read dict from final file
                    pointer1 = 0
                    pointer2 = 0

                    with open(partial_index, "r+") as partial_to_merge:
                        #read dict form file to merge
                        #print(is_empty(partial_to_merge))
                        if is_empty(partial_to_merge):
                            continue

                        partial_data = json.load(partial_to_merge)
                            
                        partial_dict = list(partial_data.items())
                        
                        #print(len(partial_dict))
                        partial_length = len(partial_dict)


                        if final_merged_is_empty and not is_empty(partial_to_merge): 
                                
                            json.dump(partial_data ,final_merged_file,indent = 2)
                            final_merged_file.seek(0)
                            # print("dumped")
                            final_merged_is_empty = False
                            continue 

                        #final_merged_file.seek(0) #problem lies here
                        final_partial_dict = list(new_dict.items())
                        final_merged_file.seek(0)
                        final_partial_length = len(final_partial_dict)

                        new_dict = OrderedDict() #dict to be dumped into json final merge file
                        while pointer1 < final_partial_length and pointer2 < partial_length:
                            entry1 = final_partial_dict[pointer1]
                            entry2 = partial_dict[pointer2]
                            if entry1[0] < entry2[0]:
                                new_dict[entry1[0]] =  entry1[1]
                                pointer1 += 1
                            #shared keys are nulled
                            elif entry1[0] == entry2[0]:
                                # print("key : ", entry1[0], " ",entry2[0])
                                # print(entry1[1])
                                # print(entry2[1])
                                new_merged_dict = entry1[1] | entry2[1]
                                # print()
                                # print(new_merged_dict)
                                
                                new_dict[entry1[0]] = new_merged_dict
                                pointer1+=1
                                pointer2 +=1
                            else:
                                new_dict[entry2[0]] =  entry2[1]
                                pointer2 += 1
                        #dump the rest of the dictionary which ever one is left
                        while pointer1 < final_partial_length:
                            new_dict[final_partial_dict[pointer1][0]] = final_partial_dict[pointer1][1]
                            pointer1 +=1
                        while pointer2 < partial_length:
                            new_dict[partial_dict[pointer2][0]] = partial_dict[pointer2][1]
                            pointer2 +=1

                    json.dump(new_dict,final_merged_file, indent = 2)




    def get_auxillary_indices(self, flag = "index_of_indices") -> dict:
        #will connect to mongoDB server to get indices and read into memory
        if flag == "index_of_indices":
            pass
        elif flag == "index_of_pics":
            pass

        return dict()

                




if __name__ == "__main__":
    current_crawl = CrawlerThread()
    current_crawl.crawl()


