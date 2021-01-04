import urllib3
import requests
import facebook


token = "147067070355584|jmOMnn2brOXsE0RTmeuvqsc5JYA"
graph = facebook.GraphAPI(access_token=token, version=3.1)
events = graph.request('/search?q=Poetry&type=event&limit=10000')
eventList = events['data']
eventid = eventList[1]['id']
event1 = graph.get_object(id=eventid,
fields='attending_count,can_guests_invite,category,cover,declined_count,description,end_time,guest_list_enabled,interested_count,is_canceled,is_page_owned,is_viewer_admin,maybe_count,noreply_count,owner,parent_group,place,ticket_uri,timezone,type,updated_time')
attenderscount = event1['attending_count']
declinerscount = event1['declined_count']
interestedcount = event1['interested_count']
maybecount = event1['maybe_count']
noreplycount = event1['noreply_count']
attenders = requests.get("https://graph.facebook.com/v2.7/"+eventid+"/attending?access_token="+token+"&limit="+str(attenderscount))
attenders_json = attenders.json()
admins = requests.get("https://graph.facebook.com/v2.7/"+eventid+"/admins?access_token="+token)
admins_json = admins.json()