import sys
import urllib.request
import csv
import pandas as pd
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
def main(talk_url):
    if not talk_url.startswith('http://'):
        talk_url = TED_TALK_URL + talk_url

    print(talk_url)
    resultlinks = ''
    try:
        html = get_html(talk_url)
        # soup = BeautifulSoup(html)
        soup = BeautifulSoup(html,'html.parser')
        transcript = soup.find_all('ul', attrs={'class': 'talk-topics__list'})
        for tag in transcript:
            tdTags = tag.find_all('a')
            for a in tdTags:
                atag = a.text
                topic = atag.replace('\n',' ')
                resultlinks = (resultlinks+','+topic).strip()

        # transcript = soup.find_all('h4', attrs={'class': 'h9'})
        # for tag in transcript:
        #     tdTags = tag.find("a")
        #     Tag_value = tdTags.text
        #     title = Tag_value.replace('\n',' ')
        # resultlinks.append(title)
        #
        # transcript = soup.find_all('span', attrs={'class': 'meta__val'})
        # for tag in transcript:
        #     tdTags = tag.text
        #     posted = tdTags.replace('\n',' ')
        #     break;
        # resultlinks.append(posted)

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
    allcontent = pd.DataFrame( columns=['topics','link','filename'])
    for i in range(0,count):
        # talk_url = 'http://www.ted.com'+content[i]
        talk_url = content[i].split('/transcript',1)[0]
        link = content[i]
        # talk_url = content[i]
        # filename = talk_url.split('talks/',1)[1].split('/transcript',1)[0]+'.txt'
        # filename = 'testfile.txt'
        filename = 'topics.txt'
        fname = talk_url.split('talks/',1)[1].split('/transcript',1)[0]+'.txt'
        returnvalues = main(talk_url)
        returnvalues1 = []
        returnvalues1.append(returnvalues)
        returnvalues1.append(link)
        returnvalues1.append(fname)
        row = []
        row.append(returnvalues1)
        allcontent = allcontent.append(pd.DataFrame(row, columns=['topics','link','filename']),ignore_index=True)
        # allcontent.append(returnvalues)
        # print(allcontent)

        # if (returnvalues == 'zzz'):
        #     print('Error for file',talk_url)
        #     wronglinks.append(talk_url)
        # else:
        #     try:
        #         file = open(filename,"w")
        #         file.write(returnvalues)
        #         file.close()
        #         correctlinks.append(talk_url)
        #     except:
        #         print('Error for file',talk_url)
        #         wronglinks.append(talk_url)
        #         continue
    # fname = open('allcontent.txt','w')
    # for item in allcontent:
    #     fname.write("%s\n" % item)
    # fname.close()

    allcontent.to_csv('topics.csv')
    # fname = open('wronglinks_new.txt','w')
    # for item in wronglinks:
    #     fname.write("%s\n" % item)
    # fname.close()
    #
    # fname = open('correctlinks_new.txt','w')
    # for item in correctlinks:
    #     fname.write("%s\n" % item)
    # fname.close()