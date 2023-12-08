import math
from collections import Counter
import json
import re
from pathlib import Path
import os
class Ranker:
    TOTAL_DOCUMENTS = 30000

    CHAMPIONS_LIST_CUTOFF = 5

    @staticmethod 
    def retrieve_articles(query_term : str) -> dict[str, dict[str, list[int]]]:
        #C:\Users\Jaylen\Desktop\TheBirdEngine\partial_indexes
        dirname = os.path.dirname(__file__)
        index_of_index_path =  os.path.join(dirname, 'index_of_index.json')
        #print(index_of_index_path)
        with open(index_of_index_path, 'r',encoding="utf8") as fp : #index_of_index.json
            index_of_index = json.load(fp)

            #congruent term processing so that similar words in substance are found in the index because the index was indexed with subtance of the word in mind
            regex_obj = re.search("[A-Za-z0-9]+",query_term)
            query_term = query_term[regex_obj.span()[0] : regex_obj.span()[1]]
            pos = index_of_index[query_term]

            if regex_obj != None:

                alphabet_to_index = query_term.lower()[regex_obj.span()[0]]

                #partial_indexes\m
                dirname1 = os.path.dirname(__file__)
                indexpath =  os.path.join(dirname1, f'partial_indexes/{alphabet_to_index}/_0.txt')
                with open(indexpath, 'r' ,encoding="utf8") as index :
                    index.seek(pos)
                    postings_list = json.loads(index.readline())
                    print(postings_list)
                    
                    return postings_list
    @staticmethod
    def vector_space_rank(text_query : list[str]) -> list[str]:
        #we use tf.idf model
        #weight of a term is = (1 + log(tf)) x log(N/df)
        #weighting scheme for now : lnc.ltc, ddd,qqq
        #compute vector for query
    
        query_vector, all_postings, every_url = Ranker.lncltc_query_vector(text_query)
        top_res = Ranker.rank_documents_lnc_ltc(query_vector, all_postings, every_url)


        return top_res
    
    @staticmethod
    def lncltc_query_vector(text_query : list[str]) -> tuple[list[float], list[ dict[str, list[int]]], list[set[str]]]: #returns the query vector
        query_vector = [0] * len(text_query)
        print()
        all_postings = []
        frequencies = Counter(text_query)
        normal_sum = 0
        
        all_urls = list(set())
        for index in range(len(text_query)):
            print("atemr in : " ,text_query[index])
            #log tf and idf then cosine normalize
            current_term = text_query[index].strip()
            #first calculate tf
            log_tf = 1 + math.log(frequencies[current_term],10)

            postings_list = Ranker.retrieve_articles(current_term)[current_term]
            all_urls.append(set())
            for posting in postings_list.keys():
                all_urls[index].add(posting)

            df = len(postings_list.values())
            idf = Ranker.TOTAL_DOCUMENTS / df

            wt = log_tf * idf

            normal_sum += wt ** 2 

            query_vector[index] = wt

            all_postings.append(postings_list)
            for i, posting in enumerate(postings_list.items()):
                if i <= 10:
                    log_tf = 1 + math.log(len(posting[1]),10)
                    

        l_2_norm = math.sqrt(normal_sum)

        #normalization
        for index in range(len(query_vector)):
            query_vector[index] = query_vector[index] / l_2_norm
        print("query vector: ", query_vector)
        return (query_vector, all_postings, all_urls)
    
    @staticmethod
    def rank_documents_lnc_ltc(query_vector : list[float], all_postings : list[dict[str, dict[str, list[int]]]], all_urls: list[set[str]]) -> list[str]:
        #documents should contain ~75%  
        #only score documents for high tf-idf terms
        threshold = math.ceil(len(query_vector) * .75) - 1
        contenders_list = []
        
        #only compute the scores for the docs in the union
        #1 - we go thru all the docs in the longest posting_list DID NOT DO THIS YET
        #2 - for each doc in the longest posting_list we see if it is in at least threshold other posting_listsDID NOT DO THIS YET
        #3 - if it is , then compute the score and store the score with the URL in a list
        scores_dict = dict()
        for term_i, posting in enumerate(all_postings):
           # print("posting: ",posting)
            for i, post in enumerate(posting.items()): 
                if i <= 10:
                    log_tf = 1 + math.log(len(post[1]),10)
                if post[0] not in scores_dict:
                    scores_dict[post[0]] = [0] * len(query_vector)
                scores_dict[post[0]][term_i] = log_tf


        print("SOCRES: ", scores_dict)

        #NOW WE NEED TO LENGTH NORMALIZE 
        for url, weight in scores_dict.items():
        #     print("before: ",weight)
        #     doc_len = 0
        #     for wt in weight:
        #         doc_len += (wt ** 2)
        #     doc_len = math.sqrt(doc_len)
        #     for index, wt in enumerate(weight):
        #         weight[index] = weight[index] / doc_len

        #    print("after: ",weight)

            scores_dict[url] = sum(scores_dict[url])

        #print("scores: ",scores_dict.items())
        ranked_asc = dict(sorted(scores_dict.items(), key=lambda item: -item[1]))
        res = [k for k,v in ranked_asc.items()]

        #what we currently have is LNN.LTC


        return res


            