#frontier = Queue
class Frontier:
    queue = []
    def __init__(self) -> None:
        #create the seed
        pass
    
    def dequeue(self) -> str:
        #removes traversed url
        return Frontier.queue.pop(0)
    
    def enqueue(self, url : str) -> None:
        #populizes frontier
        Frontier.queue.append(url)
