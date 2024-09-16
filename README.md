# WebCrawler
## How to use the Tool:
After starting the client application by running python search.py, the user is asked to enter a command. The first option is the build command. When this is entered the crawler will begin to work till all 214 pages have been scraped. To help track progress of the crawler the size of the frontier and the total number of pages found is printed out. The next command is the load command, which has to be used before using the next two commands. This command loads the searched URLs list, and the inverted index dictionary from the urls.txt file and the index.txt file. The next command is the print command. To use this command, enter print followed by a word, which can be either in lower or upper case, and the inverted index of the word will be returned, if the word is not in the index then nothing will be returned. The final command is the find command to use this command enter find followed by the words separated by spaces you would like to search for. The corresponding urls will be returned to you with the ones with the highest score returned at the top. Furthermore, to use the application pip install nltk.
