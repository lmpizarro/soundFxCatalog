# USAGE: ./list-sounds [SOUND_DIRECTORY]

# http://pythoncentral.io/recursive-file-and-directory-manipulation-in-python-part-1/

import os
import sys
import pysox, re
import time

from pymongo import MongoClient

client = MongoClient()
db = client.soundFxDb


# input() workaround to support Python 2. Python 3 renamed raw_input() => input().
# Alias input() to raw_input() if raw_input() exists (Python 2).
try:
    input = raw_input
except NameError:
    pass


class Discover_Files(object):

    def __init__(self, root_dir, first_level_dir='./', files_extensions=['mp3', 'wav', 'aif', 'ogg']):
        self.root_dir = root_dir
	self.first_level_dir = first_level_dir
	self.files_extensions = files_extensions
	self.files_directory = self.root_dir 
	self.file_list =[]
	self.counter = 0


    def get_paths(self):
        # Get the absolute path of the movie_directory parameter
        movie_directory = os.path.abspath(self.files_directory)

        # Get a list of files in movie_directory
        movie_directory_files = os.listdir(movie_directory)

        # Traverse through all files
        for filename in movie_directory_files:
            filepath = os.path.join(movie_directory, filename)

            # Check if it's a normal file or directory
            if os.path.isfile(filepath):

                # Check if the file has an extension of typical video files
                for movie_extension in self.files_extensions:
                    # Not a movie file, ignore
                    if not filepath.endswith(movie_extension):
                        continue

                    # We have got a video file! Increment the counter
                    self.counter += 1
		    library = re.sub(self.root_dir,'',filepath).strip()
		    head, tail = os.path.split(library)


		    self.file_list.append({'path':'{0}'.format(filepath),
				           'library': head, 
				           'file_size':os.path.getsize(filepath), 
				           'filename':tail,
                                           'root_dir' :self.root_dir, 
			                  })

            elif os.path.isdir(filepath):
                # We got a directory, enter into it for further processing
		self.files_directory = filepath
                self.get_paths()


ROOT_DIR = None

sound_list = []
def discover_audio_files(movie_directory, movie_extensions=['mp3', 'wav', 'aif', 'ogg']):
    ''' Print files in movie_directory with extensions in movie_extensions, recursively. '''

    # Get the absolute path of the movie_directory parameter
    movie_directory = os.path.abspath(movie_directory)

    # Get a list of files in movie_directory
    movie_directory_files = os.listdir(movie_directory)

    # Traverse through all files
    for filename in movie_directory_files:
        filepath = os.path.join(movie_directory, filename)

        # Check if it's a normal file or directory
        if os.path.isfile(filepath):

            # Check if the file has an extension of typical video files
            for movie_extension in movie_extensions:
                # Not a movie file, ignore
                if not filepath.endswith(movie_extension):
                    continue

                # We have got a video file! Increment the counter
                discover_audio_files.counter += 1


                try:
               	    sox_p = pysox.CSoxStream(filepath, 'r')
		    #CSignalInfo(48000.0,2,32,288000)
		    #             sr  , ch , bits prec. , samples
		    signal_info = sox_p.get_signal()
		    encoding_info = sox_p.get_encoding()
		    encoding_info = encoding_info.get_encodinginfo()
		    signal_info = signal_info.get_signalinfo()
		    library = re.sub(ROOT_DIR,'',filepath).strip()
		    head, tail = os.path.split(library)
                    # Print it's name
		    l = {'path':filepath, 'root_dir' :ROOT_DIR, 
				    "library": head , 
				    "filename":tail,
				    "file_size":os.path.getsize(filepath), 
				    'signal_info':signal_info, 
				    'encoding_info':encoding_info,
				    'insert_time': time.time()}
		    sound_list.append('{0}'.format(l))
		    result = db.disco_a.insert_one(l)
		except:
		    print "Error: ", filepath



        elif os.path.isdir(filepath):
            # We got a directory, enter into it for further processing
            discover_audio_files(filepath)



def test_discover_audio_files():
    # Directory argument supplied, check and use if it's a directory
    if len(sys.argv) == 2:
        if os.path.isdir(sys.argv[1]):
            movie_directory = sys.argv[1]
        else:
            print('ERROR: "{0}" is not a directory.'.format(sys.argv[1]))
            exit(1)
    else:
        # Set our movie directory to the current working directory
        movie_directory = os.getcwd()


    ROOT_DIR = movie_directory 
    print('\n -- Looking for movies in "{0}" --\n'.format(movie_directory))

    # Set the number of processed files equal to zero
    discover_audio_files.counter = 0

    # Start Processing
    discover_audio_files(movie_directory)
    print (sound_list[0:40])
    # We are done. Exit now.
    print('\n -- {0} Movie File(s) found in directory {1} --'.format \
            (discover_audio_files.counter, movie_directory))
    print('\nPress ENTER to exit!')

    # Wait until the user presses enter/return, or <CTRL-C>
    try:
        input()
    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':

    DF = Discover_Files("/media/usb0/Sonidos" )
    DF.get_paths()

    print DF.file_list
