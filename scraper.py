# TESTING
from urllib.request import urlopen
from urllib.error import HTTPError
# TESTING
import shutil
import os
import re
from bs4 import BeautifulSoup


# Globals

__LINK_CONSTANT = "http://zeus.mtsac.edu/~rpatters/CISD11/Workshops/"

__CLASS_SECTIONS = ["Assignment.htm", "Lab.htm"]

__MAX_URL = 15

# # 


class Workshop:

    def __init__ (self, section, chapter_number):

        self.section = section

        self.section_title = section[:-4]

        self.chapter_number = chapter_number

        self.workshop_url = get_Workshop_Url (section, chapter_number)

        self.soup = get_Soup (self.workshop_url)

        self.directory = self.section_title + '/Chapter' + str (chapter_number)

        prepare_Directory (self.directory)

        self.download_links = get_Download_a_Tags (self.soup)

# # 

def save_to_file (obj):

    with open ('Documents/error_a_tags.txt', 'a') as error_a_tag_file:
        
        error_a_tag_file.write ('\nError occured -- Now Saving --')

        for element in obj:

            error_a_tag_file.write ('\n')
            error_a_tag_file.write (str (element))

    return;

    
def get_Download_a_Tags (web_page):

    string_pattern = re.compile (r'\bdownload')

    a_tags = web_page.find_all ('a',  attrs={'title' : string_pattern});

    with open ('Documents/complete_a_tags.txt', 'a') as a_tag_file:

        a_tag_file.write ('\nNew Element:')

        for a_tag in a_tags: 

            a_tag_file.write ('\n\t')

            a_tag_file.write (str (a_tag))

        a_tag_file.write ('--------\n')

    return a_tags;


def get_Soup (url):

    DOM = urlopen (url).read ()

    return BeautifulSoup (DOM, "html.parser");


''' 
#   Deprecated?
def get_File_Name (link):

    return re.sub (r"(.*/.*/.*/)", "", link['href'])
'''



def get_File_Names (a_tags):

    file_names = []

    for a_tag in a_tags:

        file_names.append (re.sub (r"(.*/.*/.*/)", "", a_tag['href']))

    return file_names;


def prepare_Directory (pathname):

    if os.path.exists (pathname):

        shutil.rmtree (pathname)

    os.makedirs (pathname)

    return; 


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

    try:
        response = urlopen (link)

        file_stream = open (workshop.directory+'/'+ \
            workshop.current_filename, 'wb')

        file_stream.write (response.read ())

        file_stream.close ()

    except HTTPError as e:

        file_stream = open (workshop.directory+'/'+ \
            workshop.current_filename, 'wb')

        file_stream.write (e.fp.read ())

        file_stream.close ()

    return;


def Scrape (section):

    for i in range (1, __MAX_URL):

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
                a_tag['href'].rsplit ('/', 1)[-1]
                #re.sub (r"(.*/.*/.*/)", "", a_tag['href'])

            if workshop.current_filename.__len__ () < 1:

                print('\n-----------------')
                print('\n-----------------')
                print('\n-----------------')
                print('\n\t[ERROR] filename is empty')
                print('\n-----------------')
                print('\n-----------------')
                print('\n-----------------')

                with open ('Documents/errorFile.txt', 'a') as errorFile:

                    errorFile.write ('\n' + str(download_link))

                # TESTING
                save_to_file (a_tag)
                # TESTING

            else:

                print ('\tDownloading: ' + workshop.current_filename)

                download_File (workshop, download_link)

    return;


Scrape (__CLASS_SECTIONS[0])
Scrape (__CLASS_SECTIONS[1])


