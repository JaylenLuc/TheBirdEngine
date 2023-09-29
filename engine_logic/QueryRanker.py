import math
from collections import Counter
import json
import re
class Ranker:
    TOTAL_DOCUMENTS = 30000

    CHAMPIONS_LIST_CUTOFF = 5

    @staticmethod 
    def retrieve_articles(query_term : str) -> dict[str, dict[str, list[int]]]:
        with open(r'C:\Users\Jaylen\Desktop\TheBirdEngine\index_of_index.json', 'r') as fp :
            index_of_index = json.load(fp)

            #congruent term processing so that similar words in substance are found in the index because the index was indexed with subtance of the word in mind
            query_term = query_term[regex_obj.span()[0] : regex_obj.span()[1]]
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
        #compute vector for query
        query_vector, all_postings = Ranker.lncltc_query_vector(text_query)
        top_res = Ranker.rank_documents_lnc_ltc(query_vector, all_postings)


        return top_res
    
    @staticmethod
    def lncltc_query_vector(text_query : list[str]) -> tuple[list[float], list[ dict[str, list[int]]]]: #returns the query vector
        query_vector = [0] * len(text_query)
        all_postings = []
        frequencies = Counter(text_query)
        normal_sum = 0
        for index in range(len(text_query)):
            #log tf and idf then cosine normalize
            current_term = text_query[index]
            #first calculate tf
            log_tf = 1 + math.log(frequencies[current_term],10)

            postings_list = Ranker.retrieve_articles(current_term)[current_term]
            df = len(postings_list[current_term].values())
            idf = Ranker.TOTAL_DOCUMENTS / df

            wt = log_tf * idf

            normal_sum += wt ** 2 

            query_vector.append(wt)

            all_postings.append(postings_list)

        l_2_norm = math.sqrt(normal_sum)

        #normalization
        for index in range(len(query_vector)):
            query_vector[index] = query_vector[index] / l_2_norm

        return (query_vector, all_postings)
    
    @staticmethod
    def rank_documents_lnc_ltc(query_vector : list[float], all_postings : list[dict[str, dict[str, list[int]]]]) -> list[str]:
        #documents should contain ~75%  
        threshold = math.ceil(len(query_vector) * .75) - 1
        contenders_list = []
        #only compute the scores for the docs in the union
        #1 - we go thru all the docs in the longest posting_list
        #2 - for each doc in the longest posting_list we see if it is in at least threshold other posting_lists
        #3 - if it is , then compute the score and store the score with the URL in a list


        for term in query_vector:
            pass
        
        return 


            