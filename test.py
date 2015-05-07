import pymongo
import json
import random

try:
    conn = pymongo.MongoClient("ds031862.mongolab.com", 31862)
    db = conn["teamrosa"]
    db.authenticate("admin", "password")
    print "Connected Successfully!!"
except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e

readings = db.readings

for x in range(0, 3):
	data = {}
	data['ip'] = '213.159.191.221'
	data['temp'] = str(random.randint(24, 32))
	json_data = json.dumps(data)
	json_data = json.loads(json_data)
	readings.insert(json_data)
	print "Inserted readings"
