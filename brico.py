import os
import sys
import os.path
from os import path

def check_include(files):
    for dos in files:
        if ((".h" in dos) != True):
            print("[MAJOR]: [G6]: Include folder should only contain .h files:", dos)

def check_layout_inside_function(files):
    inside = open(files, "r")
    line = 0
    test = 0;
    index = 0
    for lines in inside:
        test += 1
        for char in lines:
            if (char == '\t' and ("Makefile" in files) != True):
                print("[MINOR]: [L2]: No tab should be replaced by an identation:", files, "line :", test)
    inside.close()
            
def check_function(files):
    inside = open(files, "r")
    line = 0
    for lines in inside:
        line += 1
        if len(lines) > 80:
            print("[MAJOR]: [F3]: The length of a line should not exceed 80 columns:", files, "line :", line, "(", len(lines), "> 80 )")
    inside.close()
    inside = open(files, "r")
    counter = 0
    begin_line = 0
    line = 0;
    if (".c" in files):
        for lines in inside:
            line += 1
            if (lines[0] == '{'):
                counter = 1
                begin_line = line
            if (counter > 0):
                counter += 1
            if (lines[0] == '}'):
                if (counter - 3 > 20):
                    print("[MAJOR]: [F4]: A function should not exceed 20 lines:", files, "line :", begin_line, "(", counter - 3, "> 20 )")
                counter = 0
    inside.close()
    inside = open(files, "r")
    line = 0
    counter = 0
    for lines in inside:
        line += 1
        for char in lines:
            if (char == '('):
                counter = 1
            if (counter > 0 and char == ','):
                counter += 1
            if (char == ')'):
                if (counter > 4):
                    print("[MAJOR]: [F5]: Function should not need more than 4 arguments:", files, "line :", line,"(", counter, "> 4 )")
    inside.close()
            
def check_global_scope(files):
    inside = open(files, "r")
    line_nbr = 0
    result = ""
    mid_res = ""
    for line in inside:
        if (line_nbr > 5):
            break
        if (line_nbr != 2 and line_nbr != 4):
            if (line_nbr == 1):
                for char in line:
                    mid_res += char
                    if (char == ','):
                        break
                mid_res += "\n"
                result += mid_res
            else:
                result += line
        line_nbr += 1
    if (".c" in  files):
        if (result != "/*\n** EPITECH PROJECT,\n** File description:\n*/\n"):
            print("[MAJOR]: [G1]: File header not correct:", files)
    if (files == "Makefile"):
        if (result != "##\n## EPITECH PROJECT,\n## File description:\n##\n"):
            print("[MAJOR]: [G1]: File header not correct:", files)
    inside.close()
    inside = open(files, "r")
    trailling_lines = 0;
    line_nbr = 0
    if (".c" in files):
        for lines in inside:
            line_nbr += 1
            if (lines == "\n"):
                trailling_lines += 1
            else:
                trailling_lines = 0
            if (trailling_lines == 2):
                trailling_lines = 0;
                print("[MINOR]: [G2]: There should be only one empty_line between implementations:", files, ": line:", line_nbr)
    inside.close()
    inside = open(files, "r")
    line = 0
    for lines in inside:
        line += 1
        index = 0
        for char in lines:
            if (char == ' ' and lines[index + 1] == '\n' and line > 7):
                print("[MINOR]: [G8]: Trailling space:", files, "line :", line)
            index += 1
    inside.close()
            
def check_file_organization(files):
    forbidden_files = [ ".o", ".gch", ".a", ".so", "~", "#", ".d" ]
    for ext in forbidden_files:
        if (ext in str(files)):
            print("[MAJOR]: [O1]: Delivery Folder should not contain", ext,"files:", files)
    if (any(ele.isupper() for ele in str(files)) == True and ("Makefile" in files) != True):
        print("[MAJOR]: [O4]: Name not in snake case convention:", files)

def check_coding_style(files):
    check_file_organization(files)
    check_global_scope(files)
    check_function(files)
    check_layout_inside_function(files)

def browse_directory(directory, paths):
    for files in directory:
        if path.isdir(files):
            if (files == "include"):
                check_include(os.listdir(files))
            browse_directory(os.listdir(files), paths + "/" + str(files))
        else:
            if (".c" in files or ".h" in files or "Makefile" in files):
                check_coding_style(paths + "/" + files)

def main():
    directory = os.listdir(".")
    paths = "."
    browse_directory(directory, paths)

main()
