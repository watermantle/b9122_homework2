import re


# helper function, parse function to check if a website has a specific target word
def text_parse(soup, target_word):
    pattern = f'.*?({target_word}).*?'
    for p in soup.find_all('p'):
        text = p.get_text()
        text = text.strip().lower()
        res = re.findall(pattern, text, re.S)
        if len(res) != 0: return True
    return False