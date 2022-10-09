# helper function, parse function to check if a website has a specific target word
def text_parse(soup, target_word):
    pattern = f'.*?({target_word}).*?'
    for p in soup.find_all('p'):
        text = p.get_text()
        text = text.strip().lower()
        res = re.findall(pattern, text, re.S)
        if len(res) != 0: return True
    return False


import urllib.request
import re
from bs4 import BeautifulSoup


# To crawl some pages that contains keyword: coivd
# collect newsevents related website
base = "https://www.federalreserve.gov"
seed_url = "https://www.federalreserve.gov/newsevents/pressreleases.htm"
urls_newsevents = []
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = urllib.request.Request(seed_url, headers=headers)
webpage_main = urllib.request.urlopen(response).read()

urls_newsevents = []
soup = BeautifulSoup(webpage_main, 'lxml')
url_as = soup.find_all('a', href=True)
for url_a in url_as:
    url = url_a['href']
    if url[:26] == "/newsevents/pressreleases/":
        urls_newsevents.append(url)

# check if the url contains covid
res1 = []
while len(res1) < 10 and urls_newsevents:
    try:
        curr_url = base + urls_newsevents.pop(0)
        req = urllib.request.Request(curr_url, headers=headers)
        webpage = urllib.request.urlopen(req).read()

    except Exception as ex:
        print("Unable to access = " + curr_url)
        print(ex)
        continue
        
    soup = BeautifulSoup(webpage)
    for url in soup.find_all('a', href=True):
        url = url['href']
        if url[:26] == "/newsevents/pressreleases/":
            try:
                sub_url = base + url
                print(f"working on {sub_url}")
                req = urllib.request.Request(sub_url, headers=headers)
                webpage = urllib.request.urlopen(req).read()
                soup = BeautifulSoup(webpage)
                if text_parse(soup, 'covid'):
                    res1.append(sub_url)
            except Exception as ex:
                print("Unable to access = " + sub_url)
                print(ex)
                continue



