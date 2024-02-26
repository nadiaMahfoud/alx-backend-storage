#!/usr/bin/env python3
"""
Python script that provides enhanced stats about Nginx
logs stored in MongoDB:

Database: logs
Collection: nginx
Display (same as the example):
first line: x logs where x is the number of documents in this collection
second line: Methods:
5 lines with the number of documents with the method =
["GET", "POST", "PUT", "PATCH", "DELETE"] in this order
(see example below - warning: it’s a tabulation before each line)
one line with the number of documents with:
method=GET
path=/status
third line: IPs:
10 lines with the number of documents with the IP
in descending order (like the example below)
"""

import pymongo
from pymongo import MongoClient

def log_nginx_stats(mongo_collection):
    """provides enhanced stats about Nginx logs"""
    # Display the total number of logs
    print(f"{mongo_collection.estimated_document_count()} logs")

    # Display the number of logs for each HTTP method
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Display the number of logs with method=GET and path=/status
    number_of_gets = mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{number_of_gets} status check")

    # Display the top 10 most present IPs in descending order
    print("IPs:")
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = mongo_collection.aggregate(pipeline)
    for ip_info in top_ips:
        ip = ip_info["_id"]
        count = ip_info["count"]
        print(f"\t{ip}: {count}")

if __name__ == "__main__":
    mongo_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    log_nginx_stats(mongo_collection)

