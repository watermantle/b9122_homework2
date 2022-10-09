# parse function to check if a website has a specific target word
def text_parse(soup, target_word):
    pattern = f'.*?({target_word}).*?'
    for p in soup.find_all('p'):
        text = p.get_text()
        text = text.strip().lower()
        res = re.findall(pattern, text, re.S)
        if len(res) != 0: return True
    return False

# program to crawl 20 urls that contain key word "charges"
import urllib.request
import re
from bs4 import BeautifulSoup


base_sec = "https://www.sec.gov"
seed_ulr_sec = "https://www.sec.gov/news/pressreleases"
urls_sec = []
res2 = []

response = urllib.request.Request(seed_ulr_sec, headers=headers)
webpage = urllib.request.urlopen(response).read()
soup = BeautifulSoup(webpage, 'lxml')

for url in soup.find_all('a', attrs={"hreflang" : "en"}, href=True):
    sub_url = base_sec + url['href']
    try:
        req = urllib.request.Request(sub_url, headers=headers)
        webpage = urllib.request.urlopen(req).read()

    except Exception as ex:
        print("Unable to access= " + sub_url)
        print(ex)
        continue
    soup = BeautifulSoup(webpage)
    
    # check if the website has charges
    if text_parse(soup, 'charges'):
        res2.append(sub_url)
    if len(res2) == 20: break