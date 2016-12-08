# Statuspageio

Python script that let's you create/update/delete realtime incident to your statuspage.io dashboard

# Configuration:
statuspage_url =

api_token = 

api_header =

statuspage_id =

# Use:
 - python statuspage.py --create --name 'PO: PHX phone in SFO down' --message 'we are currently investing the issue. 100 people affected.' --status 'investigating'
 - python statuspage.py --update --name 'PO: PHX phone in SFO down' --message 'rebooted phone switch' --status 'resolved'
 - python statuspage.py --delete --incident_id 'hfhg95p1jzyj'
 
