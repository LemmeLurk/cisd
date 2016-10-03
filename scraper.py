import shutil
import os
import re
from bs4 import BeautifulSoup
import urllib2


# Globals

__LINK_CONSTANT = "http://zeus.mtsac.edu/~rpatters/CISD11/Workshops/"

__CLASS_SECTIONS = ["Assignment.htm", "Lab.htm"]

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


def get_Directories (filenames):

    directories = []

    for i in range (1, filenames.__len__ ()):

        dir_name = filenames[i] + "_" + str(i)

        if os.path.exists (dir_name):

            shutil.rmtree (dir_name)

        os.makedirs (dir_name)

        directories.append (dir_name)

    return directories;


def get_Workshop_Urls (class_section):

    urls = [] 

    for count in range (1, 16):

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

    print ("\n"+"get_Workshop_Urls -- urls = \n")
    print (urls)
    print ("\n")
    return urls; 


def get_Download_Links (web_page):

    string_pattern = re.compile (r'\bdownload')

    links = web_page.find_all ('a',  attrs={'title' : string_pattern});

    print ("\nget_Download_Links() -- links = \n")
    print (links)
    print ("\n")

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


# TESTING
    f = open ('links.txt', 'w')
# TESTING

    for url in workshop_urls:

        soup = get_Soup (url)
        
        download_links = get_Download_Links (soup)
        
        filenames = get_File_Names (download_links)

        directories = get_Directories (filenames)

        i = 0

        for link in download_links:

            download_link = \
                re.sub(r"(../../../)", str(__LINK_CONSTANT), link['href'])
# TESTING
            f.write (download_link)

            print ('\n\nCISD_Scraper() -- link:' + download_link  + '\n\n')
# TESTING
            #download_File (download_link, directories[i], filenames[i])

            i += 1

    f.close ()

    return;


CISD_Scraper (__CLASS_SECTIONS[0])
