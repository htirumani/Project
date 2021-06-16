import datetime
import json
import pymongo

sy, sm, sd = 2021, 5, 31
ey, em, ed = 2021, 6, 16

start_date = datetime.datetime(sy, sm, sd)
end_date = datetime.datetime(ey, em, ed + 1)  # want to populate specified end date hence ed+1

user = 2
device = 1
height = 72   # inches
weight = 185  # lbs

delta = datetime.timedelta(minutes=1)

docs = []
while start_date != end_date:
    docs.append({
        'user': user,
        'device': device,
        'datetime': start_date,
        'height': height,
        'weight': weight
    })
    start_date = start_date + delta

print('Pushing Data to Database...')

client = pymongo.MongoClient("mongodb+srv://max:iotreu2021@cluster0.bkddq.mongodb.net/wearabledb?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs='CERT_NONE')
db = client.wearabledb
collection = db.body
collection.insert_many(docs, ordered=False)

print('Success')