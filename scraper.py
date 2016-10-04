import shutil
import os
import re
from bs4 import BeautifulSoup
import urllib2


# Globals

__LINK_CONSTANT = "http://zeus.mtsac.edu/~rpatters/CISD11/Workshops/"

__CLASS_SECTIONS = ["Assignment.htm", "Lab.htm"]

__MAX_URL = 16

# # 


class Workshop:

    def __init__ (self, section_title, chapter_number):

        self.section_number = section_number

        self.chapter_number = chapter_number

        self.directory = section_title + '/Chapter' + chapter_number

        self.files = None
    


# # 

def get_Soup (url):

    DOM = urllib2.urlopen (url).read ()

    return BeautifulSoup (DOM, "html.parser");


def get_File_Names (links):

    file_names = []

    i = 0

    for link in links:

        file_names.append (re.sub (r"(.*/.*/.*/)", "", link['href']))

        i += 1

    return file_names;


def get_Directories (section, filenames):

    directories = []

    if os.path.exists (section):

        shutil.rmtree (section)

    os.makedirs (section)

    for i in range (1, __MAX_URL):

        directory_name = str (section) + '/Chapter_' + str(i) 

        if os.path.exists (directory_name):

            shutil.rmtree (directory_name)

        os.makedirs (directory_name)

        directories.append (directory_name)

    return directories;


def get_Workshop_Urls (class_section):

    urls = [] 

    for count in range (1, __MAX_URL):

        url = ""

        if count <= 9:

            o_number = '0' + str (count)

            url = "http://zeus.mtsac.edu/~rpatters/CISD11/Workshops/"   \
                + "Workshop_"   + o_number + "/Workshop" + o_number     \
                + "/21694/"     + class_section 

        else:

            url =   "http://zeus.mtsac.edu/~rpatters/CISD11/Workshops/"     \
                +   "Workshop_" + str (count) + "/Workshop" + str (count)   \
                +   "/21694/"   + class_section 

        urls.append (url)

# TESTING
    print ("\n"+"get_Workshop_Urls -- urls = \n")
    print (urls)
    print ("\n")
# TESTING
    return urls; 


def get_Download_Links (web_page):

    string_pattern = re.compile (r'\bdownload')

    links = web_page.find_all ('a',  attrs={'title' : string_pattern});

# TESTING
    print ("\nget_Download_Links() -- links = \n")
    print (links)
    print ("\n")
# TESTING

    return links;
    

def download_File (link, directory, filename):

    request = urllib2.Request (link)

    response = urllib2.urlopen (request)

    #fileName = re.search(r"(?<=Solve/)[^}]*(?=\.)", newLink).group(0)

    file_stream = open (directory+"/"+filename, 'wb')

    file_stream.write (response.read ())

    file_stream.close ()

    return;


def CISD_Scraper (class_section):

    workshop_urls = get_Workshop_Urls (class_section);

    for url in workshop_urls:

        soup = get_Soup (url)
        
        download_links = get_Download_Links (soup)
        
        filenames = get_File_Names (download_links)

        directories = get_Directories (filenames)

        for link, directory in zip (download_links, directories):

            download_link = \
                re.sub(r"(../../../)", __LINK_CONSTANT, link['href'])

            download_File (download_link, directory)

    return;


CISD_Scraper (__CLASS_SECTIONS[0])
