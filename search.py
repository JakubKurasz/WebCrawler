#Get page
import requests as r
import re
from bs4 import BeautifulSoup
import os
import time
import nltk #have to pip install nltk
from urllib.parse import urljoin
#nltk.download('stopwords')
from nltk.corpus import stopwords

all_urls = []
urls_searched = []
url_frontier = []
d = {}
base_url = "https://Quotes.toscrape.com"
class webScraper:
    def Scrape(url, pageNumber, d):
        print(url)
        urls_searched.append(url)
        response = r.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            absolute_url = urljoin(base_url, href)
            if absolute_url not in all_urls and base_url in absolute_url:
                all_urls.append(absolute_url)
                url_frontier.append(absolute_url)
        s = soup.get_text()
        s = re.findall(r'\b\w+\b', s.lower())
        filtered_words = [word for word in s if word not in stopwords.words('english')]
        for x in range(len(filtered_words)):
            word = filtered_words[x]
            if word.isdigit() == True or len(word) < 3:
                continue
            if (word, pageNumber) in d:
                d[word, pageNumber].append(x)
            else:
                d[word, pageNumber] = [x]
        return d
    def search(phrase, d, urls_searched):
        #split input into list, with each element containing a word
        p = phrase.split()
        DocumentsPerWord = [[] for _ in range(len(p))]
        PositionsPerWordPerPage = [[] for _ in range(len(p))]
        #creates list with the corresponding documents for each word
        keys = d.keys()

        for x in range(len(p)):
            word = p[x]
            for element in keys:
                if element[0] == word:
                    DocumentsPerWord[x].append(element[1])
                    PositionsPerWordPerPage[x].append(d[element])
        if len(DocumentsPerWord) == 0:
            print("sorry no matches for that query")
            return
        elif len(DocumentsPerWord[0]) == 0:
            print("sorry no matches for that query")
            return
        uniqueDocuments = []
        uniqueDocuments += DocumentsPerWord[0]
        #gathers a list of unique potential documents
        for x in range(len(DocumentsPerWord)):
            for word in DocumentsPerWord[x]:
                if word not in uniqueDocuments:
                    uniqueDocuments.append(word)
        WordIntersectionsPerDocument = []
        #check the number of intersections between words per document
        for y in range(len(uniqueDocuments)):
            count = 0
            for x in range(len(DocumentsPerWord)):  
                if uniqueDocuments[y] in DocumentsPerWord[x]:
                    count +=1
            WordIntersectionsPerDocument.append(count)  
        #finds the Documents with the highest number of intersections 
        maximum =max(WordIntersectionsPerDocument)
        DocumentsOrderedByIntersections = []
        for y in range(maximum-1):
            for x in range(len(WordIntersectionsPerDocument)):
                if WordIntersectionsPerDocument[x] == maximum - y:
                    DocumentsOrderedByIntersections.append(uniqueDocuments[x])
        
        #creates a list of the final documents, with the positions of each word in each document
        positionsPerPagePerWord = [[] for _ in range(len(DocumentsOrderedByIntersections))]
        for x in range(len(DocumentsOrderedByIntersections)):
            for y in range(len(p)):
                if (p[y], DocumentsOrderedByIntersections[x]) in keys:
                    positionsPerPagePerWord[x].append(( d[p[y], DocumentsOrderedByIntersections[x]]))
        #subtracts from the position count the difference between itself and the starting position
        for z in range(len(DocumentsOrderedByIntersections)):
            for x in range(1,len(positionsPerPagePerWord[z])):
                for y in range(len(positionsPerPagePerWord[z][x])):
                    positionsPerPagePerWord[z][x][y] -= x    
        #for each page calculates the number of words that are next to each other  
        DocumentsFinalIndex = []
        DocumentsRunnerUps = [[] for _ in range(len(p)-1)]
        UniquePositionsPerDocument = [[] for _ in range(len(DocumentsOrderedByIntersections))]
        for y in range(len(DocumentsOrderedByIntersections)):
            #calculates the positions for each word in a page
            for x in range(len(positionsPerPagePerWord[y])):
                for element in positionsPerPagePerWord[y][x]:
                    if element not in UniquePositionsPerDocument[y]:
                        UniquePositionsPerDocument[y].append(element)
        #calculates the largest sequence of words and appends the Documents with larges sequence first
        for x in range(len(UniquePositionsPerDocument)):
            if len(p) == 1: 
                break
            count = 0
            for y in range(len(positionsPerPagePerWord[x])):
                for z in range(len(UniquePositionsPerDocument[x])):
                    if  UniquePositionsPerDocument[x][z] in positionsPerPagePerWord[x][y]:
                        count +=1
                    if count == len(p) and DocumentsOrderedByIntersections[x] not in DocumentsFinalIndex:
                        DocumentsFinalIndex.append(DocumentsOrderedByIntersections[x])
                    for b in range(1,len(p)):
                        if count == len(p) - b and DocumentsOrderedByIntersections[x] not in (DocumentsFinalIndex or DocumentsRunnerUps[b-1]): 
                            DocumentsRunnerUps[b-1].append(DocumentsOrderedByIntersections[x])
        #adds remaining elements that contain the words
        for x in range(len(DocumentsRunnerUps)):
            for element in DocumentsRunnerUps[x]:
                if element not in DocumentsFinalIndex:
                    DocumentsFinalIndex.append(element) 
        LastDocuments = []
        for element in uniqueDocuments:
            if element not in DocumentsFinalIndex:
                LastDocuments.append(element)
        LastDocumentsFreq = []
        for x in range(len(LastDocuments)):
            count = 0
            for y in range(len(p)):
                    if LastDocuments[x] in DocumentsPerWord[y]:
                        count += len(d[p[y], LastDocuments[x]])
                        count += 50
            LastDocumentsFreq.append(count)
        maxFreq = 1
        if len(LastDocumentsFreq)!=0:maxFreq = max(LastDocumentsFreq)
        for y in range(maxFreq + 1):
            for x in range((len(LastDocumentsFreq))):
                if LastDocumentsFreq[x] == maxFreq - y:
                    DocumentsFinalIndex.append(LastDocuments[x])
        for Document in DocumentsFinalIndex:
            print(urls_searched[Document])         
        #if present in document, check positions
        
w = webScraper

def main():
    url = ''
    while True:
        command = input("enter a command")
        command = command.split()
        if command[0] == 'build':
            d = {}
            urls_searched = []
            w.Scrape("https://quotes.toscrape.com/",0,d) 
            p =1
            while len(url_frontier) > 0:
                w.Scrape(url_frontier.pop(),p,d)
                print("The size of the frontier is {0}".format( len(url_frontier)))
                p+=1
                print("The size of the total urls found is {0}".format(len(all_urls)))
                time.sleep(6)
            with open(r'Index.txt','w+') as f:
                f.write(str(d))
            with open(r'urls.txt','w+') as f:
                f.write(str(urls_searched))
        elif command[0] == 'load':
            with open(r'Index.txt','r') as f:
                for i in f.readlines():
                    dic=i #string
            d = eval(dic)
            with open(r'urls.txt','r') as f:
                for i in f.readlines():
                    urls=i #string
            urls_searched = eval(urls)
        elif command[0] == 'print':
            keys = d.keys()
            search = command[1].lower()
            for x in range(len(urls_searched)):
                if (search, x) in keys:
                    print("positions of {0} in the inverted index for page number {1}: {2} This corresponds to the url {3}".format(search,x,d[search, x], urls_searched[x]))
        elif command[0] == 'find':
            searchList = command[1:]
            search = ""
            for word in searchList:
                search += " {0}".format(word)
            search = search.lower()
            w.search(search, d, urls_searched)
            print("The urls with the highest score appear at the top")
        elif command[0] == 'Q':
            return

if __name__ == "__main__":
    main()