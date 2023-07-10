import requests
import re


# return YouTube channel id via handle or False if failed
def scraping_get_channel_id_from_handle(handle: str):
    if handle.find('@') == -1:
        handle = '@' + handle

    url = 'https://www.youtube.com/' + handle
    resp = requests.get(url)
    print(resp)
    if resp.status_code == 200:
        channel_id = re.findall('<meta itemprop="identifier" content="([^"]*)"', resp.text)
        channel_name = re.findall('<meta itemprop="name" content="([^"]*)"', resp.text)
        return channel_id, channel_name
    else:
        return False


channel_id, channel_name = scraping_get_channel_id_from_handle('@thesecondloft')
print(channel_id)
print(channel_name)

