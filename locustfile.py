import time
import datetime
from locust import User, task, constant, tag
import pymongo
from time import perf_counter
from bson import json_util
from bson.json_util import loads
from bson import ObjectId
import re

class Mongouser(User):
    client = pymongo.MongoClient("mongodb+srv://main_admin:bugsyBoo@migratedemo2.vmwqj.mongodb.net/ek?retryWrites=true&w=majority&readPreference=secondary")
    db = client.clinical

    @tag('lucene')
    @task(5)
    def lucene(self):
        print('lucene')
        try: 
            tic = time.time();
            output = self.db.emr.aggregate([
          {"$search": {
            "compound" : {
              "should" : [
                  {"regex" : {"query" : "metastatic(\s|-)+thyromegaly", "path" : "illness_history", "allowAnalyzedField": True}},
                  {"regex" : {"query" : "thyromegaly(\s|-)+(2[-\s]*)?methoxyestradiol", "path" : "illness_history", "allowAnalyzedField": True}},
                  {"regex" : {"query" : "(2[-\s]*)?methoxyestradiol", "path" : "illness_history", "allowAnalyzedField": True}}
                ]
            }
          }},
          {"$project": {"score": {"$meta": "searchScore"},"patient_id": 1, "referring_physician": 1, "age": 1, "term": "metastaticthyromegaly_2-methoxyestradiol", "illness_history": 1}}
        ])
            # output = self.db.study.find_one()
            self.environment.events.request_success.fire(request_type="pymongo", name="lucene", response_time=(time.time()-tic), response_length=0)
        except KeyboardInterrupt:
            print
            sys.exit(0)
        except Exception as e:
            print(f'{datetime.datetime.now()} - DB-CONNECTION-PROBLEM: '
                  f'{str(e)}')
            connect_problem = True
    
    @task(4)
    def regex(self):
        print('regex')
        try: 
            tic = time.time()
            output = self.db.emr.aggregate([
          {"$match": {"mentions" : {"$in":
            [
                re.compile("metastatic(\s|-)+thyromegaly"),
                re.compile("thyromegaly(\s|-)+(2[-\s]*)?methoxyestradiol"),
                re.compile("(2[-\s]*)?methoxyestradiol")
              ]
          }}},
          {"$project": {"patient_id": 1, "referring_physician": 1, "age": 1, "term": "hyromegaly_2-methoxyestradio", "mentions": 1}},
          {"$limit": 2000}
        ])
            # output = self.db.study.update_one({ "environment_oid":"PROD" },{'$set' : {'status' : 'True'}})
            self.environment.events.request_success.fire(request_type="pymongo", name="regex", response_time=(time.time()-tic), response_length=0)
        except KeyboardInterrupt:
            print
            sys.exit(0)
        except Exception as e:
            print(f'{datetime.datetime.now()} - DB-CONNECTION-PROBLEM: '
                 f'{str(e)}')
            connect_problem = True

    @task(1)
    def update(self):
        print('update')
        try:
            tic = time.time()
            output = self.db.emr.update_many({"mentions": r"^Support\saffect"}, {'$set' : {'version' : '1.1'}})
            # obj = {"nm":"ek","text": "Another post!","environment_oid":"PROD"}
            # output = self.db.study.insert_one(obj)
            self.environment.events.request_success.fire(request_type="pymongo", name="update", response_time=(time.time()-tic), response_length=0)
        except KeyboardInterrupt:
            print
            sys.exit(0)
        except Exception as e:
            print(f'{datetime.datetime.now()} - DB-CONNECTION-PROBLEM: '
                f'{str(e)}')
            connect_problem = True
