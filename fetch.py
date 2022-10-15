import requests, os, json, time, aiohttp, asyncio
import ticket, config, search

url = f"{config.url}/api/v3/requests"
headers = {"TECHNICIAN_KEY": os.environ.get("TECHNICIAN_KEY")}
# today = epoch.datetime.datetime.today().strftime('%m-%d-%Y')

# This generates the SD request based of parms object and returns response as dict
def getresponse(query):
    data = search.query(query)
    print(data)
    params = {"input_data": json.dumps(data)}
    response = requests.get(url, headers=headers, params=params)
    time.sleep(1.5)
    return response.json()


def getids(choice, prevmonth=1, fields_required="[id]"):
    request_ids = []
    query = search.Parms(
        month=prevmonth, choice=choice, fields_required=fields_required
    )
    response = getresponse(query)

    while True:
        for request in response["requests"]:
            request_ids += [request["id"]]

        query.start_index = query.start_index + query.row_count

        if not response["list_info"]["has_more_rows"]:
            break
        response = getresponse(query)

    print("Total Count:")
    print(response["list_info"]["total_count"])

    return request_ids


# Accepts ID list, requests tickets simultaneously, returns as list
async def tickets(request_ids):
    async with aiohttp.ClientSession() as session:

        tasks = []
        for id in request_ids:
            tasks.append(asyncio.ensure_future(ticket.get(session, id)))

        request_list = await asyncio.gather(*tasks)
        return request_list
