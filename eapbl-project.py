# -*- coding: utf-8 -*-

import mechanize
from bs4 import BeautifulSoup
import os
import csv
import zipfile
import shutil
import time

'''
Program to download images from the endangered archives collection from http://eap.bl.uk/database/collections.a4d
'''

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
        'http://eap.bl.uk/database/results.a4d?projID=EAP689',  # EAP689 Constituting a digital archive of Tamil agrarian history (1650-1950) - phase II
        'http://eap.bl.uk/database/results.a4d?projID=EAP692',  # EAP692 Documentation of endangered temple art of Tamil Nadu
        'http://eap.bl.uk/database/results.a4d?projID=EAP737'  	# EAP737 Representing Self and Family. Preserving early Tamil studio photography
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
        br.addheaders = [('User-Agent', user_agent_string)]

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
                print "Loading publication link: " + link
                page = br.open(link).read()

                try:
                    os.mkdir(os.path.join(abspath, title))
                except OSError:
                    print "Directory: " + title + " already exists! Not creating it again. Not downloading again."

                with open(os.path.join(abspath + '/' + title, 'thumbs.html'), 'w') as f:
                    f.write(page)
            else:
                print "Already exists! folder: " + title + " and thumbs.html"

    # get a list of folder names, cd into it, parse the thumbs.html file and store the urls of the image in a file
    folders = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')]
    base_image_url = 'http://eap.bl.uk/'
    for f in folders:
        os.chdir(f)
        print "Switched to folder: " + f + ". Downloading images."
        image_soup = BeautifulSoup(open('thumbs.html', 'r'), 'html.parser')
        ul = image_soup.find('ul', class_='ad-thumb-list')

        try:
            for li in ul.find_all('li'):
                image_link = li.a['href']
                full_image_link = base_image_url + li.a['href']
                image_file_name = image_link.replace('/', '_')
                image_path = os.path.join(os.path.abspath('.'), image_file_name)

                # don't download image if already exists
                if not os.path.exists(image_file_name):
                    # download and write the image
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
