import sys
from termcolor import colored
import sqlite3

connection = sqlite3.connect("data.db")

args = sys.argv

def write_file(todo):
    status = 1
    try:
        with connection as con:
            cur = con.cursor()
            last = cur.execute("SELECT todo_number FROM todo ORDER BY todo_number DESC LIMIT 1").fetchone()
            if last is None:
                number = 1
            else:
                number = last[0] + 1
            cur.execute("INSERT INTO todo VALUES (?, ?, ?);", (number, status, todo))
    except IOError:
        print("Unable to open database")

def read_file():
    done = "[x]"
    undone = "[ ]"
    try:
        with connection as con:
            cur = con.cursor()
            rows = cur.execute("SELECT todo_number, todo_status, todo_text FROM todo").fetchall()
            for i in rows:
                symbol = undone if i[1] == 1 else done
                print("No: "+ str(i[0]) + " " + str(symbol) + " --- " + str(i[2])) 
    except IOError:
        print("Unable to open database")

def remove_task(num1):
    try:
        with connection as con:
            cur = con.cursor()
            cur.execute("DELETE FROM todo WHERE todo_number = ? ", (num1,))

    except IOError:
        print("Unable to open database")


def check_task(num2):
    done = "[x]"
    undone = "[ ]"
    try:
        with connection as con:
            cur = con.cursor()
            cur.execute("UPDATE todo SET todo_status = ? WHERE todo_number = ?", (0,num2))
            rows = cur.execute("SELECT todo_number, todo_status, todo_text FROM todo").fetchall()
            for i in rows:
                symbol = undone if i[1] == 1 else done
                print("No: "+ str(i[0]) + " " + str(symbol) + " --- " + str(i[2])) 

    except IOError:
        print("Unable to open database")

def read_undone():
    done = "[x]"
    undone = "[ ]"
    try:
        with connection as con:
            cur = con.cursor()
            rows = cur.execute("SELECT todo_number, todo_status, todo_text FROM todo WHERE todo_status = 1").fetchall()
            for i in rows:
                symbol = undone if i[1] == 1 else done
                print("No: "+ str(i[0]) + " " + str(symbol) + " --- " + str(i[2])) 
    except IOError:
        print("Unable to open database")

def delete_all():
    try:
        with connection as con:
            cur = con.cursor()
            cur.execute("DELETE from todo")

    except IOError:
        print("Unable to open database")



def todo(args):
    commands= ["-la", "-a" , "-r", "-c", "-l", "-d"]
    
    start_message = ("Command Line Todo application\n" + "=============================\n" 
    + "Command line arguments:\n" + "    -la  Lists all the tasks\n" +  "    -l   Lists all undone tasks\n" 
    + "    -a   Adds a new task\n" + "    -r   Removes a task\n" 
    + "    -c   Completes a task\n" 
    + colored( "    -d   Deletes all task", 'red'))
    
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE if not exists todo (todo_number INTEGER, todo_status INTEGER, todo_text TEXT)")

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




todo(args)