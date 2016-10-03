import os
import re
from bs4 import BeautifulSoup
import urllib2


# Globals

root_url = 

__LINK_CONSTANT = "http://zeus.mtsac.edu/~rpatters/CISD11/Workshops/"

__CLASS_SECTIONS = ["Assignment.htm", "Lab.htm"]

__DIRECTORIES = ""

# # 

def get_Soup (url):

    DOM = urllib2.urlopen (url).read ()

    return BeautifulSoup (DOM);


def get_File_Names (links):

    file_names = [links.len]

    for i, link in links:

        file_names[i] = re.sub (r"(.*/.*/.*/)", "", link['href'])

    return file_names;


def prepare_Directories (filenames):

    for i in range (1, links.len):

        dir_name = filenames[i] + "_" + str(i)

        # TODO replace with real code
        if !exists(dir_name):

            # Delete current directory, and remake it

            os.makedirs (dir_name)

    return;


def get_Download_Links (web_page):

    string_pattern = re.compile (r'\bdownload')

    _links = web_page.find_all ('a',  attrs={'title' : string_pattern}) 

    #   Prepare Urls
    for count in range (1, URL_MAX):

        url = ""

        if count < 9:

            o_number = '0' + str (count)

            url = "http://zeus.mtsac.edu/~rpatters/CISD11/Workshops/"   \
                + "Workshop_"   + o_number + "/Workshop" + o_number     \
                + "/21694/"     + __CLASS_SECTIONS[count]

        else:

            url =   "http://zeus.mtsac.edu/~rpatters/CISD11/Workshops/"     \
                +   "Workshop_" + str (count) + "/Workshop" + str (count)   \
                +   "/21694/"   + __CLASS_SECTIONS[count]

        urls[count] = url

    return urls; 
    # end of Scrape() 


def download_File (link, directory, filename):

    request = urllib2.Request (link)

    response = urllib2.urlopen (request)

    #fileName = re.search(r"(?<=Solve/)[^}]*(?=\.)", newLink).group(0)

    file_stream = open (directory+"/"+filename, 'wb')

    file_stream.write (response.read ())

    file_stream.close c()

    return;


def CISD_Scraper (url):

    soup = get_Soup (url)
    
    download_links = get_Download_Links (soup)

    filenames = get_File_Names (download_links)

    prepare_Directories (filenames)

    for i, url in workshop_urls:

        download_link = re.sub(r"(../../../)", __LINK_CONSTANT, url)

        download_File (download_link, directories[i], )

    return;


