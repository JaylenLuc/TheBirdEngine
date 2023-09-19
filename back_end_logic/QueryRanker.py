class Ranker:

    @staticmethod 
    def retrieve_articles(query_term : str) -> dict[str, dict[str, list[int]]]:

        #read N chunks from teh alphabet dictionary
        #if query_term is greater than the last chunk then read the next N chunks until word is found
        #return the entire dicitonary
        return