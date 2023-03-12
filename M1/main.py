import sys
from index import Index
import json
from database import Database





if __name__ == "__main__":
    index = Index()
    inverted_index = index.create_inverted_index(sys.argv[1])
    db = Database("SearchEng","Inverted_index")
    db.storeData( inverted_index)

