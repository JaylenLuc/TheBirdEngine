import bs4
import re
from krovetzstemmer import Stemmer
from collections import defaultdict
import urllib

# -*- coding: utf-8 -*-

html_doc = """<html><head><title>The Dormouse's story.</title></head>
<body>
<p class="title"><b>The Dormouse's\t story</b></p>

<p class="story">Once-upon a "time" there were-three little.sisters; and their names were 
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""


ex = """As they rounded a bend in the path that ran beside the river, Lara recognized the silhouette of a fig tree atop a nearby hill. The weather was hot and the days were long. The fig tree was in full leaf, but not yet bearing fruit.
Soon Lara spotted other landmarks—an outcropping of limestone beside the path that had a silhouette like a man’s face, a marshy spot beside the river where the waterfowl were easily startled, a tall tree that looked like a man with his arms upraised. They were drawing near to the place where there was an island in the river. The island was a good spot to make camp. They would sleep on the island tonight.
Lara had been back and forth along the river path many times in her short life. Her people had not created the path—it had always been there, like the river—but their deerskin-shod feet and the wooden wheels of their handcarts kept the path well worn. Lara’s people were salt traders, and their livelihood took them on a continual journey.
At the mouth of the river, the little group of half a dozen intermingled families gathered salt from the great salt beds beside the sea. They groomed and sifted the salt and loaded it into handcarts. When the carts were full, most of the group would stay behind, taking shelter amid rocks and simple lean-tos, while a band of fifteen or so of the heartier members set out on the path that ran alongside the river.
With their precious cargo of salt, the travelers crossed the coastal lowlands and traveled toward the mountains. But Lara’s people never reached the mountaintops; they traveled only as far as the foothills. Many people lived in the forests and grassy meadows of the foothills, gathered in small villages. In return for salt, these people would give Lara’s people dried meat, animal skins, cloth spun from wool, clay pots, needles and scraping tools carved from bone, and little toys made of wood.
Their bartering done, Lara and her people would travel back down the river path to the sea. The cycle would begin again.
It had always been like this. Lara knew no other life. She traveled back and forth, up and down the river path. No single place was home. She liked the seaside, where there was always fish to eat, and the gentle lapping of the waves lulled her to sleep at night. She was less fond of the foothills, where the path grew steep, the nights could be cold, and views of great distances made her dizzy. She felt uneasy in the villages, and was often shy around strangers. The path itself was where she felt most at home. She loved the smell of the river on a hot day, and the croaking of frogs at night. Vines grew amid the lush foliage along the river, with berries that were good to eat. Even on the hottest day, sundown brought a cool breeze off the water, which sighed and sang amid the reeds and tall grasses.
Of all the places along the path, the area they were approaching, with the island in the river, was Lara’s favorite.
The terrain along this stretch of the river was mostly flat, but in the immediate vicinity of the island, the land on the sunrise side was like a rumpled cloth, with hills and ridges and valleys. Among Lara’s people, there was a wooden baby’s crib, suitable for strapping to a cart, that had been passed down for generations. The island was shaped like that crib, longer than it was wide and pointed at the upriver end, where the flow had eroded both banks. The island was like a crib, and the group of hills on the sunrise side of the river were like old women mantled in heavy cloaks gathered to have a look at the baby in the crib—that was how Lara’s father had once described the lay of the land.
Larth spoke like that all the time, conjuring images of giants and monsters in the landscape. He could perceive the spirits, called numina, that dwelled in rocks and trees. Sometimes he could speak to them and hear what they had to say. The river was his oldest friend and told him where the fishing would be best. From whispers in the wind he could foretell the next day’s weather. Because of such skills, Larth was the leader of the group.
“We’re close to the island, aren’t we, Papa?” said Lara.
“How did you know?”
“The hills. First we start to see the hills, off to the right. The hills grow bigger. And just before we come to the island, we can see the silhouette of that fig tree up there, along the crest of that hill.”
“Good girl!” said Larth, proud of his daughter’s memory and powers of observation. He was a strong, handsome man with flecks of gray in his black beard. His wife had borne several children, but all had died very young except Lara, the last, whom his wife had died bearing. Lara was very precious to him. Like her mother, she had golden hair. Now that she had reached the age of childbearing, Lara was beginning to display the fullness of a woman’s hips and breasts. It was Larth’s greatest wish that he might live to see his own grandchildren. Not every man lived that long, but Larth was hopeful. He had been healthy all his life, partly, he believed, because he had always been careful to show respect to the numina he encountered on his journeys.
Respecting the numina was important. The numen of the river could suck a man under and drown him. The numen of a tree could trip a man with its roots, or drop a rotten branch on his head. Rocks could give way underfoot, chuckling with amusement at their own treachery. Even the sky, with a roar of fury, sometimes sent down fingers of fire that could roast a man like a rabbit on a spit, or worse, leave him alive but robbed of his senses. Larth had heard that the earth itself could open and swallow a man; though he had never actually seen such a thing, he nevertheless performed a ritual each morning, asking the earth’s permission before he went striding across it.
“There’s something so special about this place,” said Lara, gazing at the sparkling river to her left and then at the rocky, tree-spotted hills ahead and to her right. “How was it made? Who made it?”
Larth frowned. The question made no sense to him. A place was never made, it simply was. Small features might change over time. Uprooted by a storm, a tree might fall into the river. A boulder might decide to tumble down the hillside. The numina that animated all things went about reshaping the landscape from day to day, but the essential things never changed, and had always existed: the river, the hills, the sky, the sun, the sea, the salt beds at the mouth of the river.
He was trying to think of some way to express these thoughts to Lara, when a deer, drinking at the river, was startled by their approach. The deer bolted up the brushy bank and onto the path. Instead of running to safety, the creature stood and stared at them. As clearly as if the animal had whispered aloud, Larth heard the words “Eat me.” The deer was offering herself.
Larth turned to shout an order, but the most skilled hunter of the group, a youth called Po, was already in motion. Po ran forward, raised the sharpened stick he always carried and hurled it whistling through the air between Larth and Lara.
A heartbeat later, the spear struck the deer’s breast with such force that the creature was knocked to the ground. Unable to rise, she thrashed her neck and flailed her long, slender legs. Po ran past Larth and Lara. When he reached the deer, he pulled the spear free and stabbed the creature again. The deer released a stifled noise, like a gasp, and stopped moving.
There was a cheer from the group. Instead of yet another dinner of fish from the river, tonight there would be venison.
The distance from the riverbank to the island was not great, but at this time of year—early summer—the river was too high to wade across. Lara’s people had long ago made simple rafts of branches lashed together with leather thongs, which they left on the riverbanks, repairing and replacing them as needed. When they last passed this way, there had been three rafts, all in good condition, left on the east bank. Two of the rafts were still there, but one was missing.
“I see it! There—pulled up on the bank of the island, almost hidden among those leaves,” said Po, whose eyes were sharp. “Someone must have used it to cross over.”
“Perhaps they’re still on the island,” said Larth. He did not begrudge others the use of the rafts, and the island was large enough to share. Nonetheless, the situation required caution. He cupped his hands to his mouth and gave a shout. It was not long before a man appeared on the bank of the island. The man waved.
“Do we know him?” said Larth, squinting. I.B.M, IBM
"""
import urllib.robotparser
import urllib.request
from urllib.parse import urlparse, urljoin
import urllib.request
# from nltk.corpus import stopwords
# from urllib.parse import urlparse,urljoin
# import urllib.robotparser
# import hashlib
# test_dict = dict()
# url = "https://docs.python.org/3/library/"

# current_parsed = urlparse(url)

# robot_parser = urllib.robotparser.RobotFileParser()
# for i in range(2):
#     robot_parse_url = urljoin(current_parsed.scheme + '://' + current_parsed.netloc , 'robots.txt') 
#     site_maps_lines = urllib.request.urlopen(robot_parse_url)
#     #print(site_maps_lines.read())
    
#     robot_parser.set_url(robot_parse_url)
#     if robot_parse_url not in test_dict:
#         robot_parser.read()
#         print(robot_parser.can_fetch("*",url))
#         test_dict[robot_parse_url] = site_maps_lines.read()
#     else:
#         site_map = test_dict[robot_parse_url]
#         print(type(site_map))
#         robot_parser.parse(site_map.decode('utf-8'))
#         print(robot_parser.can_fetch("*",url))












# # parsed = urlparse(url)
# import os 
# hashseed = os.getenv('PYTHONHASHSEED')
# os.environ['PYTHONHASHSEED'] = '0'

# #how are we going to split words first of all?:

# #Do we care about capitlization - NO
# #how about apostrophies or periods? what about hyphens -(periods we split, hyphens and em dashes we split, apostrpoohies )?
# #eg I.B.M , query : IBM --- fixed by igonoring periods only when it is followed by a space ---> conflate the entire token
# #stem all the words

# # Micheals Micheal Micheal's
# import functools
# from krovetzstemmer import Stemmer
# import os
# import json
# from collections import OrderedDict
# #  BIT_HASH_LENGTH = 3
# li = [["101",1],["010",5],["111",3],["110",7]]
    

            
# return_vec = [0] * 3
# for binary_str, weight in li:
#     for i in range(3):
#         if binary_str[i] == "1":
#             return_vec[i] += weight
#         else:
#             return_vec[i] -= weight 
# for i in range(BIT_HASH_LENGTH):
#     if int(return_vec[i]) > 0 :
#         return_vec[i] = 1
#     else:
#         return_vec[i] = 0
# print(str(return_vec))
# current_hash = b"0101101010001100100100110101111010000111011010010111110010111101100101110100010001111010011101011100111010101100010111110100111011111101110100000010111001110010100101010000010101010110000010101101000010001110101010101011000010010111110000101100001100001011"
# compared_hash =b"1110001100101111011010101000000001100101011011111001000110001100101000010111110001000100010101011101101110100010010010011100000101100010000111010001110001000110110011010001110011100000000110111011111001000100101010101011000101001010110011010000111010011000"
# new_int = int(current_hash,2) ^ int(compared_hash,2)
# bin_ = bin(int(new_int))[2:]
# print(bin_.count('1'))
# print(f"{True}")

# if not os.path.exists("partial_indexes"):
#     os.makedirs("partial_indexes")
#     for letters in range(26):
#         os.makedirs(f'partial_indexes/{chr(97 + letters)}')
# else:
#     print("partial_indexes dir already exists")

        
        
        
#         }
# temp1 = {'a' : {'albert' : {"11" : [1,2,3,4,245,6,67],"22" : [1,2,3,434,5,6,67]},'abudia' : {"55" : [1111,2,3,4,5,6,67],"67" : [1111,243,3,4,5,6,64327]}}}
# print(temp['a']['abudia'])
# temp_ordered = {}
# for letter, term_dict in temp.items():
#     temp_ordered = collections.OrderedDict(sorted(term_dict.items()))
#     temp[letter] = {}
# print(temp_ordered)
# print(temp)


# with open("partial_indexes/a.json",'w') as fp:

#     json.dump(temp_ordered ,fp)

# # print(temp)

# def test():
#     for letter, term_dict in temp.items():

#         partial_ordered = OrderedDict(sorted(term_dict.items()))
        
#         with open(f"partial_indexes/{letter}/_{len(os.listdir(f'partial_indexes/{letter}'))}.json",'w') as fp:
                    
#             fp.write(json.dumps(partial_ordered, indent = 2))
temp = {'a' : {'azera' : {"1" : [1,2,3,4,5,6,67],"2" : [1,2,3,4,5,6,67],"14" : [1,2,3,323234,5,6,67]},'albert' : {"1" : [1,2,3,4,5,6,67],"2" : [1,2,3,4,5,6,67]},'abudia' : {"5" : [1111,2,3,4,5,6,67],"6" : [1111,2,3,4,5,6,64327]}},
         'x' : {'xzera' : {"1" : [1,2,3,4,5,6,67],"2" : [1,2,3,4,5,6,67],"14" : [1,2,3,323234,5,6,67]},'xlbert' : {"1" : [1,2,3,4,5,6,67],"2" : [1,2,3,4,5,6,67]},'xbudia' : {"5" : [1111,2,3,4,5,6,67],"6" : [1111,2,3,4,5,6,64327]}}}


import pymongo as mongo
import pprint
#-------------------------------------------------------------------------------------------------------------------
# conn_str = "mongodb+srv://jaylenluc1:cocmaster1@cluster0.xtpwykd.mongodb.net/?retryWrites=true&w=majority"

# client = mongo.MongoClient(conn_str)

# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

# db = client["test_db"]

# print(db.list_collection_names())

# posts = db.posts

# def make1():
#     print(client.list_database_names())

#     post_id = posts.insert_one(temp).inserted_id

#     print(post_id)

#     print(client.list_database_names())

# def find1():
#     #pprint.pprint(posts.find_one())
#     print()
#     print('hi')
#     print(posts.find_one())
#     cursor = posts.find({},{'x' : 1})
#     print('cursor')
#     print(cursor[0])



# #make1()
# find1()

#-------------------------------------------------------------------------------------------------------------------
from pathlib import Path
import os
import json
from collections import OrderedDict
# #creates the directory
# if not os.path.exists("partial_indexes"):
#     os.makedirs("partial_indexes")
#     for letters in range(26):
#         os.makedirs(f'partial_indexes/{chr(97 + letters)}')
#     for number in range(10):
#         os.makedirs(f'partial_indexes/{number}')







#USE PANDAS TO READ CHUNKS OF JSON AT A TIME
def single_thread_binary_merger():

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
                if partial_index == Path(r"partial_indexes\0\_62.json"):
                    print("WTF")
                    
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
                #final_merged_file.seek(0)
        #break






#test code
# test1 = {"rew" : {"fdsafdas": [1,2,3,4,5], "fdsafdsafad" : [32532543]}, "hi" : {'fdsafd' : [54325]}, "rewr" : {"fdsafdsaf" : [543,4324]}}

# test2 = {"aplzaplrew" : {'fdsafds' : [2,34,5,7,3]}, "plpklphi" : {"fdasfdsa" : [1,2,4,6,7], "vbcnxzmvb" : [1,2,43]}}

# test1 = list(test1.items())
# test2 = list(test2.items())
# pointer1 = 0
# pointer2 = 0
# print(test1[pointer1][0])
# print(test1[pointer1][1])
# to_be_added = dict()
# to_be_added[test1[pointer1][0]] =  test1[pointer1][1]
# print(to_be_added)
# if "ab" < "albert":
#     print("ab is first")
# else:
#     print("albert is first")



# new_dict = dict() #dict to be dumped into json final merge file
# while pointer1 < len(test1) and pointer2 < len(test2):
#     entry1 = test1[pointer1]
#     entry2 = test2[pointer2]
#     if entry1[0] < entry2[0]:
#         new_dict[entry1[0]] =  entry1[1]
#         pointer1 += 1
#     elif entry1[0] == entry2[0]
#     else:
#         new_dict[entry2[0]] =  entry2[1]
#         pointer2 += 1
# #end of test code
# while pointer1 < len(test1):
#     new_dict[test1[pointer1]] = test1[pointer1]
#     pointer1 +=1
# while pointer2 < len(test2):
#     new_dict[test2[pointer2]] = test2[pointer2]
#     pointer2 +=1




single_thread_binary_merger() #merger tester
# list(obj.items())
# with open(r"C:\Users\Jaylen\Desktop\TheBirdEngine\partial_indexes\0\_0.json", "r+") as raw:
#     obj = json.load(raw)
# list(obj.items())
# with open(r"C:\Users\Jaylen\Desktop\TheBirdEngine\partial_indexes\0\_1.json", "r") as st:
#     print(type(st))
#     char = st.read(1)
#     print(char != '{')


