import os, config

async def get(session, id) :
    url = f"{config.url}/api/v3/requests/{id}"
    headers = {"TECHNICIAN_KEY":os.environ.get('TECHNICIAN_KEY')}

    async with session.get(url, headers=headers) as resp :
        resp = await resp.json()
        return resp