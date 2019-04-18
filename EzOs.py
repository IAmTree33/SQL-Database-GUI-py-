"""
EzOs
"""
import os
import shutil
def console_out(file):
    megabytes = str(os.stat(file).st_size / 1000000) + "MBs"
    print(f"Multiplied {file}'s contents")
    print(f"New File Size: {megabytes}")

def build_path(path):
    new_path = ""
    current = path.split("\\")
    for i in current:
        new_path += i
        new_path += "\\"

    return new_path

def multiply_file(file, console=False, loop=0, continue_=True, get_status=False):
    try:
        content = open(file,"r").read()
        run = True
    except MemoryError:
        run = False
        if continue_:
             if console:
                 print(f"File Size Too High:\nAttempting to interpret [File: '{file}']\nIgnoring [Loop: {loop}]")
             if get_status:
                 yield "<<readfailed>>"
             content = []
             with open(file) as text:
                 
                 for line in text:
                     try:
                         content.append(line.rstrip()[0:60]+"\n")
                     except MemoryError:
                         if console:
                             print(f"Writing to... [{file}]")
                         if get_status:
                             yield "<<writing>>"
                         break 
             edit = open(file,"a")
             for line in content:
                 edit.write(line)
             if console:
                 console_out(file)
                 
             edit.close()
             if get_status:
                 yield "<<complete>>"
        elif not continue_:
            if get_status:
                yield "<<failed>>"
            pass
             

    if run:        
        edit = open(file,"a")
        if not loop:
            edit.write(content)
            if get_status:
                yield "<<complete>>"
        else:
            if loop == "inf":
                if get_status:
                    yield "<<infloop>>"
                while 1:
                    edit.write(content)
                    if get_status:
                        yield "<<LOOP>>" 
                    if console:
                        console_out(file)
                
            else:
                if get_status:
                    yield "<<finiteloop>>"
                for i in range(loop):
                    edit.write(content)
                    if console:
                        console_out(file)
         
        
        edit.close() 

def go_back():
    current = os.getcwd()
    current_new = current.split("\\")
    current_new.pop(-1)
    path = ""
    for i in current_new:
        path += i
        path += '\\'
    os.chdir(path)


