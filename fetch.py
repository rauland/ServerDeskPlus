import requests, os, json, time, aiohttp, asyncio
import ticket, epoch, config
from default import Parms

domain = config.get()
url = f"{domain['DEFAULT']['url']}/api/v3/requests"
headers = {"TECHNICIAN_KEY":os.environ.get('TECHNICIAN_KEY')}
today = epoch.datetime.datetime.today().strftime('%m-%d-%Y')

# Input data for SD query
def query(d) :
    match d.choice:
        case 'open':
            data ={
                "list_info": {
                    "row_count": d.row_count,
                    "start_index": d.start_index,
                    "sort_field": "id",
                    "sort_order": "desc",
                    "get_total_count": True,
                    "fields_required":d.fields_required,
                    "filter_by": {
                        "name": "Open_System"
                    },
                }
            }
        case 'created':
            data ={
                "list_info": {
                    "row_count": d.row_count,
                    "start_index": d.start_index,
                    "sort_field": "id",
                    "sort_order": "desc",
                    "get_total_count": True,                    
                    "fields_required":d.fields_required,
                    "search_criteria": [{
                        "field": "created_time",
                        "condition": "greater than",
                        "value": epoch.getlastdate(1, d.month),                        
                        },
                        {
                        "field": "created_time",
                        "condition": "lesser than",
                        "value": epoch.getlastdate(1, d.month - 1),
                        "logical_operator" : "and"                        
                        }
                    ]
                }
            }
        case 'closed':
            data = {
                "list_info": {
                    "row_count": d.row_count,
                    "start_index": d.start_index,
                    "sort_field": "id",
                    "sort_order": "desc",
                    "get_total_count": True,                    
                    "fields_required":d.fields_required,
                    "search_criteria": [{
                        "field": "resolved_time",
                        "condition": "greater than",
                        "value": epoch.getlastdate(1, d.month),                        
                        },
                        {
                        "field": "resolved_time",
                        "condition": "lesser than",
                        "value": epoch.getlastdate(1, d.month - 1),
                        "logical_operator" : "and"                        
                        }
                    ]
                }
            }
        case 'all':
            data ={
                "list_info": {
                    "row_count": d.row_count,
                    "start_index": d.start_index,
                    "sort_field": "id",
                    "sort_order": "desc",
                    "get_total_count": True,                    
                    "fields_required":d.fields_required,
                    "search_criteria": [{
                        "field": "created_time",
                        "condition": "greater than",
                        "value": epoch.getlastdate(1, d.month),                        
                        },
                    ]
                }
            }          
    return data

# This generates the SD request based of parms object and returns response as dict
def getresponse(d) :
    data = query(d)
    print(data)
    params = {'input_data': json.dumps(data)}
    response = requests.get(url,headers=headers, params=params)
    time.sleep(1.5) 
    return response.json()

def getids(choice, prevmonth = 1, fields_required = '[id]'):
    request_ids = []
    d = Parms(month=prevmonth, choice=choice, fields_required=fields_required)
    response = getresponse(d)
           
    while True:       
        for request in response['requests']:
            request_ids += [request['id']]
                    
        d.start_index = d.start_index + d.row_count
        
        if not response['list_info']['has_more_rows']:
            break
        response = getresponse(d)
    
    print ('Total Count:')
    print (response['list_info']['total_count'])

    return request_ids

# Accepts ID list, requests tickets simultaneously, returns as list
async def tickets(request_ids) :
    async with aiohttp.ClientSession() as session :   
        
        tasks = []
        for id in request_ids :
            tasks.append(asyncio.ensure_future(ticket.get(session, id)))
            
        request_list = await asyncio.gather(*tasks)
        return request_list