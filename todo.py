import sys
from termcolor import colored
import sqlite3

connection = sqlite3.connect("data.db")

args = sys.argv

def write_file(todo):
    try:
        with open(file_name, "r") as f:
            f = f.readlines()
            lines=[]
            if len(f) > 0:
                for line in f:
                    lines.append(line)
            new_line= "[ ] " + todo + "\n"  
            lines.append(new_line)
        with open(file_name, "w") as nf:
            nf.writelines(lines)
    except IOError:
        print("Unable to write file: ", f)

def read_file():
    try:
        with open(file_name, "r") as f:
            f = f.readlines()
            if len(f) == 0:
                print("No todos for today! :)")
            else:
                for i, line in enumerate(f):
                    print(str(i+1) + " - " + line, end= "")   
    except IOError:
        print("Unable to write file: ", f)

def remove_task(num1):
    pass

def check_task(num2):
    pass
def read_undone():
    pass

def delete_all():
    pass



def remove_done_task():
    pass

def todo(args):
    commands= ["-la", "-a" , "-r", "-c", "-l", "-d", "-am", "-dd"]
    
    start_message = ("Command Line Todo application\n" + "=============================\n" 
    + "Command line arguments:\n" + "    -la  Lists all the tasks\n" +  "    -l   Lists all undone tasks\n" 
    + "    -a   Adds a new task\n" + "    -r   Removes a task\n" 
    + "    -c   Completes a task\n" +"    -am  Adds multiple new tasks\n" + colored( "    -dd  Deletes all done tasks\n", 'red')
    + colored( "    -d   Deletes all task", 'red'))
    
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE todo (todo_number INTEGER, todo_status INTEGER, todo_ TEXT)")

#if no arguments the basic message
    if len(args) == 1:
        print(start_message)

#not correct argument    
    elif len(args) > 1 and args[1] not in commands:
        print("Unsupported argument")
        print(start_message)

#list task
    elif len(args) == 2 and args[1] == commands[0]:
        read_file()

#no task specified
    elif len(args) == 2 and args[1] == commands[1]:
        print("Unable to add: no task provided")

#add task
    elif len(args) == 3 and args[1] == commands[1]:
        write_file(args[2])

#not able to remove task
    elif len(args) == 2 and args[1] == commands[2]:
        print("Unable to remove: no index provided")
#remove task
    elif len(args) == 3 and args[1] == commands[2]:
        if args[2].isnumeric():
            remove_task(int(args[2]))
        else:
            print("Unable to remove: index is not a number")

#not able to check task
    elif len(args) == 2 and args[1] == commands[3]:
        print("Unable to check: no index provided")

#check task
    elif len(args) == 3 and args[1] == commands[3]:
        if args[2].isnumeric():
            check_task(int(args[2]))
        else:
            print("Unable to remove: index is not a number")

#list undone_task
    elif len(args) == 2 and args[1] == commands[4]:
        read_undone()

#delete all tasks
    elif len(args) == 2 and args[1] == commands[5]:
        delete_all()


#delete done tasks
    elif len(args) == 2 and args[1] == commands[7]:
        remove_done_task()

todo(args)