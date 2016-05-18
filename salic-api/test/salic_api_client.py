import requests, json
import threading
import copy


base_address = 'mincserver:8000'
base_version = 'alpha'

uris = [
       	'/projetos/',
        ]

content_types = [
                 "application/json",
                 "application/xml"
                ]


def print_result(response):
	print json.dumps(response.json(), indent=4, sort_keys=True) 

def call_maker(path, headers = {}):

	try:
		response = requests.get(path, headers = headers)
		print 'Call \'%s\' started'%(path)
		#print_result(response)
		print 'Call \'%s\' succesfully done'%(path)
		return response
	except Exception as e:
		print str(e)




calls = []

for uri in uris:
	path = 'http://'+base_address+'/'+base_version+uri
	call = threading.Thread(target=call_maker, args = (path, ))
	calls.append(call)
	calls.append(call)
	calls.append(call)

for call in calls:
	call.start()
