#frontier = Queue
class Frontier:
    queue = []
    def __init__(self) -> None:
        Frontier.queue = ['https://en.wikipedia.org/wiki/List_of_birds_by_common_name'] #automatically make a google query and get the top 3 results

        #FUTURE functionality : web scrape top N results from google without any libraries 
    
    
    def dequeue(self) -> str:
        #removes traversed url
        return Frontier.queue.pop(0)
    
    def enqueue(self, url : str) -> None:
        #populizes frontier
        Frontier.queue.append(url)
