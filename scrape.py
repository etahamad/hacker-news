import requests
from bs4 import BeautifulSoup
import pprint

banner = """
 _    _            _               _   _                      _____                                
| |  | |          | |             | \ | |                    / ____|                               
| |__| | __ _  ___| | _____ _ __  |  \| | _____      _____  | (___   ___ _ __ __ _ _ __   ___ _ __ 
|  __  |/ _` |/ __| |/ / _ \ '__| | . ` |/ _ \ \ /\ / / __|  \___ \ / __| '__/ _` | '_ \ / _ \ '__|
| |  | | (_| | (__|   <  __/ |    | |\  |  __/\ V  V /\__ \  ____) | (__| | | (_| | |_) |  __/ |   
|_|  |_|\__,_|\___|_|\_\___|_|    |_| \_|\___| \_/\_/ |___/ |_____/ \___|_|  \__,_| .__/ \___|_|   
                                                                                  | |              
                                                                                  |_|              
"""
print(banner)

res = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

links = soup.select('.titlelink')
links2 = soup2.select('.titlelink')
subtext = soup.select('.subtext')
subtext2 = soup2.select('.subtext')

mega_links = links + links2
mega_subtext = subtext + subtext2


def sort_stories_by_votes(hn):
    return sorted(hn, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 80:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


pprint.pprint(create_custom_hn(mega_links, mega_subtext))
