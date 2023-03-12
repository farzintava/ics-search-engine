import lxml
from lxml import html, etree
import json
from lxml import html
from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from lxml.html.clean import Cleaner
import math
from database import Database


import os

bookkeeping_path = "/Users/farzintavakoli/Desktop/CS/Project 3/bookkeeping.json"
webpages_path = "/Users/farzintavakoli/Desktop/CS/webpages"


class Index:

    def __init__(self):
        with open(bookkeeping_path) as bk:
            self.bookkeeping = json.load(bk)
        self.total_doc = len(self.bookkeeping)

    def tokenize(self, text):
        text = text.lower()
        stop_words = set(stopwords.words('english'))
        return [token for token in word_tokenize(text) if not token in stop_words and token.isascii() and token.isalnum()]

    def lemmatize(self, tokens):
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(token) for token in tokens]

    def preprocess_text(self, text):
        tokens = self.tokenize(text)
        lemmatized_tokens = self.lemmatize(tokens)
        return lemmatized_tokens

    def create_inverted_index(self, folder_path):
        inverted_index = {}

        for doc_id in self.bookkeeping:
            with open(f'{folder_path}/{doc_id}', 'rb') as f:
                content = f.read()
                parser = etree.HTMLParser(remove_blank_text=True)
                tree = etree.fromstring(content, parser)

                # doc_id = f"{folder}/{filename}"
                print(doc_id)

                if tree == None:
                    continue
                # Get title, bold and heading tags
                title = self.preprocess_text(
                    " ".join(tree.xpath("//title/text()")))
                bold = self.preprocess_text(" ".join(tree.xpath("//b/text()")))
                h1 = self.preprocess_text(" ".join(tree.xpath("//h1/text()")))
                h2 = self.preprocess_text(" ".join(tree.xpath("//h2/text()")))
                h3 = self.preprocess_text(" ".join(tree.xpath("//h3/text()")))
                a = self.preprocess_text(" ".join(tree.xpath("//a/text()")))

                # Preprocess and tokenize the text
                text = " ".join(tree.xpath(
                    '//text()[normalize-space() and not(ancestor::style) and not(ancestor::script)]')) if tree != None else ""
                tokens = self.preprocess_text(text)

                unique_tokens = set(tokens)

                # Store the position, frequency and importance of each token
                for i, token in enumerate(tokens):
                    if token not in inverted_index:
                        inverted_index[token] = {"df": 0, "docs": []}

                    if len(inverted_index[token]["docs"]) == 0 or inverted_index[token]["docs"][-1]["dID"] != doc_id:

                        inverted_index[token]["df"] += 1
                        inverted_index[token]["docs"].append(
                            {"dID": doc_id, "tf": 1, "pos": [i], "imp": 0.0})
                    else:
                        inverted_index[token]["docs"][-1]["tf"] += 1
                        inverted_index[token]["docs"][-1]["pos"].append(i)

                # Store the importance of each token in the title, bold and heading tags
                for token in unique_tokens:
                    if token in title:
                        inverted_index[token]["docs"][-1]["imp"] += 2.0
                    if token in bold:
                        inverted_index[token]["docs"][-1]["imp"] += 1.5
                    if token in h1:
                        inverted_index[token]["docs"][-1]["imp"] += 1.5
                    if token in h2:
                        inverted_index[token]["docs"][-1]["imp"] += 1.5
                    if token in h3:
                        inverted_index[token]["docs"][-1]["imp"] += 1.5
                    if token in a:
                        inverted_index[token]["docs"][-1]["imp"] += 2.0

                doc_len = 0
                for token in unique_tokens:
                    importance = inverted_index[token]["docs"][-1]['imp']
                    tf_raw = inverted_index[token]["docs"][-1]["tf"]
                    tf_wt = 1 + math.log10(tf_raw)
                    if importance > 0:
                        tf_wt *= (1 + importance/8.0)
                    doc_len += math.pow(tf_wt, 2)
                doc_len = math.sqrt(doc_len)

                for token in unique_tokens:
                    tf_raw = inverted_index[token]["docs"][-1]["tf"]
                    tf_wt = 1 + math.log10(tf_raw)
                    inverted_index[token]["docs"][-1]["nl"] = tf_wt/doc_len

        return inverted_index


    def create_bigram_index(self, folder_path):
        inverted_index = {}

        for doc_id in self.bookkeeping.keys():
            with open(f'{folder_path}/{doc_id}', 'rb') as f:
                content = f.read()
                parser = etree.HTMLParser(remove_blank_text=True)
                tree = etree.fromstring(content, parser)

                # doc_id = f"{folder}/{filename}"
                print(doc_id)

                if tree == None:
                    continue
                
                # Preprocess and tokenize the text
                text = " ".join(tree.xpath(
                    '//text()[normalize-space() and not(ancestor::style) and not(ancestor::script)]')) if tree != None else ""
                tokens = self.preprocess_text(text)
                tokens = create_bigram(tokens)
                unique_tokens = set(tokens)


                doc_len = 0
                # Store the position, frequency and importance of each token
                for  token in unique_tokens:
                    if token not in inverted_index:
                        inverted_index[token] = {}
                    tf_raw = tokens.count(token)
                    tf_wt = 1 + math.log10(tf_raw)
                    doc_len += math.pow(tf_wt, 2)
                    inverted_index[token][doc_id]=tf_wt

                doc_len = math.sqrt(doc_len)
                
                # Normalize
                for token in unique_tokens:
                    tf_wt = inverted_index[token][doc_id]
                    inverted_index[token][doc_id] = tf_wt/math.log10(doc_len)

        return inverted_index


    


def create_bigram(tokens):
    bigrams = []
    for i in range(0, len(tokens)-1):
        bigrams.append(f"{tokens[i]} {tokens[i+1]}")
    return bigrams
