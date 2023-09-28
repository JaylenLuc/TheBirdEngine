import math
from collections import Counter
import json
import re
class Ranker:
    TOTAL_DOCUMENTS = 30000

    @staticmethod 
    def retrieve_articles(query_term : str) -> dict[str, dict[str, list[int]]]:
        with open(r'C:\Users\Jaylen\Desktop\TheBirdEngine\index_of_index.json', 'r') as fp :
            index_of_index = json.load(fp)
            pos = index_of_index[query_term]


            regex_obj = re.search("[A-Za-z0-9]+",query_term)

            if regex_obj != None:

                alphabet_to_index = query_term.lower()[regex_obj.span()[0]]


                with open(f'partial_indexes\\{alphabet_to_index}\\_0.txt', 'r') as index :
                    index.seek(pos)
                    postings_list = json.loads(index.readline())
                    
                    return postings_list
    @staticmethod
    def vector_space_rank(text_query : list[str]) -> list[str]:
        #we use tf.idf model
        #weight of a term is = (1 + log(tf)) x log(N/df)
        #weighting scheme for now : lnc.ltc, ddd,qqq
        query_vector = Ranker.lncltc_query_vector(text_query)
        #compute vector for query


        return ""
    
    @staticmethod
    def lncltc_query_vector(text_query : list[str]) -> list[float]: #returns the query vector
        query_vector = [0] * len(text_query)
        frequencies = Counter(text_query)
        for index in range(len(text_query)):
            #log tf and idf then cosine normalize
            current_term = text_query[index]
            #first calculate tf
            log_tf = 1 + math.log(frequencies[current_term],10)

            postings_list = Ranker.retrieve_articles(current_term)
            idf = Ranker.TOTAL_DOCUMENTS / len(postings_list[current_term].values())


            