import sys
import os

path = "."
delimeter = ""


def verify_and_process(filepath):
    if not str(filepath).endswith(".cube"):
        print(f"Ignoring file: '{filepath}'")
        return

    print(f"Processing file: '{filepath}'")

    newpath = f"{str(filepath).removesuffix(".cube").split(delimeter)[0]}{delimeter}.cube" if delimeter != "" else filepath
    if  delimeter != "":
        os.rename(src=filepath, dst=newpath)
        print(f"now '{newpath}'")

    file_contents = ""
    with open(newpath, "r") as open_file:
        file_contents = open_file.read()
        if "TITLE" in file_contents:
            for line in file_contents.splitlines():
                if line.startswith("TITLE"):
                    file_contents = file_contents.replace(line, f"TITLE \"{os.path.basename(newpath).removesuffix(".cube")}\"")
                    break
        else:
            file_contents = f"TITLE \"{os.path.basename(newpath).removesuffix(".cube")}\"\n{file_contents}"

    if file_contents != "":
        with open(newpath, "w+") as open_file:
            open_file.write(file_contents)


def find_files(existantpath):
    if os.path.isfile(existantpath):
        verify_and_process(existantpath)
        return

    # directory search
    for item in os.listdir(existantpath):
        find_files(os.path.join(existantpath, item))


if len(sys.argv) < 2:
    print("This utility requires arguments. Please include a path to a file or directory of files.")
    exit()

path = sys.argv[1]

if len(sys.argv) >= 3:
    delimeter = sys.argv[2]

if not os.path.exists(path):
    print(
        f"The specified path '{path}' does not point to a valid file or file directory. Please try again.")
    exit()

path = os.path.abspath(path)
find_files(path)
