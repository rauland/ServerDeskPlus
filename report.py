import json, asyncio
import fetch


def getjson(query, months=1, prevmonth=1, idonly=False):
    request_list = []
    for i in range(months):
        request_list += fetch.getids(query, prevmonth=i + prevmonth)

    if idonly:
        return request_list
    else:
        return asyncio.run(fetch.tickets(request_list))


def reportquery(prevmonth = 1):
    ids = []
    ids += getjson("open", idonly=True,prevmonth=prevmonth)
    ids += getjson("created", months=13, idonly=True,prevmonth=prevmonth)
    ids += getjson("closed", months=13, idonly=True,prevmonth=prevmonth)

    ids = list(set(ids))

    data = asyncio.run(fetch.tickets(ids))

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
