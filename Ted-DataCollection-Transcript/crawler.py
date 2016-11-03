import sys
import urllib.request
from bs4 import BeautifulSoup

__version__ = '0.1'
__project_name__ = 'TedTranscriptExtractor'
__project_link__ = 'http://gist.github.com/786849'

# TED_TALK_URL = 'http://www.ted.com/index.php/talks/'
TED_TALK_URL = ''
def get_html(url):
    request = urllib.request.Request(url)
    request.add_header('User-Agent', '%s/%s +%s' % (
        __project_name__, __version__, __project_link__
    ))
    opener = urllib.request.build_opener()
    return opener.open(request).read()

def main(talk_url,resultlinks):
    if not talk_url.startswith('http://'):
        talk_url = TED_TALK_URL + talk_url

    html = get_html(talk_url)
    # soup = BeautifulSoup(html)
    soup = BeautifulSoup(html,'html.parser')
    # transcript = soup.find_all('div', attrs={'class': 'media__image media__image--thumb talk-link__image'})
    transcript = soup.find_all('a', attrs={'class': 'talk-topics__link'})
    print(transcript)
    for tag in transcript:
        # print('----------',tag)
        # tdTags = tag.find('a')['href']+'/transcript'
        tdTags = tag.text
        print('TD------------',tdTags)
        resultlinks.append(tdTags)
    # return resultlinks

if __name__ == "__main__":
    i=1
    n=2
    all_links = []
    for i in range(1,n+1):
        resultlinks = []
        # talk_url = 'http://www.ted.com/talks?event=tedglobal&page='+str(i)+'&sort=newest'
        talk_url = 'http://www.ted.com/talks/alyssa_monks_how_loss_helped_one_artist_find_beauty_in_imperfection'
        main(talk_url,resultlinks)
        # returnvalues = main(talk_url,resultlinks)
        # print("All links are:",returnvalues)
        # all_links.append(returnvalues)
    # print('Final List of Links',all_links)
    # print('type is:',type(all_links),len(all_links))
    # for arritems in all_links:
    #     for values in arritems:
    #         print(values)
    #         break




