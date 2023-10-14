from Models.textprocessor import process_text,tokens_freqency,create_bigram
import math


class Query:
    def __init__(self,query,database):
        self.query = query
        self.database = database

    def create_tf_idf(self):
        tokens = process_text(self.query)
        tf = tokens_freqency(tokens)
        total_doc = 37497
        
        wt = {}
        query_len = 0
        for token in tf:
           token_inverted_index = self.database.findById("Inverted_index",token)
           if token_inverted_index == None:
                continue
           df = len(token_inverted_index["data"])

           idf = math.log10(total_doc/df)
           tf_wt = math.log10(tf[token]) + 1
           wt[token] = tf_wt * idf
           query_len += math.pow(wt[token], 2)
        
        query_len = math.sqrt(query_len)


        nl = {}

        for token in wt:
            nl[token] = wt[token]/query_len

        return nl



    def create_bigram_tf_idf(self):
        tokens = process_text(self.query)
        tokens = create_bigram(tokens)
        tf = tokens_freqency(tokens)
        total_doc = 37497
        
        wt = {}

        query_len = 0
        for token in tf:
           token_inverted_index = self.database.findById("Bigram_index",token)
           if token_inverted_index == None:
                continue
           df = len(token_inverted_index["data"])


           idf = math.log10(total_doc/df)
           tf_wt = math.log10(tf[token]) + 1
           wt[token] = tf_wt * idf
           query_len += math.pow(wt[token], 2)
        query_len = math.sqrt(query_len)

        nl = {}

        for token in wt:
            nl[token] = wt[token]/query_len

        return nl

    def findRankedResults(self):
        query_nl = self.create_tf_idf()
        bigram_query_nl = self.create_bigram_tf_idf()

        results = {}

        # cosine similarity 
        for token in query_nl:
            print(token)
            token_inverted_index = self.database.findById("Inverted_index",token)
            if token_inverted_index == None:
                continue
            data = token_inverted_index["data"]

            for doc_id in data:
                doc = data[doc_id]
                if doc_id in results:
                    results[doc_id] += (query_nl[token] * doc["nl"])*0.4
                else:
                    results[doc_id] = (query_nl[token] * doc["nl"])*0.4

                results[doc_id] += (doc["imp"]/10)*0.2

        # bigram cosine similarity
        for token in bigram_query_nl:
            token_inverted_index = self.database.findById("Bigram_index", token)
            if token_inverted_index == None:
                continue
            data = token_inverted_index["data"]

            for doc in data:
                if doc in results:
                    results[doc] += (bigram_query_nl[token] * data[doc])*0.4
                else:
                    results[doc] = (bigram_query_nl[token] * data[doc])*0.4

        return dict(sorted(results.items(), key=lambda item: item[1],reverse=True))


   
    
    
    
