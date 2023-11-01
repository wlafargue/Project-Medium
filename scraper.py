from bs4 import BeautifulSoup as bs
import requests

def scrape(url):
    """ Web scrapping with BeautifulSoup.

    Args:
        url (str): webpage url
    
    Returns:
        data (dict): dictionary containing lists of titles, texts, 
                     pictures, authors and authors' photo
    
    """
    response = requests.get(url)
    soup = bs(response.content, "lxml")

    # Titles
    titles = [title.text 
              for title in soup.find_all('h2', 'be if ig ih ii ij ik il' + \
              ' im in io ip gu gv iq ir gw is it iu iv iw ix ' + \
              'iy iz ja jb gh gg hz ib id bj')]

    # Texts
    texts = [text.text for text in soup.find_all('h3')]

    # Pictures
    pictures = []
    block = soup.find('div', "hd he hf l")
    for div in block.find_all('div', {"class": "ab"}):
        if div.find('div', 'l er ie'): 
            if div.find('img', "bw lh"):
                img = div.find('img', "bw lh")
                if img['src'] not in pictures:
                    pictures.append(img['src'])
            else:
                pictures.append(None)

    # Authors
    authors = []
    for author in soup('div', 'ff fg hm hn ho ab'):
        authors.append(author.find_all('a', "af ag ah ai aj ak al am an ao ap aq ar hx ab q")[0].text)

    # Authors' photo
    photos = [img['src'] for img in soup.find_all('img', "l hv bx hq hr ec")]

    # Original webpage of articles
    hrefs = []
    for article in soup.find_all('div', "ab"):
        a = article.find_all('a', "af ag ah ai aj ak al am an ao ap aq ar as at")
        if len(a) > 0:
            h = a[0].find('h2')
            if h is not None:
                hrefs.append('https://medium.com'+a[0]['href'])

    # Minutes for reading
    min_read = []
    for article in soup.find_all('div', 'jg jh ji jj jk ab q'):
        for span in article.findAll('span'):
            if 'read' in span.text:
                min_read.append(int(span.text.split()[0]))
                

    # Published date
    date = []
    for article in soup.find_all('div', 'jg jh ji jj jk ab q'):
        for span in article.children:
            if ' read' not in span.text and len(span.text)> 2:
                date.append(span.text)

    data = {
        'titles' : titles,
        'texts' : texts,
        'pictures' : pictures,
        'authors' : authors,
        'photos' : photos,
        'hrefs': hrefs,
        'min_read': min_read,
        'date': date
    }

    return data
