#web development platform for python
from flask import Flask

#for jason response
from flask import jsonify

#priority queue for ranking the results based on relevance
from queue import PriorityQueue

#web scraping library
from bs4 import BeautifulSoup as bs

#http request library
import requests as rq

#for nltk libraries for approximate string matching of results
import nltk.corpus
import nltk.stem.snowball
import string
from nltk import word_tokenize
from nltk.corpus import wordnet


#google search library for python
from googlesearch import search



#download nltk files
nltk.download("stopwords") 
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')


# Get default English stopwords and extend with punctuation
#this is needed to approximate string matching
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(string.punctuation)
stopwords.append('')

#inialize lemmatizer see https://en.wikipedia.org/wiki/Lemmatisation for definition
lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()



app = Flask(__name__)

#web service with [query] parameter/variable 
#default number of returned results is 5
@app.route('/<query>')
def scrape(query, num_results =5):
        #strip the query off whitespaces
        query = query.strip(string.punctuation)

        #list containing final result
        results_list = PriorityQueue()
        

        #list of html tags to be exempted during string matching
        exemption_list = ["form", "script", "style"]

        #match accuracy list
        match_accuracy = [.8, .6, .4, .2, .1]

        #maximum retrieved from google
        max_retrievable = 10

        #sentinel for number of results seen
        result_count = 0

        #parse query to googlesearch library for search
        #this call then returns a generator containing list of urls of size max_retrievable
        #loop through the urls and scraped contents under html using beautifulsoup
        #rank scraped content based on percentage match -match_acc
        for url in search(query.strip(), tld="co.in", stop =  max_retrievable, pause=2):
                try:
                        r = rq.get(url) #get request from url
                        if r.status_code == 200: # if request was successfully                                                            
                                soup = bs(r.text, 'html5lib') #fetch html from request and parse for scraping using beautifulsoup
                                listTags = soup.html.findAll() #perform a recursive search for all children tags under html
                                
                                # retrive tags with relevant information and rank them based on match accuracy
                                for rank, match_acc in enumerate(match_accuracy):
                                        relevant_text = relevant_information(listTags, query, exemption_list, match_acc) # retrieve relevant text within html using approximate string matching
                                        if relevant_text != None:
                                                #insert relevant information and the url into a priority queue ranked by match accuracy
                                                results_list.put((rank, [url, relevant_text]))
                                                break #break once relevant information found from url's website                                      
                except Exception as e:
                        print (e)
                        return "No result - something happened"
        
        jason_result = []
        #retrieve top num_results results and return such as json response
        while not results_list.empty() and result_count < num_results:
                r = results_list.get()[1]
                jason_result.append(r)
                result_count +=1
        return jsonify(jason_result)
                              

# perform approximate string matching - sometimes called fuzzy match, on all tags (except the exemption list), within html documents 
#for approximate sentence match, we use nltk library
def relevant_information(tags, query, tag_exemption, match_percent = 0.1):
        for t in tags:
                if not t in tag_exemption: #scan only tags not includeded in the exemption list
                        #get word tokens for only with only alphabetical words
                        if t.string != None: #some html strings can be none... handle that                                       
                                match_tokens = [token.lower().strip() for token in word_tokenize(t.string) if token.isalpha() or token not in stopwords]
                                query_tokens = [token.lower().strip() for token in word_tokenize(query) if token.isalpha() or token not in stopwords]                        
                        else:
                                continue
                        #get word tagging for lemmerization                        
                        pos_qr = map(get_wordnet_pos, nltk.pos_tag(query_tokens))
                        pos_mt = map(get_wordnet_pos, nltk.pos_tag(match_tokens))

                        #lemmerize
                        lemmae_qr = [lemmatizer.lemmatize(token.lower(), pos) for token, pos in pos_qr] 
                        lemmae_mt = [lemmatizer.lemmatize(token.lower(), pos) for token, pos in pos_mt]

                        #using intersection over union metric, calculate the match
                        s = len(set(lemmae_qr).intersection(lemmae_mt)) / float(len(set(lemmae_qr).union(lemmae_mt)))
                        
                        if (s>=match_percent):
                                return t.string #return once match meeets criteria          
        
        return None # return None when no suitable match found in the website

#define wordnet tagging function used in lemmerization
def get_wordnet_pos(pos_tag):
        if pos_tag[1].startswith('J'):
                return (pos_tag[0], wordnet.ADJ)
        elif pos_tag[1].startswith('V'):
                return (pos_tag[0], wordnet.VERB)
        elif pos_tag[1].startswith('N'):
                return (pos_tag[0], wordnet.NOUN)
        elif pos_tag[1].startswith('R'):
                return (pos_tag[0], wordnet.ADV)
        else:
                return (pos_tag[0], wordnet.NOUN)
                       



if __name__=='__main__':
    app.run(debug=True)