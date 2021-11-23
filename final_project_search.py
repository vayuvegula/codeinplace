"""
File: searchengine.py
---------------------
You fill in this comment
"""

import os
import sys
import string


def create_index(filenames, index, file_titles):
    """
    This function is passed:
        filenames:      a list of file names (strings)

        index:          a dictionary mapping from terms to file names (i.e., inverted index)
                        (term -> list of file names that contain that term)

        file_titles:    a dictionary mapping from a file names to the title of the article
                        in a given file
                        (file name -> title of article in that file)

    The function will update the index passed in to include the terms in the files
    in the list filenames.  Also, the file_titles dictionary will be updated to
    include files in the list of filenames.
    """
    for single_file in filenames:
        unique_terms_in_file, title = file_clean(single_file)
        # creating the index dictionary
        for term in unique_terms_in_file:
            if term not in index:
                index[term] = []
            if single_file not in index[term]:
                index[term].append(single_file)
        # creating the file titles dictionary
        file_titles[single_file] = title


def file_clean(filename):
    """
This function is passed:
Input parameter : filename : --> It is a string which is the name of the text file.
Return:(unique_terms,title)
 unique_terms--> A list consisting of unique terms from the text file after removing spaces,punctuation
        marks and making all the terms lower case
 title -> str: first line of the file assumed to be title
    """

    with open(filename) as f:
        all_lines = []  # for getting the title
        clean_lines = []  # for creating a list of cleaned up lines
        for line in f:
            # setting up list for title extraction
            all_lines.append(line)
            # cleaning up the lines
            line = line.strip().lower()
            line = line.strip('')
            no_punc = ""
            for char in line:
                if char not in string.punctuation:
                    no_punc = no_punc + char
            line = no_punc
            clean_lines.append(line)
        # extracting title name
        title = all_lines[0].strip()
        # removing duplicate terms in the file
        unique_terms = []
        for clean_line in clean_lines:
            terms = clean_line.split()
            for term in terms:
                if term not in unique_terms:
                    unique_terms.append(term)
        return unique_terms, title


def search(index, query):
    """
    This function is passed:
        index:      a dictionary mapping from terms to file names (inverted index)
                    (term -> list of file names that contain that term)

        query  :    a query (string), where any letters will be lowercase

    The function returns a list of the names of all the files that contain *all* of the
    terms in the query (using the index passed in).

    >>> index = {}
    >>> create_index(['test1.txt', 'test2.txt'], index, {})
    >>> search(index, 'apple')
    ['test1.txt']
    >>> search(index, 'ball')
    ['test1.txt', 'test2.txt']
    >>> search(index, 'file')
    ['test1.txt', 'test2.txt']
    >>> search(index, '2')
    ['test2.txt']
    >>> search(index, 'carrot')
    ['test1.txt', 'test2.txt']
    >>> search(index, 'dog')
    ['test2.txt']
    >>> search(index, 'nope')
    []
    >>> search(index, 'apple carrot')
    ['test1.txt']
    >>> search(index, 'apple ball file')
    ['test1.txt']
    >>> search(index, 'apple ball nope')
    []
    """
    query_list = query.split()
    for query_term in query_list:
        if query_term in index:
            posting_list_starting = index[query_list[0]]
            posting_list_next = index[query_term]
            if posting_list_next in posting_list_starting:
                posting_list_starting = posting_list_next
        else:
            posting_list_starting = []

    return posting_list_starting


##### YOU SHOULD NOT NEED TO MODIFY ANY CODE BELOW THIS LINE (UNLESS YOU'RE ADDING EXTENSIONS) #####


def do_searches(index, file_titles):
    """
    This function is given an inverted index and a dictionary mapping from
    file names to the titles of articles in those files.  It allows the user
    to run searches against the data in that index.
    """
    while True:
        query = input("Query (empty query to stop): ")
        query = query.lower()  # convert query to lowercase
        if query == '':
            break
        results = search(index, query)

        # display query results
        print("Results for query '" + query + "':")
        if results:  # check for non-empty results list
            for i in range(len(results)):
                title = file_titles[results[i]]
                print(str(i + 1) + ".  Title: " + title + ",  File: " + results[i])
        else:
            print("No results match that query.")


def textfiles_in_dir(directory):
    """
    DO NOT MODIFY
    Given the name of a valid directory, returns a list of the .txt
    file names within it.

    Input:
        directory (string): name of directory
    Returns:
        list of (string) names of .txt files in directory
    """
    filenames = []

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filenames.append(os.path.join(directory, filename))

    return filenames


def main():
    """
    Usage: searchengine.py <file directory> -s
    The first argument specified should be the directory of text files that
    will be indexed/searched.  If the parameter -s is provided, then the
    user can interactively search (using the index).  Otherwise (if -s is
    not included), the index and the dictionary mapping file names to article
    titles are just printed on the console.
    """
    # Get command line arguments
    args = sys.argv[1:]

    num_args = len(args)
    if num_args < 1 or num_args > 2:
        print('Please specify directory of files to index as first argument.')
        print('Add -s to also search (otherwise, index and file titles will just be printed).')
    else:
        # args[0] should be the folder containing all the files to index/search.
        directory = args[0]
        if os.path.exists(directory):
            # Build index from files in the given directory
            files = textfiles_in_dir(directory)
            index = {}  # index is empty to start
            file_titles = {}  # mapping of file names to article titles is empty to start
            create_index(files, index, file_titles)

            # Either allow the user to search using the index, or just print the index
            if num_args == 2 and args[1] == '-s':
                do_searches(index, file_titles)
            else:
                print('Index:')
                print(index)
                print('File names -> document titles:')
                print(file_titles)
        else:
            print('Directory "' + directory + '" does not exist.')


if __name__ == '__main__':
    main()
