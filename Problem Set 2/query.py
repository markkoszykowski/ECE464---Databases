# Mark Koszykowski
# ECE464 - Problem Set 2
# Querying Code

from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb+srv://root:ece464@idmb.zqkw5.mongodb.net/admin')
db = client.reviews

# How many reviews of each rating
query1 = db.The_Shawshank_Redemption.aggregate([
    {"$project" : {"ratingOutof10" : 1, "_id" : 0}},
    {"$group" : {"_id" : "$ratingOutof10", "count" : {"$sum" : 1}}},
    {"$sort" : {"_id" : 1}}
])

for query in query1:
    pprint(query)
print()

# Newest review
query2 = db.The_Shawshank_Redemption.find({},
    {"title" : 1, "ratingOutof10" : 1, "date" : 1, "reviewLink" : 1}).sort(
    [("date.year", -1), ("date.month", -1), ("date.day", -1)]
).limit(1)

for query in query2:
    pprint(query)
print()

# Review people found most helpful
query3 = db.The_Shawshank_Redemption.find({},
    {"title" : 1, "foundHelpful" : 1, "totalHelpful" : 1, "ratingOutof10" : 1, "reviewLink" : 1}).sort(
    [("foundHelpful", -1)]
).limit(1)

for query in query3:
    pprint(query)
print()

# Review with the longest actual review
query4 = db.The_Shawshank_Redemption.aggregate([
    {"$project" : {"title" : 1, "ratingOutof10" : 1, "reviewLink" : 1, "review_length" : {"$strLenCP" : "$review"}}},
    {"$sort" : {"review_length" : -1}},
    {"$limit" : 1}
])

for query in query4:
    pprint(query)
print()

# Reviews without spoiler warning
query5 = db.The_Shawshank_Redemption.find(
    {"spoiler" : False},
    {"title" : 1, "ratingOutof10" : 1, "reviewLink" : 1}
)

for query in query5:
    pprint(query)