from elasticsearch import Elasticsearch


class Es(object):
    def __init__(self,start_date=None,end_date=None):
        self.es = Elasticsearch([{'host':'192.168.79.141','port':9200}])
        self.start_date = start_date
        self.end_date = end_date

        self.query_all =  {'query':
              {'match_all': {}
               }
          }

        self.query_page = {'query':
                              {'match_all': {}
                               },
                           "from": self.start_date,
                           "size": self.end_date
                          }

        self.time_1m = {'query':
            {"range": {
                'timestamp': {'gt': 'now-1m'}
                }

            }
          }

        self.time_quantum = {'query':
                    {"range": {
                        'timestamp':{
                            "gt" : "{}T{}:30:00".format("2019-05-29","16"),
                            "lt": "{}T{}:37:59".format("2019-05-29","16"),
                            "time_zone": "Asia/Shanghai"
                            }
                        }
                    }
                }

        self.term =  {'query':
              {'term': {'type':'chq'}
               }
          }

        self.bool_query = {
              "query": {
                "bool": {
                  "must": [
                    { "match": { "type":'chq'}}
                  ],
                  "filter": [
                    { "range": {
                        'logdate':{
                            "gt" : "{}T{}:02:01".format("2018-10-09","00"),
                            "lt": "{}T{}:02:03".format("2018-10-09","00"),

                            }
                        }}
                  ]
                }
              }
            }

    def search(self,index,body,**args):
        ret = self.es.search(index=index,body=body,**args)
        return ret

    def count(self,index):
        ret = self.es.count(index=index)
        return ret

if __name__ == '__main__':


    Ess = Es(2,2)
    # ret = Ess.search(index='chq-2019.06.09',body=Ess.query_all,size=20,sort='logdate:desc')
    ret = Ess.search(index='chq-2019.06.09',body=Ess.query_page)
    #
    #
    #
    # # print (ret)
    # # print (ret['hits']['hits'])
    for i in ret['hits']['hits']:

        print (i['_source']['message'])

    # es = Elasticsearch([{"host": '192.168.79.141', "port": "9200"}])
    #
    #
    # page = es.search(
    #     index='chq-2019.06.09',
    #
    #     scroll='2m',
    #     size=1000,
    #     body={
    #         "query": {
    #             "match_all": {}
    #         }
    #     }
    # )
    #
    # sid = page['_scroll_id']
    # scroll_size = page['hits']['total']
    # print (scroll_size)
# Start scrolling
# while (scroll_size > 0):
#     print ("Scrolling...")
#     page = es.scroll(scroll_id=sid, scroll='2m')
#     # Update the scroll ID
#     sid = page['_scroll_id']
#     # Get the number of results that we returned in the last scroll
#     scroll_size = len(page['hits']['hits'])
#     print ("scroll size: " + str(scroll_size))
