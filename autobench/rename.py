import os


def main(directory, old, new):
    os.chdir(directory)
    old_files = os.listdir(directory)
    for old_file_name in old_files:
        new_file_name = old_file_name.replace(old, new)
        os.rename(old_file_name, new_file_name)

if __name__ == '__main__':
    path = raw_input('Please enter the dirction you want to go to: ')
    old_string = raw_input('Please enter the old string you want to replace: ')
    new_string = raw_input('Please enter the new string you want: ')
    main(path, old_string, new_string)
