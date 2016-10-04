# TESTING
from urllib2 import urlopen
# TESTING
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

        self.section_title = section_title

        self.chapter_number = chapter_number

        self.workshop_url = get_Workshop_Url (section_title, chapter_number)

        self.soup = get_Soup (self.workshop_url)

        self.directory = section_title + '/Chapter' + str (chapter_number)

        prepare_Directory (self.directory)

        self.download_links = get_Download_Links (self.soup)

# # 

    
def get_Download_Links (web_page):

    string_pattern = re.compile (r'\bdownload')

    links = web_page.find_all ('a',  attrs={'title' : string_pattern});

    return links;


def get_Soup (url):

    DOM = urllib2.urlopen (url).read ()

    return BeautifulSoup (DOM, "html.parser");


def get_File_Name (link):

    return re.sub (r"(.*/.*/.*/)", "", link['href'])



def get_File_Names (links):

    file_names = []

    for link in links:

        file_names.append (re.sub (r"(.*/.*/.*/)", "", link['href']))

    return file_names;


def prepare_Directory (pathname):

    if os.path.exists (pathname):

# TODO Don't clobber
        shutil.rmtree (pathname)

    os.makedirs (pathname)

    return; 


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


def get_Workshop_Url (class_section, chapter_number):

    url = ""

    if chapter_number <= 9:

        o_number = '0' + str (chapter_number)

        url = "http://zeus.mtsac.edu/~rpatters/CISD11/Workshops/"   \
            + "Workshop_"   + o_number + "/Workshop" + o_number     \
            + "/21694/"     + class_section 

    else:

        url =   "http://zeus.mtsac.edu/~rpatters/CISD11/Workshops/"     \
            +   "Workshop_" + str (chapter_number)  + "/Workshop"       \
            +   str (chapter_number)   + "/21694/"  + class_section 

    return url; 


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

    return urls; 


    

def download_File (workshop, link):

    # TESTING
    print ('\ndownload_File() :: link: '+link+'\n\n')
    # TESTING

    request = urllib2.Request (link)

    try:
        response = urllib2.urlopen (request)

        file_stream = open (workshop.directory+'/'+ \
            workshop.current_filename, 'wb')

        file_stream.write (response.read ())

        file_stream.close ()

    except urllib2.HTTPError, e:

        file_stream = open (workshop.directory+'/'+ \
            workshop.current_filename, 'wb')

        file_stream.write (e.fp.read ())

        file_stream.close ()

    return;


def Scrape (section):

    for i in range (1, 16):

        print ('\n\nChapter ' + str(i))

        workshop = Workshop (section, i)
        
        workshop.file_count = 0

        for a_tag in workshop.download_links:

            workshop.file_count += 1

            print ('\n\t' + str (workshop.file_count) + ' of ' + \
                str (workshop.download_links.__len__ ()))

            download_link = \
                re.sub(r"(../../../)", __LINK_CONSTANT, a_tag['href'])

            workshop.current_filename = \
                re.sub (r"(.*/.*/.*/)", "", a_tag['href'])

            if workshop.current_filename.__len__ () < 1:

                print('\n-----------------')
                print('\n-----------------')
                print('\n-----------------')
                print('\n\t[ERROR] filename is empty')

            else:

                print ('\tDownloading: ' + workshop.current_filename)

                download_File (workshop, download_link)

    return;


Scrape (__CLASS_SECTIONS[0])
Scrape (__CLASS_SECTIONS[1])
