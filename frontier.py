#frontier = Queue
class Frontier:
    queue = []
    def __init__(self) -> None:
        Frontier.queue = ['https://birdsoftheworld.org/bow/home','https://www.britannica.com/animal/bird-animal','https://www.allaboutbirds.org/news/', 'https://www.audubon.org/bird-guide','https://en.wikipedia.org/wiki/Bird'] #automatically make a google query and get the top 3 results

        #FUTURE functionality : web scrape top N results from google without any libraries 
    
    
    def dequeue(self) -> str:
        #removes traversed url
        return Frontier.queue.pop(0)
    
    def enqueue(self, url : str) -> None:
        #populizes frontier
        Frontier.queue.append(url)
