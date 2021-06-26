from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from gingerit.gingerit import GingerIt
import re

def getDataFromUrl(url, whole):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # body = soup.find('body').text.replace('\n', ' ').replace('\r', '').text.strip()
    # body = soup.find("div", class_="main-content").text.split('\n')
    body = soup.find("body").text.split('\n')
    correctionFor = []
    print("Finding for "+str(url))
    # print(body)
    correctionForUrl = getCorrect(body)
    if correctionForUrl:
        appendData = {
            'url' : url,
            'urlResult' : correctionForUrl
        }
        correctionFor.append(appendData)
    return correctionFor


def getCorrect(body):
    correctionsList = []
    for txt in body:
        if txt:
            textFilter = txt.strip()
            textFilter = re.sub('[!@#$]*', '', textFilter)
            parser = GingerIt()
            x=550 
            res=[textFilter[y-x:y] for y in range(x, len(textFilter)+x,x)]
            for textToFilter in res:
                result = parser.parse(textToFilter)
                if result['corrections']:
                    correctionsList.append(result)
            # break
    return correctionsList
    

def checkIt(req):
    if 'url' in req.GET:
        url = req.GET.get('url')
        whole = req.GET.get('whole')
        correctionDetail = getDataFromUrl(url, whole)
        # print(correctionDetail)
        context = {
            'mainUrl' : url,
            'whole' : whole,
            'correctionDetail' : correctionDetail
        }
        return render(req,'checkSpell.html', context=context)
    else:
        context = {
            'mainUrl' : "",
            'whole' : "1"
        }
        return render(req,'checkSpell.html', context=context)
