import os


def main(dir, old):
    os.chdir(dir)
    for old_file in os.listdir("."):
        if old_file.endswith(old):
            index = old_file.find("_") #can be replaced by any character
            os.rename(old_file, old_file[:index + 1] + "0" + old_file[index + 1:])  # replace "" by anything I want.



if __name__ == '__main__':
    path = raw_input('Please enter the direction you want to go to: ')
    old_string = raw_input('Please enter the type of file: ')  # type of file
    main(path, old_string)

