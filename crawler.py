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


class CrawlerThread:



    def __init__(self) -> None:
        self.frontier = frontier.Frontier()

    def crawl(self) -> None:
        
        while self.frontier.queue:
            current_url = self.frontier.dequeue()
            #look at robot file
            
            #construct bs4 object
            bs_obj = bs4.BeautifulSoup(current_url, 'html.parser')
            #get the text
            tokenized = tokenizer.Tokenizer.tokenize(bs_obj)
            if not tokenized:
                #get all links
                self.frontier.queue.extend(bs_obj.find_all('a'))
    







if __name__ == "__main__":
    current_crawl = CrawlerThread()


