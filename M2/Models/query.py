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
           df = token_inverted_index["data"]["df"]

           idf = math.log10(total_doc/df)
           tf_wt = math.log10(tf[token]) + 1
           wt[token] = tf_wt * idf
           query_len += math.pow(wt[token], 2)
        
        query_len = math.sqrt(query_len)


        nl = {}

        for token in wt:
            nl[token] = wt[token]/math.log10(query_len)

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

        for token in query_nl:
            print(token)
            token_inverted_index = self.database.findById("Inverted_index",token)
            if token_inverted_index == None:
                continue
            data = token_inverted_index["data"]

            # print(data)
            for doc in data["docs"]:
                if doc["dID"] in results:
                    results[doc["dID"]] += (query_nl[token] * doc["nl"])
                else:
                    results[doc["dID"]] = (query_nl[token] * doc["nl"])

        for token in bigram_query_nl:
            token_inverted_index = self.database.findById("Bigram_index", token)
            if token_inverted_index == None:
                continue
            data = token_inverted_index["data"]

            for doc in data:
                # print("doc is",doc)
                if doc in results:
                    results[doc] += (bigram_query_nl[token] * data[doc])
                else:
                    results[doc] = (bigram_query_nl[token] * data[doc])


        return dict(sorted(results.items(), key=lambda item: item[1],reverse=True))


    # def findRankedResults(self):
    #     query_nl = self.create_tf_idf()

    #     results = {}

    #     for token in query_nl:
    #         print(token)
    #         data = self.database.findById("Inverted_index",token)["data"]
    #         # print(data)
    #         for doc in data["docs"]:
    #             if doc["dID"] in results:
    #                 results[doc["dID"]] += (query_nl[token] * doc["nl"])
    #             else:
    #                 results[doc["dID"]] = (query_nl[token] * doc["nl"])
    #     return dict(sorted(results.items(), key=lambda item: item[1],reverse=True))
    
    
    
