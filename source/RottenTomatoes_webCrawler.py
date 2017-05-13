import re
from bs4 import BeautifulSoup
import time
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def name_to_tag(name):
    tag = str.lower(name)
    tag = tag.replace(' ', '_')
    return tag


# name = input("Please input the actor/actress: ")  # type 'Zhang Ziyi'
# movie_tag = name_to_tag(name)
# url = "https://www.rottentomatoes.com/celebrity/%s" % movie_tag

url = "https://www.rottentomatoes.com/celebrity/zhang_ziyi"
source_code = requests.get(url)  #
soup = BeautifulSoup(source_code.text, 'lxml')
list_soup = soup.find('tbody')
title_dict = {}
href_dict = {}
rating_dict = {}
i = 0
for movie_info in list_soup.findAll('tr'):
    title = movie_info.find('a', {'class': 'unstyled articleLink'}).string.strip()
    title = str(title)
    title_dict[i] = title
    i += 1
i = 0
for movie_info in list_soup.findAll('a'):
    href = movie_info.get('href')
    href = str(href)
    href_dict[i] = href
    i += 1
i = 0
for movie_info in list_soup.findAll('span'):
    rating = movie_info.get('data-rating')
    if rating is not None:
        rating = int(rating)
        rating_dict[i] = rating
        i += 1

best_mov = {}  # movie title: rating
best_intro = {}  # movie title: introduction
best_info = {}  # movie title: movie info
info = []


def find_GenreAndDirector(href):
    genres_dict = {1: 'Action & Adventure', 2: 'Animation', 4: 'Art House & International',
                   5: 'Classics', 6: 'Comedy', 8: 'Documentary', 9: 'Drama', 10: 'Horror',
                   11: 'Kids & Family', 13: 'Mystery & Suspense', 14: 'Science Fiction & Fantasy',
                   15: 'Special Interest', 16: 'Television', 18: 'Romance'}  # haven't found 3, 7, 12, 17
    if 'genres' in href:
        href = href.replace('/browse/opening/?genres=', '')
        href = int(href)
        href = genres_dict[href]
    if 'celebrity' in href:
        href = href.replace('/celebrity/', 'Director: ')
        href = href.replace('_', ' ')  # ang_lee to ang lee
        href = href.title()  # ang lee to Ang Lee
    return href


best_comments = open('best_comments.txt', 'w')

for k in rating_dict:
    if rating_dict[k] > 70:
        m_title = title_dict[k]
        print (m_title)
        best_mov[m_title] = rating_dict[k]
        m_url = "https://www.rottentomatoes.com" + href_dict[k]
        m_sourceCode = requests.get(m_url)
        m_soup = BeautifulSoup(m_sourceCode.text, 'lxml')
        best_comments.writelines(m_title + '\n')
        for comment in m_soup.findAll('p', {'class': "comment clamp clamp-6"}):
            comment = str(comment)
            pattern = re.compile("<.*>")
            for found_trash in re.findall(pattern, comment):
                comment = comment.replace(found_trash, '')
            # The above three lines using the regular expression to delete useless string
            # have the same effect as:
            # comment = comment.replace('<p class="comment clamp clamp-6>", '')
            # comment = comment.replace('</p>', '')
            # comment = comment.replace('<br/>', '')
            best_comments.writelines(comment + '\n')
        intro = m_soup.find('div', {'class': "movie_synopsis clamp clamp-6"}).contents[0]
        intro = str(intro)
        best_intro[m_title] = intro
        mov_info = m_soup.findAll('div', {'class': 'meta-value'})
        mov_info = str(mov_info)
        mov_info = BeautifulSoup(mov_info, 'lxml')
        print ('Genre:')
        best_info[m_title] = 'Genre: '
        for info in mov_info.findAll('a'):
            info_href = info.get('href')
            info_href = str(info_href)
            GenreAndDirector = find_GenreAndDirector(info_href)
            if 'Director:' in GenreAndDirector:
                print (GenreAndDirector)
                best_info[m_title] += '\n' + GenreAndDirector
                break
            print (GenreAndDirector)
            best_info[m_title] += GenreAndDirector + ' '
best_comments.close()

file_time = 'Time File Created:' + time.asctime() + '\n'
best_movies = open('best_movies.txt', 'w')
best_movies.writelines(file_time)

for key in best_mov:
    line = 'Movie Title: ' + str(key) + '\nScore: ' + str(best_mov[key]) + '\n'
    best_movies.writelines(line)
    introduction = best_intro[key]
    best_movies.writelines('Introduction:' + introduction + '\n')
    movie_information = best_info[key]
    best_movies.writelines(movie_information + '\n')
best_movies.close()

worst_mov = {}  # movie title: rating
worst_intro = {}  # movie title: introduction
worst_info = {}  # movie title: movie info

worst_comments = open('worst_comments.txt', 'w')

for k in rating_dict:
    if 60 > rating_dict[k] > 0:
        m_title = title_dict[k]
        print (m_title)
        worst_mov[m_title] = rating_dict[k]
        m_url = "https://www.rottentomatoes.com" + href_dict[k]
        m_sourceCode = requests.get(m_url)
        m_soup = BeautifulSoup(m_sourceCode.text, 'lxml')
        worst_comments.writelines(m_title + '\n')
        for comment in m_soup.findAll('p', {'class': "comment clamp clamp-6"}):
            comment = str(comment)
            pattern = re.compile("<.*>")
            for found_trash in re.findall(pattern, comment):
                comment = comment.replace(found_trash, '')
            worst_comments.writelines(comment + '\n')
        intro = m_soup.find('div', {'class': "movie_synopsis clamp clamp-6"}).contents[0]
        intro = str(intro)
        worst_intro[m_title] = intro
        mov_info = m_soup.findAll('div', {'class': 'meta-value'})
        mov_info = str(mov_info)
        mov_info = BeautifulSoup(mov_info, 'lxml')
        print ('Genre:')
        worst_info[m_title] = 'Genre: '
        for info in mov_info.findAll('a'):
            info_href = info.get('href')
            info_href = str(info_href)
            GenreAndDirector = find_GenreAndDirector(info_href)
            if 'Director:' in GenreAndDirector:
                print (GenreAndDirector)
                worst_info[m_title] += '\n' + GenreAndDirector
                break
            print (GenreAndDirector)
            worst_info[m_title] += GenreAndDirector + ' '
worst_comments.close()

worst_movies = open('worst_movies.txt', 'w')
worst_movies.writelines(file_time)

for key in worst_mov:
    line = 'Movie Title: ' + str(key) + '\nScore: ' + str(worst_mov[key]) + '\n'
    worst_movies.writelines(line)
    introduction = worst_intro[key]
    worst_movies.writelines('Introduction:' + introduction.encode('utf8') + '\n')
    movie_information = worst_info[key]
    worst_movies.writelines(movie_information.encode('utf8') + '\n')
worst_movies.close()

# Reference for functions wordListToFreqDict, sortFreqDict and removeStopwords:
# William J. Turkel and Adam Crymble , "Counting Word Frequencies with Python,"
# Programming Historian, (2012-07-17), http://programminghistorian.org/lessons/counting-frequencies


def wordListToFreqDict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(zip(wordlist, wordfreq))


def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux


stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards']
stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
stopwords += ['yours', 'yourself', 'yourselves']


def removeStopwords(wordlist, stopwords):
    return [w for w in wordlist if w not in stopwords]


def create_WordFrequency(input, output):
    with open(input, 'r') as fin:
        wordstring = fin.read().lower()
    fin.close()

    wordlist = wordstring.split()
    wordlist = removeStopwords(wordlist, stopwords)
    dictionary = wordListToFreqDict(wordlist)
    sorteddict = sortFreqDict(dictionary)

    WordFrequency = open(output, 'w')

    for s in sorteddict:
        print(str(s))
        WordFrequency.writelines(str(s))
    WordFrequency.close()

input_best = 'best_comments.txt'
output_best = 'best_WordFrequency.txt'

input_worst = 'worst_comments.txt'
output_worst = 'worst_WordFrequency.txt'

create_WordFrequency(input_best,output_best)
create_WordFrequency(input_worst, output_worst)

