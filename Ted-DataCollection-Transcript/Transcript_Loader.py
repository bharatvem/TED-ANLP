import sys
import urllib.request
import csv
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


# !! Important All the chanes are to ne made only below this line ...
def main(talk_url,resultlinks):
    if not talk_url.startswith('http://'):
        talk_url = TED_TALK_URL + talk_url

    print(talk_url)
    try:
        html = get_html(talk_url)
        # soup = BeautifulSoup(html)
        soup = BeautifulSoup(html,'html.parser')
        transcript = soup.find_all('span', attrs={'class': 'talk-transcript__fragment'})
        for tag in transcript:
            tdTags = tag.text
            resultlinks = resultlinks+' '+tdTags.replace('\n',' ')
        return resultlinks
    except:
        print('Error HTML Request Failed for:',talk_url)
        # wronglinks.append(talk_url)
        resultlinks = 'zzz'
        return resultlinks

if __name__ == "__main__":
    with open('correctlinks_new.txt') as f:
        content = f.read().splitlines()
    print(content)
    count = len(content)
    i=0
    wronglinks = []
    correctlinks = []

    for i in range(0,count):
        resultlinks = ''
        # talk_url = 'http://www.ted.com'+content[i]
        talk_url = content[i]
        filename = talk_url.split('talks/',1)[1].split('/transcript',1)[0]+'.txt'
        # filename = 'testfile.txt'
        returnvalues = main(talk_url,resultlinks)
        # print("All links are:",returnvalues)
        if (returnvalues == 'zzz'):
            print('Error for file',talk_url)
            wronglinks.append(talk_url)
        else:
            try:
                file = open(filename,"w")
                file.write(returnvalues)
                file.close()
                correctlinks.append(talk_url)
            except:
                print('Error for file',talk_url)
                wronglinks.append(talk_url)
                continue

    # fname = open('wronglinks_new.txt','w')
    # for item in wronglinks:
    #     fname.write("%s\n" % item)
    # fname.close()
    #
    # fname = open('correctlinks_new.txt','w')
    # for item in correctlinks:
    #     fname.write("%s\n" % item)
    # fname.close()