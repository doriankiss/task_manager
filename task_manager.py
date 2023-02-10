"""Notes for improvement from Cogrammer feedback:
I see you are using the sleep method. Just keep in mind when working on a real project the sleep won't just delay something for a time, 
but will also freeze the user interface. So I recommend you read up on multi-threading and then run you sleep methods on another thread.

Also when asking for the date the user can enter any date of even any characters as long as it is in the format you provide. 
Then when you gr you get an exception. Just keep stuff like that it in mind because it is extremely important to cover every single 
possibility in real word apps.

Notes on improvements carried out:
- I believe I have successfully addressed the date issue.
- I don't know whether or not I've successfully implemented multi-threading.
"""

#=====importing libraries===========
from datetime import date
from datetime import datetime
import ast
import time
import threading

#=====defining functions======
def main_menu(username):
    # Presenting the menu to the user and making sure that the user input is coneverted to lower case. Make sure only
    # admin can access the user registration, report generating and display statistics features.
    if(username == "admin"):
        menu = input('''Select one of the following Options below:
                        r - Register a user
                        a - Add a task
                        va - View all tasks
                        vm - View my tasks
                        gr - Generate reports
                        ds - Display statistics
                        e - Exit
                        : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
                        a - Add a task
                        va - View all tasks
                        vm - View my tasks
                        e - Exit
                        : ''').lower()
    return menu

def reg_user(username):
    # Allow admin only to register new users.
    if(username != "admin"):
        print("\nOnly administrators are permitted to access this feature.\n")
        input("Press enter to return to the main menu. ")
        main_menu(username)
    print("Choose a new username and password for the new user you'd like to register.")
    usernameList = []
    with open('user.txt', 'r') as f:
        for line in f:
            userSplit = line.split(', ')
            existingUsername = userSplit[0]
            usernameList.append(existingUsername)
    
    newUsername = ""
    escape = False
    while(escape == False):
        while(len(newUsername) == 0):
            newUsername = input("Username: ")
        if(newUsername not in usernameList):
            # Loop until two matching passwords entered
            while True:
                newPassword = ""
                while(len(newPassword) == 0):
                    newPassword = input("Password: ")
                confirmPass = input("Reenter password to confirm: ")
                if(newPassword == confirmPass):
                    with open('user.txt', 'a') as f:
                        f.write(f"\n{newUsername}, {newPassword}")
                    print("\nUser registered successfully.\n")
                    escape = True
                    break
                else:
                    print("Passwords not identical. Try again.")
                    continue 
        # Choose to return to the main login options menu, or enter another username to register.
        else:
            print("That username already exists. Would you like to choose a unique username to register with, or return to the "
            "main menue to login using this username?")
            choice = 0
            while(choice != 1) and (choice != 2):
                choice = int(input("Enter <1> to try registering with a different unername "
                "or enter <2> to return to the main menu: "))
            if(choice == 1):
                newUsername = ""
            elif(choice == 2):
                escape = True
                break

def add_task():
    # Allow present user to assign tasks to himself or any other user.
    usernameList = []
    with open('user.txt', 'r') as f:
        for line in f:
            userSplit = line.split(', ')
            usernameList.append(userSplit[0])
    
    # Choose user to asign task to:
    escape = False
    while(escape == False):
        chosenUser = input("Enter the name of the user to which you would like to assign a task: ")
        if(chosenUser in usernameList):
            break
        else:
            choice = 0
            while(choice != 1) and (choice != 2):
                choice = int(input("Username not recognised. Enter <1> to try again, or <2> to return to the main menu: "))
        if(choice == 1):
            continue
        elif(choice == 2):
            username = ""
            escape = True
            break
        
    # Assign task to user, if valid username given
    if(len(chosenUser) > 0):
        taskName = ""
        while(len(taskName) == 0):
            taskName = input("Task name: ")
        taskDescription = ""
        while(len(taskDescription) == 0):
            taskDescription = input("Task description: ")
        today = date.today()
        assignedDate = today.strftime("%d %b %Y")
        # Need to change the below date input section in response to Cogrammer feedback
        dueDate = ""
        isValidDate = False
        while(len(dueDate) != 11) or (isValidDate == False):  # 11 is the number of chars in the requested date format
            try:    
                dueDate = input("Due date (DD Mmm YYYY), e.g. 20 Jan 2023: ")
                dueDateList = dueDate.split(" ")
                dueDay = dueDateList[0]
                dueMonth = dueDateList[1]
                dueYear = dueDateList[2]
                isValidDate = is_valid_date(dueDay, dueMonth, dueYear)
            except:
                continue
            
        taskComplete = "No"  # Purpose of this line unknown. I will leave it alone for now as there are no bugs in the program.
        
        task = {'User': chosenUser,
                'Task': taskName,
                'Description': taskDescription,
                'Assigned': assignedDate,
                'Due': dueDate,
                'Complete': "No"
        }
        with open('tasks.txt', 'a') as f:
            f.write(str(task) + "\n")

        print("Task assigned.\n")
        input("Press enter to continue. ")
        print(" ")

def view_all():
    # View all assigned tasks
    print(" ")
    with open('tasks.txt', 'r') as f:
        tasks = {}
        line_num = 1
        for line in f:
            line_dict = ast.literal_eval(line)  # https://www.tutorialspoint.com/How-to-convert-a-String-representation-of-a-Dictionary-to-a-dictionary-in-Python, accessed 08/01/2023, 01:56
            tasks[line_num] = line_dict
            line_num += 1
    
    for num in range(1, line_num):
        print(f"Task {num}:\t\t\t{tasks[num]['Task']}\nAssigned to:\t\t{tasks[num]['User']}\nDate assigned:\t\t"
            f"{tasks[num]['Assigned']}\n"
            f"Due date:\t\t{tasks[num]['Due']}\nTask complete?\t\t{tasks[num]['Complete']}\nTask decription:\n "
            f"{tasks[num]['Description']}\n")
            
    input("Press enter to return to the main menu. ")
    print(" ")
    return  

def view_mine(username):
    # View tasks assigned to user currently logged in. If no tasks, print this advisory and return to main menu.
    print(" ")
    with open('tasks.txt', 'r') as f:
        all_tasks = {}
        line_num_all = 1
        for line in f:
            line_dict = ast.literal_eval(line)  # https://www.tutorialspoint.com/How-to-convert-a-String-representation-of-a-Dictionary-to-a-dictionary-in-Python, accessed 08/01/2023, 01:56
            all_tasks[line_num_all] = line_dict
            line_num_all += 1

    my_tasks_nums = []
    for i in all_tasks:
        if all_tasks[i]['User'] == username:
            my_tasks_nums.append(i)

    if not my_tasks_nums:
        print("You have no tasks!\n")
        #time.sleep(1)
        threading.Thread(time.sleep(1)).start()  # Added in response to Cogrammer feedback. Is this correct usage?
        return
   
    for num in my_tasks_nums:
        print(f"Task {num}:\t\t\t{all_tasks[num]['Task']}\nAssigned to:\t\t{all_tasks[num]['User']}\nDate assigned:\t\t"
                f"{all_tasks[num]['Assigned']}\n"
                f"Due date:\t\t{all_tasks[num]['Due']}\nTask complete?\t\t{all_tasks[num]['Complete']}\nTask decription:\n "
                f"{all_tasks[num]['Description']}\n")

    my_task_num_strs = []
    for num in my_tasks_nums:
        my_task_num_strs.append(str(num))

    escape = False
    while escape == False:
        choice = input("Enter task number for more options, or enter -1 to return to the main menu: ")
        if choice in my_task_num_strs:
            escape = True
            break
        elif choice == '-1':
            escape = True
            print(" ")
            return
    
    choice_int = int(choice)
    print(f"\nTask {choice}:\t\t\t{all_tasks[choice_int]['Task']}\nAssigned to:\t\t{all_tasks[choice_int]['User']}\nDate assigned:\t\t"
            f"{all_tasks[choice_int]['Assigned']}\n"
            f"Due date:\t\t{all_tasks[choice_int]['Due']}\nTask complete?\t\t{all_tasks[choice_int]['Complete']}\nTask decription:\n "
            f"{all_tasks[choice_int]['Description']}\n")

    # If task marked as complete, give option to mark as incomplete or return to main menu. Completed tasks can't be edited.
    if all_tasks[choice_int]['Complete'] == 'Yes':
        print(f"Task {choice} is marked as complete, so it cannot be further edited. Would you like to mark it as incomplete?\n")
        mark_incomplete_or_return = False
        while(mark_incomplete_or_return != '1') and (mark_incomplete_or_return != '2'):
            mark_incomplete_or_return = input("Enter <1> to mark the task as incomplete, or enter <2> to return to the main menu: ")
        if mark_incomplete_or_return == '1':
            all_tasks[choice_int]['Complete'] = "No"
            print(f"\nTask {choice}:\t\t\t{all_tasks[choice_int]['Task']}\nAssigned to:\t\t{all_tasks[choice_int]['User']}\nDate assigned:\t\t"
                    f"{all_tasks[choice_int]['Assigned']}\n"
                    f"Due date:\t\t{all_tasks[choice_int]['Due']}\nTask complete?\t\t{all_tasks[choice_int]['Complete']}\nTask decription:\n "
                    f"{all_tasks[choice_int]['Description']}\n")
        elif mark_incomplete_or_return == '2':
            return

    
    complete_or_edit = input("Enter <1> to mark the task as complete, or <2> to edit the task: ")
    if complete_or_edit == "1":
        all_tasks[choice_int]['Complete'] = "Yes"
    elif complete_or_edit == "2":
        user_or_due = input("\nEnter <1> to edit the user the task is assigned to, or <2> to edit the task's due-date: ")
        if user_or_due == "1":
            escape = False
            while escape == False:
                all_tasks[choice_int]['User'] = input("User: ")
                if all_tasks[choice_int]['User'] in usernameList:
                    escape = True
                    break
                else:
                    print("\nThat username is not yet registered. Please try again.\n")
                    continue
        elif user_or_due == "2":
            # Validate this date
            #all_tasks[choice_int]['Due'] = input("\nDue date (DD Mmm YYYY), e.g. 20 Jan 2023: ")
            
            dueDate = ""
            isValidDate = False
            while(len(dueDate) != 11) or (isValidDate == False):  # 11 is the number of chars in the requested date format
                try:    
                    dueDate = input("Due date (DD Mmm YYYY), e.g. 20 Jan 2023: ")
                    dueDateList = dueDate.split(" ")
                    dueDay = dueDateList[0]
                    dueMonth = dueDateList[1]
                    dueYear = dueDateList[2]
                    isValidDate = is_valid_date(dueDay, dueMonth, dueYear)
                except:
                    continue
            
            all_tasks[choice_int]['Due'] = dueDate

    print(f"\nTask {choice}:\t\t\t{all_tasks[choice_int]['Task']}\nAssigned to:\t\t{all_tasks[choice_int]['User']}\nDate assigned:\t\t"
            f"{all_tasks[choice_int]['Assigned']}\n"
            f"Due date:\t\t{all_tasks[choice_int]['Due']}\nTask complete?\t\t{all_tasks[choice_int]['Complete']}\nTask decription:\n "
            f"{all_tasks[choice_int]['Description']}\n")
    
    # Overwrite tasks.txt with updated tasks
    with open('tasks.txt', 'w') as f:
        for i in all_tasks:
            f.write(str(all_tasks[i]) + '\n')

    input("\nPress enter to continue. ")

def generate_reports(username):
    # Accessible to admin only. Generate user friendly overviews, as well as easily accessible save-files for these.
    if(username != "admin"):
        print("\nOnly administrators are permitted to access this feature.\n")
        input("Press enter to return to the main menu. ")
        return
    
    # Section for generating task_overview.txt
    line_num = 1
    tasks = {}
    with open('tasks.txt', 'r') as f:
        for line in f:
            line_dict = ast.literal_eval(line)  # https://www.tutorialspoint.com/How-to-convert-a-String-representation-of-a-Dictionary-to-a-dictionary-in-Python, accessed 08/01/2023, 01:56
            tasks[line_num] = line_dict
            line_num += 1

    num_tasks = line_num -1
    #print(num_tasks)
    num_tasks_completed = 0
    num_tasks_overdue = 0
    today = datetime.today()
    for i in range(1, line_num):
        if tasks[i]['Complete'] == 'Yes':
            num_tasks_completed += 1
        due = datetime.strptime(tasks[i]['Due'], '%d %b %Y')
        if tasks[i]['Complete'] == 'No' and due < today:
            num_tasks_overdue += 1
        
    num_tasks_incomplete = num_tasks - num_tasks_completed

    percentage_tasks_incomplete = num_tasks_incomplete / num_tasks * 100
    percentage_tasks_overdue = num_tasks_overdue / num_tasks * 100

    task_overview_dict = {'num_tasks': num_tasks,
                            'num_completed': num_tasks_completed,
                            'num_incomplete': num_tasks_incomplete,
                            'num_overdue': num_tasks_overdue,
                            'percent_incomplete': percentage_tasks_incomplete,
                            'percent_overdue': percentage_tasks_overdue
                            }

    with open('task_overview_save.txt', 'w') as f:
        f.write(str(task_overview_dict))

    with open('task_overview.txt', 'w') as f:
        f.write(f"Total number of tasks generated and tracked using task_manager.py: {task_overview_dict['num_tasks']}\n"
                f"Total number of completed tasks: {task_overview_dict['num_completed']}\n"
                f"Total number of incomplete tasks: {task_overview_dict['num_incomplete']}\n"
                f"Total number of overdue tasks: {task_overview_dict['num_overdue']}\n"
                f"Percentage of tasks incomplete: {task_overview_dict['percent_incomplete']}\n"
                f"Percentage of tasks overdue: {task_overview_dict['percent_overdue']}")
    
    # Section for generating user_overview.txt
    username_list = []
    with open('user.txt', 'r') as f:
        for line in f:
            user_password_split = line.split(', ')
            username_list.append(user_password_split[0])

    user_overview_dict = {}

    num_users = 0
    for username in username_list:
        num_users += 1
        user_overview_dict[username] = {'num_tasks_assigned_to' : 0,  # Done
                                        'percent_total_tasks_assigned_to': 0,  # Done
                                        'num_tasks_assigned_to_complete': 0,  # Done
                                        'percent_tasks_assigned_to_complete': 0,  # Done
                                        'num_tasks_assigned_to_incomplete': 0,  # Done
                                        'percent_tasks_assigned_to_incomplete': 0,
                                        'num_tasks_assigned_to_overdue': 0,  # Done
                                        'percent_tasks_assigned_to_overdue': 0
                                        }

    user_overview_dict['num_users'] = num_users
    user_overview_dict['num_tasks'] = num_tasks

    for username in username_list:
        for task_num in tasks:
            if tasks[task_num]['User'] == username:
                user_overview_dict[username]['num_tasks_assigned_to'] += 1

    for task_num in tasks:
        if tasks[task_num]['Complete'] == 'Yes':
            username_holder = tasks[task_num]['User']
            user_overview_dict[username_holder]['num_tasks_assigned_to_complete'] += 1
        else:
            username_holder = tasks[task_num]['User']
            user_overview_dict[username_holder]['num_tasks_assigned_to_incomplete'] += 1
        due = datetime.strptime(tasks[task_num]['Due'], '%d %b %Y')
        if due < today:
            username_holder = tasks[task_num]['User']
            user_overview_dict[username_holder]['num_tasks_assigned_to_overdue'] += 1
    
    for username in username_list:
        # Using try-except to avoid division by zero error
        try:
            user_overview_dict[username]['percent_total_tasks_assigned_to'] = user_overview_dict[username]['num_tasks_assigned_to'] / num_tasks * 100
        except: 
            user_overview_dict[username]['percent_total_tasks_assigned_to'] = 0

        try:
            user_overview_dict[username]['percent_tasks_assigned_to_complete'] = user_overview_dict[username]['num_tasks_assigned_to_complete'] / user_overview_dict[username]['num_tasks_assigned_to'] * 100
        except:
            user_overview_dict[username]['percent_tasks_assigned_to_complete'] = 0
        
        try:    
            user_overview_dict[username]['percent_tasks_assigned_to_incomplete'] = user_overview_dict[username]['num_tasks_assigned_to_incomplete'] / user_overview_dict[username]['num_tasks_assigned_to'] * 100
        except:
            user_overview_dict[username]['percent_tasks_assigned_to_incomplete'] = 0

        try:
            user_overview_dict[username]['percent_tasks_assigned_to_overdue'] = user_overview_dict[username]['num_tasks_assigned_to_overdue'] / user_overview_dict[username]['num_tasks_assigned_to'] * 100
        except:
            user_overview_dict[username]['percent_tasks_assigned_to_overdue'] = 0

    # print(user_overview_dict)

    with open('user_overview_save.txt', 'w') as f:
        f.write(str(user_overview_dict))

    with open('user_overview.txt', 'w') as f:
        f.write(f"Total number of users registered with task_manager.py: {user_overview_dict['num_users']}\n"
                f"Total number of tasks that have been generated and tracked using task_manager.py: {user_overview_dict['num_tasks']}\n")
        for username in username_list:
            f.write(f"\nUser: {username}:\n"
                    f"Number of tasks assigned to {username}: {user_overview_dict[username]['num_tasks_assigned_to']}\n"
                    f"Percentage of total number of tasks, which have been assigned to {username}: {user_overview_dict[username]['percent_total_tasks_assigned_to']}\n"
                    f"Percentage of tasks assigned to {username} which are complete: {user_overview_dict[username]['percent_tasks_assigned_to_complete']}\n"
                    f"Percentage of tasks assigned to {username} which are incomplete: {user_overview_dict[username]['percent_tasks_assigned_to_incomplete']}\n"
                    f"Percentage of tasks assigned to {username} which are overdue: {user_overview_dict[username]['percent_tasks_assigned_to_overdue']}\n")
    
    print("\nReports generated!\n")
    # Section for returning to main menu
    #time.sleep(1)
    threading.Thread(time.sleep(1)).start()  # Added threading in response to Cogrammer feedback. Is this correct usage?
    return

def display_stats(username):
    # Generate up-to-date reports to ensure subsequently displayed stats are accurate
    generate_reports(username)
    
    # Print out contents of task_overview.txt and user_overview.txt to the terminal in a user-friendly format. For admin only.
    if(username != "admin"):
        print("\nOnly administrators are permitted to access this feature.\n")
        input("Press enter to return to the main menu. ")
        return

    with open('task_overview.txt', 'r') as f:
        print('\nTask overview:\n')
        for line in f:
            stripped_line = line.strip('\n')
            print(stripped_line)

    with open('user_overview.txt', 'r') as f:
        print('\nUser overview:\n')
        for line in f:
            stripped_line = line.strip('\n')
            print(stripped_line)

    input("\nPress enter to return to the main menu. ")  # To allow user to read printed reports before choosing when to return to menu
    print(" ")

def gen_username_list():
    usernameList = []
    with open('user.txt', 'r') as f:
        for line in f:
            lineList = line.split(', ')
            usernameList.append(lineList[0])

    return usernameList

def gen_password_list():
    passwordList = []
    with open('user.txt', 'r') as f:
        for line in f:
            lineList = line.split(', ')
            passwordList.append(lineList[1])
    return passwordList

def is_valid_date(day, month, year):
    # Function learnt from anon and Sash Sinha, https://stackoverflow.com/questions/9987818/in-python-how-to-check-if-a-date-is-valid, accessed 28/01/2023
    # Convert alphabetic Mmm to digital MM month format
    if month == "Jan":
        digi_month = 1
    elif month == "Feb":
        digi_month = 2
    elif month == "Mar":
        digi_month = 3
    elif month == "Apr":
        digi_month = 4
    elif month == "May":
        digi_month = 5
    elif month == "Jun":
        digi_month = 6
    elif month == "Jul":
        digi_month == 7
    elif month == "Aug":
        digi_month = 8
    elif month == "Sep":
        digi_month = 9
    elif month == "Oct":
        digi_month = 10
    elif month == "Nov":
        digi_month = 11
    elif month == "Dec":
        digi_month = 12

    int_day = int(day)
    int_year = int(year)

    day_count_for_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if int_year%4==0 and (int_year%100 != 0 or int_year%400==0):
        day_count_for_month[2] = 29
    return (1 <= digi_month <= 12 and 1 <= int_day <= day_count_for_month[digi_month])

#====Login section====
usernameList = gen_username_list()
passwordList = gen_password_list()

escape = False
while(escape == False):
    username = input("Username: ")
    givenPassword = input("Password: ")
    if(username in usernameList):
        userIndex = usernameList.index(username)
        correctPassword = passwordList[userIndex].strip()  # It needed to be stripped because it was including a newline for some unknown reason.
    if(username in usernameList) and (givenPassword == correctPassword):
        escape = True
        break
    else:
        choice = 0
        while(choice != 1) and (choice != 2):
            choice = int(input("Username and/or password incorrect. Enter <1> to try again, or <2> to exit the program: "))
        if(choice == 1):
            continue
        elif(choice == 2):
            print('Goodbye!!!')
            exit()

# username = "admin"  # Can be temporarily pre-set num for testing of certain functions

while True:
    menu = main_menu(username)

    if menu == 'r':
        reg_user(username)

    elif menu == 'a':
        add_task()
        
    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine(username)

    elif menu == 'gr':
        generate_reports(username)

    elif menu == 'ds':
        display_stats(username)

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")