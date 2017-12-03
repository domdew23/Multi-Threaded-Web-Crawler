import os

# Each website you crawl is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating project - ', directory)
        os.makedirs(directory)                  # create a new directory with specified name
    else:
        print('Already created project - ', directory)


# Create queue and crawled files (if not created)
def create_data_files(project_name, base_url):
    queue = os.path.join(project_name + '/queue.txt')         # a list of links on the waiting list
    crawled = os.path.join(project_name + '/crawled.txt')     # a list of links that have been crawled
    if not os.path.isfile(queue):               # checks if the file exists already
        write_file(queue, base_url)             # home page will be first url in waiting list
    if not os.path.isfile(crawled):
        write_file(crawled, '')


# Create a new file
def write_file(file_name, data):
    with open(file_name, 'w') as file:  # creates new file with file_name in write mode
        file.write(data)                # writes specified data to the file
        file.close()                    # close file to save memory


# Add data onto a existing file
def append_to_file(file_name, data):
    with open(file_name, 'a') as file:  # a mode means add onto a file
        file.write(data + '\n')         # put pointer on a new line


# Delete the contents of a file
def delete_file_contents(file_name):
    with open(file_name, 'w'):        # open a file with the same name, will delete all the contents
        pass

# A Set can only have unique elements

# Read a file and convert each line to items in a set
def file_to_set(file_name):
    results = set()                                 # create a new empty set
    with open(file_name, 'rt') as file:             # open the file_name in read text mode
        for line in file:                           # iterate through file one line at a time
            results.add(line.replace('\n', ''))     # add each new line to the set
    return results


# Iterate through a set, each item will be a new line in the file
def set_to_file(links, file):
    delete_file_contents(file)      # clear the file
    for link in sorted(links):      # go through each link in the set
        append_to_file(file, link)  # add data to end of the file (queued or crawled)














