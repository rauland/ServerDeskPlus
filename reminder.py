import send, report, config
import pandas as pd

data = report.getjson("open")
df = pd.json_normalize(data)

category = df.loc[pd.isnull(df['request.category.name'])]
assigned = category.loc[category['request.technician.name'] != None]
technician = assigned['request.technician.name'].unique()
technician = technician[~pd.isnull(technician)]
assigned = assigned[['request.id','request.subject','request.requester.name','request.technician.name']]

for assign in assigned['request.id']:
    assigned['request.id'].loc[assigned['request.id'] == assign] = f"""<a href="{config.url}/WorkOrder.do?woMode=viewWO&amp;woID={assign}">{assign}</a>"""

for tech in technician:
    to_email = assigned.loc[assigned['request.technician.name'] == tech]
    tech_email = tech.replace(" ", "")+f"{config.at}"
    body = to_email.to_html(index=False, escape=False)
    send.email("⚠️ Unassigned Ticket Categories", body, tech_email, tech)
