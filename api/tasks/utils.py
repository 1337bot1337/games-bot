import os


def directory_containing(filename):
    directory = os.getcwd()
    while True:
        if directory == '/':
            return None
        elif filename in os.listdir(directory):
            return directory
        else:
            directory = os.path.abspath(os.path.join(directory, '..'))


project_root = directory_containing('manage.py')
