# -*- coding: utf-8 -*-

import mechanize
from bs4 import BeautifulSoup
import os
import csv
import sys
import shutil
import time
import urllib2
import random

'''
Program to download images from the endangered archives collection from http://eap.bl.uk/database/collections.a4d
'''

if sys.version_info[0] != 2:
    raise Exception("Python 2 is required to run this script.")

# list of project urls to downloads
urls = ['http://eap.bl.uk/database/results.a4d?projID=EAP023',  # EAP023 Preserving Marathi manuscripts and making them accessible
        'http://eap.bl.uk/database/results.a4d?projID=EAP038',  # EAP038 Survey, conservation and archiving of pre-1947 Telugu printed materials in India
        'http://eap.bl.uk/database/results.a4d?projID=EAP127',  # EAP127 Archiving 'popular market' Bengali books
        'http://eap.bl.uk/database/results.a4d?projID=EAP183',  # EAP183 Preserving early print literature on the history of Tamilnadu
        'http://eap.bl.uk/database/results.a4d?projID=EAP191',  # EAP191 Strategies for archiving the endangered publications of French India (1800-1953)
        'http://eap.bl.uk/database/results.a4d?projID=EAP201',  # EAP201 Study and collection of Hakku Patras and other documents among folk communities in Andhra Pradesh
        'http://eap.bl.uk/database/results.a4d?projID=EAP208',  # EAP208 Preserving memory: documentation and digitisation of palm leaf manuscripts from northern Kerala, India
        'http://eap.bl.uk/database/results.a4d?projID=EAP248',  # EAP248 Preserving more Marathi manuscripts and making them accessible - major project
        'http://eap.bl.uk/database/results.a4d?projID=EAP261',  # EAP261 Digital archive of early Bengali drama
        'http://eap.bl.uk/database/results.a4d?projID=EAP262',  # EAP262 Retrieval of two major and endangered newspapers: Jugantar and Amrita Bazar Patrika
        'http://eap.bl.uk/database/results.a4d?projID=EAP314',  # EAP314 Rescuing Tamil customary law: locating and copying endangered records of village judicial assemblies (1870-1940)
        'http://eap.bl.uk/database/results.a4d?projID=EAP341',  # EAP341 Rescuing text: retrieval and documentation of printed books and periodicals from public institutions in eastern India published prior to 1950 - major project
        'http://eap.bl.uk/database/results.a4d?projID=EAP372',  # EAP372 Preserving early periodicals and newspapers of Tamilnadu and Pondichery
        'http://eap.bl.uk/database/results.a4d?projID=EAP458',  # EAP458 Constituting a digital archive of Tamil agrarian history during the colonial period
        'http://eap.bl.uk/database/results.a4d?projID=EAP584',  # EAP584 Preserving memory II - documentation and digitisation of palm leaf manuscripts from Kerala, India
        'http://eap.bl.uk/database/results.a4d?projID=EAP676',  # EAP676 Survey of Buddhist Sanskrit manuscripts in the possession of Vajrayana Viharas and Newar Buddhist families in Lalitpur in the Kathmandu valley, Nepal
        'http://eap.bl.uk/database/results.a4d?projID=EAP683',  # EAP683 Rāmamālā Library manuscript project
        'http://eap.bl.uk/database/results.a4d?projID=EAP689',  # EAP689 Constituting a digital archive of Tamil agrarian history (1650-1950) - phase II
        'http://eap.bl.uk/database/results.a4d?projID=EAP692'   # EAP692 Documentation of endangered temple art of Tamil Nadu
        ]

user_agent_list = ['Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)',
                   'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
                   'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
                   'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1',
                   'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
                   'Mozilla/5.0 (Windows; U; Windows NT 6.2; WOW64; rv:1.8.0.7) Gecko/20110321 MultiZilla/4.33.2.6a SeaMonkey/8.6.55',
                   'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
                   'Opera/12.02 (Android 4.1; Linux; Opera Mobi/ADR-1111101157; U; en-US) Presto/2.9.201 Version/12.02',
                   'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; XH; rv:8.578.498) fr, Gecko/20121021 Camino/8.723+ (Firefox compatible)',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
                   'Mozilla/5.0 (X11; U; Linux x86_64; it-it) AppleWebKit/534.26+ (KHTML, like Gecko) Ubuntu/11.04 Epiphany/2.30.6',
                   'Mozilla/5.0 (X11; U; Linux x86_64; fr-FR) AppleWebKit/534.7 (KHTML, like Gecko) Epiphany/2.30.6 Safari/534.7',
                   'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Epiphany/2.30.6 Safari/534.7',
                   'Mozilla/5.0 (X11; U; Linux i686; sv-se) AppleWebKit/531.2+ (KHTML, like Gecko) Safari/531.2+ Epiphany/2.30.6',
                   'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0',
                   'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0',
                   'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
                   'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.13) Gecko/20100916 Iceape/2.0.8',
                   'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121201 icecat/17.0.1',
                   'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20111106 IceCat/7.0.1',
                   'Mozilla/5.0 (X11; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1 Iceweasel/15.0.1',
                   'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
                   'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1250.0 Iron/22.0.2150.0 Safari/537.4'
                   ]


# create a directory to work in and cd into it
try:
    os.mkdir(os.path.join(os.getcwd(), 'eapbl-project'))
except OSError:
    print "Directory 'eapbl-project' already exists! Not creating it again!"

os.chdir('eapbl-project')

br = mechanize.Browser()
abspath = os.path.abspath('.')

for url in urls:

    # TODO: don't download page if already exists
    print "Downloading page: " + url
    html_page = br.open(url).read()

    soup = BeautifulSoup(html_page, 'html.parser')
    results = soup.select('#results')
    heading = results[0].find('th').h3.text     # heading is the name of the project
    heading = heading.replace(':', '-')

    try:
        os.mkdir(os.path.join(abspath, heading))
    except OSError:
        print "Directory " + heading + " already exists! Not creating it again!"

    # don't write page if already exists
    if not os.path.exists(os.path.join(abspath+'/'+heading, 'page.html')):
        with open(os.path.join(abspath+'/'+heading, 'page.html'), 'w') as f:
            f.write(html_page)
    else:
        print "Not writing 'page.html' - already exists"

    with open(os.path.join(abspath + '/' + heading, 'ref.txt'), 'w') as r:  # store referer link in ref.txt
        r.write(url)

# list all the directories
dirs = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')]

for directory in dirs:
    print "Switching to directory: " + directory
    os.chdir(directory)

    # check if pubs.csv file exists - and write accordingly
    if not os.path.exists('pubs.csv'):
        soup = BeautifulSoup(open('page.html', 'r'), 'html.parser')
        results = soup.select("#results")

        base_url = 'http://eap.bl.uk/database/'

        with open('pubs.csv', 'wb') as f:
            writer = csv.writer(f, delimiter='@', quoting=csv.QUOTE_MINIMAL)
            for tr in results[0].find_all('tr'):
                for x in range(1, len(tr.find_all('td')), 2):
                    title = tr.find_all('td')[x].a.text.encode('utf-8').strip()                 # encode to utf-8
                    link = base_url + tr.find_all('td')[x].a['href'].encode('utf-8').strip()    # encode to utf-8

                    writer.writerow([title, link])
    else:
        print "Not writing 'pubs.csv' already exists"

    # read the pubs.csv, create a folder for every publication
    with open('pubs.csv', 'r') as f:
        abspath = os.path.abspath('.')

        br = mechanize.Browser()
        user_agent_string = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'
        with open('ref.txt', 'r') as r:
            referer_string = r.read().strip()

        br.addheaders = [('user-Agent', user_agent_string), ('referer', referer_string)]

        reader = csv.reader(f, delimiter='@')
        for row in reader:
            title = row[0].replace('/', '-').replace(':', '-')
            link = row[1]
            # skip 1 iteration if zip file of title name exists
            if os.path.exists(title + '.zip'):
                print "Already downloaded and zipped " + title
                continue

            # don't load link and write if thumbs.html already exists
            if not os.path.exists(os.path.join(title, 'thumbs.html')):
                # time.sleep(2)
                print "Loading publication link: " + link
                try:
                    random_user_agent = random.choice(user_agent_list)
                    br.addheaders = [('user-agent', random_user_agent)]
                    page = br.open(link).read()
                except urllib2.URLError, e:
                    print e.reason

                # request = br.request
                # print request.header_items()

                try:
                    os.mkdir(os.path.join(abspath, title))
                except OSError:
                    print "Directory: " + title + " already exists! Not creating it again. Not downloading again."

                with open(os.path.join(abspath + '/' + title, 'thumbs.html'), 'w') as f:
                    f.write(page)
            else:
                print "Already exists! folder: " + title + " and thumbs.html"

            if not os.path.exists(os.path.join(title, 'ref.txt')):  # store a referer link for the images
                with open(os.path.join(abspath + '/' + title, 'ref.txt'), 'w') as tref:
                    tref.write(link)

    # get a list of folder names, cd into it, parse the thumbs.html file and store the urls of the image in a file
    folders = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')]
    base_image_url = 'http://eap.bl.uk/'
    for f in folders:
        os.chdir(f)
        print "Switched to folder: " + f + ". Downloading images."
        image_soup = BeautifulSoup(open('thumbs.html', 'r'), 'html.parser')
        ul = image_soup.find('ul', class_='ad-thumb-list')

        # add image referer link
        with open('ref.txt', 'r') as image_referer:
            img_ref = image_referer.read().strip()

        random_user_agent = random.choice(user_agent_list)
        br.addheaders = [('user-agent', random_user_agent), ('Referer', img_ref)]

        try:
            for li in ul.find_all('li'):
                image_link = li.a['href']
                full_image_link = base_image_url + li.a['href']
                image_file_name = image_link.replace('/', '_').strip('_')  # strip leading '_' from image_file_name
                image_path = os.path.join(os.path.abspath('.'), image_file_name)

                # don't download image if already exists
                if not os.path.exists(image_file_name):
                    # download and write the image
                    time.sleep(2)

                    random_user_agent = random.choice(user_agent_list)
                    br.addheaders = [('user-agent', random_user_agent)]

                    print "Retrieving image: " + full_image_link
                    br.retrieve(full_image_link, image_path)
                else:
                    print "Already exists! image: " + image_file_name

            # sleep for 3 seconds after downloading a set of images
            time.sleep(3)
        except AttributeError:
            print "AttributeError - There may be no images available yet."
            pass

        os.chdir('..')

    # zip up all folders
    for pub_folder in os.listdir('.'):
        if os.path.isdir(pub_folder):
            shutil._make_zipfile(pub_folder, pub_folder)    # create a zip archive of the folder
            shutil.rmtree(pub_folder)                       # delete the folder & contents

    # return to previous directory
    os.chdir('..')

print "DONE!"
