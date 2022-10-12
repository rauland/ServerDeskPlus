import send, report, config
import pandas as pd

domain = config.get()
domain = domain['DEFAULT']['domain']

data = report.getjson("open")
df = pd.json_normalize(data)

category = df.loc[pd.isnull(df['request.category.name'])]
assigned = category.loc[category['request.technician.name'] != None]
techician = assigned['request.technician.name'].unique()
assigned = assigned[['request.id','request.subject','request.requester.name','request.technician.name']]
# assigned.loc[assigned['request.id']]=f"""<a href=f"{domain}/WorkOrder.do?woMode=viewWO&amp;woID={assigned['request.id']}target="_blank"></a>"""

for tech in techician:
    to_email = assigned.loc[assigned['request.technician.name'] == tech]
    tech_email = tech.replace(" ", "")+"@awh.com.au"
    body = to_email.to_html(index=False)
    send.email("⚠️ Unassigned Ticket Categories", body, tech_email, tech)

# <a href=f"{domain}/WorkOrder.do?woMode=viewWO&amp;woID=56966" target="_blank"></a>