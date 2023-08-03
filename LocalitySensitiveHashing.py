
#this is where we reduce the dimensionality of our data, determine distances, maximize collisions, and determine duplication with our local definition
from crawler import CrawlerThread
import hashlib

class LocalitySensitiveHasher: 
    _BIT_HASH_LENGTH = 256
    _SIM_HASH_THRESHOLD = 12
    @staticmethod
    def simHash(current_url : str, crawler_instance : CrawlerThread) -> list:
        final_hash = [0] * 256

        def _generate_32_bit_hash(token : str):
            if (token != None) and (type(token) ==  str) and (len(token) > 0):
                # print(crawler_instance.prelim_dict)
                # print()
                # print(crawler_instance.tokenized)

                weight = len(crawler_instance.prelim_dict[token])
                hex_ = hashlib.sha256(token.encode('utf-32')).hexdigest()
                bin_ = bin(int(hex_, 32))[2:] #32 bit binary rep remove 0x

                return [bin_,weight]
        

        _list_of_bits = list(map(_generate_32_bit_hash, crawler_instance.prelim_dict.keys())) # a list of lists [[bits, weights],...]

        for binary_str, weight in _list_of_bits:
            for i in range(LocalitySensitiveHasher._BIT_HASH_LENGTH):
                if binary_str[i] == "1":
                    final_hash[i] += weight
                else:
                    final_hash[i] -= weight 

        for i in range(LocalitySensitiveHasher._BIT_HASH_LENGTH):
            if int(final_hash[i]) >= 0 :
                final_hash[i] = "1"
            else:
                final_hash[i] = "0"

        return final_hash



            

            

    @staticmethod
    def simHashSimilarityScore(current_hash : list, compared_hash : list) -> bool:

        current_hash = "".join(current_hash)
        compared_hash = "".join(compared_hash)


        #hamming distance
        #returns true if they are too similar 
        #XOR the two binary strings and all the ones are counted to produce the hamming distance. if < 77 then false otherwise true

        new_int = int(current_hash,2) ^ int(compared_hash,2)
        bin_ = bin(int(new_int))[2:]
        count_differences = bin_.count('1')
        if count_differences > LocalitySensitiveHasher._SIM_HASH_THRESHOLD:

            return False
        
        else:
            print()
            print(count_differences)
            return True
    