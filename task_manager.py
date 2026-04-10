"""
Use the following username and password to access the admin rights 

username: admin
password: password

"""

#=====importing libraries===========
import os
from datetime import datetime

DATETIME_STRING_FORMAT = "%Y-%m-%d"


def reg_user(username_password):
    """User registration logic"""
    while True:
        new_username = input("Enter a new username: ").strip()
        if new_username in username_password:
            print("Username already exisists")
            continue
        new_password = input("Enter a new password: ")
        confirm_password = input("Confirm your password: ")
        if new_password == confirm_password:
            username_password[new_username] = new_password
            try:
                with open("user.txt", "w") as out_file:
                    user_data = [f"{u};{p}" for u, p in username_password.items()]
                    out_file.write("\n".join(user_data))
                print(f"Success: User '{new_username}' registered.")
                return username_password
            except IOError as e:
                print(f"File Error: Could not write to user.txt. {e}")
                return username_password
        else:
            print("Error: Passwords do not match. Please try again.")

def add_task(task_list, username_password):
    """Logic to add task to file"""
    task_username = input("Name: ")
    if task_username not in username_password:
        print("Error")
        return
    task_title = input("Title: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Error")
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": datetime.today(),
        "completed": False
    }
    task_list.append(new_task)
    save_tasks(task_list)
    print("Task added successfully.")

def view_all(task_list):
    """View all tasks logic"""
    for i, t in enumerate(task_list):
        status = "Yes" if t['completed'] else "No"
        print(f"--- Task {i+1} ---")
        print(f"Title: \t\t {t['title']}")
        print(f"Assigned to: \t {t['username']}")
        print(f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Completed: \t {status}")
        print(f"Description: \t {t['description']}\n")

def view_mine(task_list, curr_user):
    """Logic to view all users tasks"""
    while True:
        user_tasks = [(i, t) for i, t in enumerate(task_list) if t['username'] == curr_user]
        if not user_tasks:
            print("You have no tasks.")
            return
        for display_idx, (original_idx, t) in enumerate(user_tasks, 1):
            status = "Yes" if t['completed'] else "No"
            print(f"{display_idx}. {t['title']} (Completed: {status})")
        try:
            choice = int(input("Select task number (Or type -1 to return to main menu): "))
            if choice == -1:
                break
            orig_idx, task = user_tasks[choice - 1]
            action = input("Select: (c) Mark as complete, (e) Edit task: ").lower()
            if action == 'c':
                task['completed'] = True
                print("Task mcomplete.")
            elif action == 'e':
                if task['completed']:
                    print("Error")
                else:
                    sub_choice = input("Edit (u)sername or (d)ue date? ").lower()
                    if sub_choice == 'u':
                        task['username'] = input("New assigned user: ")
                    elif sub_choice == 'd':
                        new_date = input("New due date (YYYY-MM-DD): ")
                        task['due_date'] = datetime.strptime(new_date, DATETIME_STRING_FORMAT)
                    print("Task updated.")
            save_tasks(task_list)
        except (ValueError, IndexError):
            print("Invalid input.")

def generate_reports(task_list, username_password):
    """Logic to show all reports"""
    curr_date = datetime.today()
    total_tasks = len(task_list)
    total_users = len(username_password)
    completed_tasks = len([t for t in task_list if t['completed']])
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = len([t for t in task_list if not t['completed'] and t['due_date'] < curr_date])
    perc_incomplete = (uncompleted_tasks / total_tasks * 100) if total_tasks > 0 else 0
    perc_overdue = (overdue_tasks / total_tasks * 100) if total_tasks > 0 else 0
    with open("task_overview.txt", "w") as t_file:
        t_file.write("TASK OVERVIEW REPORT\n" + ("=" * 25) + "\n")
        t_file.write(f"Total tasks generated: \t\t{total_tasks}\n")
        t_file.write(f"Completed tasks: \t\t{completed_tasks}\n")
        t_file.write(f"Uncompleted tasks: \t\t{uncompleted_tasks}\n")
        t_file.write(f"Overdue tasks: \t\t\t{overdue_tasks}\n")
        t_file.write(f"Percentage incomplete: \t\t{perc_incomplete:.2f}%\n")
        t_file.write(f"Percentage overdue: \t\t{perc_overdue:.2f}%\n")
    
    with open("user_overview.txt", "w") as u_file:
        u_file.write("USER OVERVIEW REPORT\n" + ("=" * 25) + "\n")
        u_file.write(f"Total users registered: \t{total_users}\n")
        u_file.write(f"Total tasks generated: \t\t{total_tasks}\n\n")
        for user in username_password:
            user_tasks = [t for t in task_list if t['username'] == user]
            u_total = len(user_tasks)
            if u_total == 0:
                u_file.write(f"USER: {user}\n No tasks assigned.\n\n")
                continue
            u_comp = len([t for t in user_tasks if t['completed']])
            u_uncomp = u_total - u_comp
            u_overdue = len([t for t in user_tasks if not t['completed'] and t['due_date'] < curr_date])
            u_perc_total = (u_total / total_tasks * 100) if total_tasks > 0 else 0
            u_perc_comp = (u_comp / u_total * 100)
            u_perc_uncomp = (u_uncomp / u_total * 100)
            u_perc_overdue = (u_overdue / u_total * 100)
            u_file.write(f"USER: {user}\n")
            u_file.write(f"  Assigned: \t{u_total} ({u_perc_total:.2f}% of total)\n")
            u_file.write(f"  Completed: \t{u_perc_comp:.2f}%\n")
            u_file.write(f"  Remaining: \t{u_perc_uncomp:.2f}%\n")
            u_file.write(f"  Overdue: \t{u_perc_overdue:.2f}%\n\n")
    print("Success")

def display_stats(task_list, username_password):
    """Logic to display student statistics"""
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        print("Reports not found. Generating now...")
        generate_reports(task_list, username_password)
    print("\n--- Statistics ---")
    with open("task_overview.txt", "r") as f:
        print(f.read())

def save_tasks(task_list):
    """Logic to save added tasks to the file"""
    with open("tasks.txt", "w") as f:
        for t in task_list:
            status = "Yes" if t['completed'] else "No"
            line = [
                t['username'], t['title'], t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                status
            ]
            f.write(";".join(line) + "\n")

def main():
    """Logic to set up main menu"""
    username_password = {}
    if os.path.exists("user.txt"):
        with open("user.txt", "r") as f:
            for line in f:
                if ";" in line:
                    u, p = line.strip().split(";")
                    username_password[u] = p
    else:
        username_password = {"admin": "password"}

    task_list = []
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as f:
            for line in f:
                p = line.strip().split(";")
                if len(p) == 6:
                    task_list.append({
                        "username": p[0], "title": p[1], "description": p[2],
                        "due_date": datetime.strptime(p[3], DATETIME_STRING_FORMAT),
                        "assigned_date": datetime.strptime(p[4], DATETIME_STRING_FORMAT),
                        "completed": p[5] == "Yes"
                    })
    curr_user = None
    while curr_user is None:
        username = input("Username: ")
        password = input("Password: ")
        if username in username_password and username_password[username] == password:
            curr_user = username
        else:
            print("Invalid credentials.")
    while True:
        if curr_user == "admin":
            menu = input("r: register\na: add task\nva: view all\nvm: view mine\ngr: generate reports\nds: display stats\ne: exit\n: ").lower()
        else:
            menu = input("a: add task\nva: view all\nvm: view mine\ne: exit\n: ").lower()

        if menu == 'r' and curr_user == 'admin': reg_user(username_password)
        elif menu == 'a': add_task(task_list, username_password)
        elif menu == 'va': view_all(task_list)
        elif menu == 'vm': view_mine(task_list, curr_user)
        elif menu == 'gr' and curr_user == 'admin': generate_reports(task_list, username_password)
        elif menu == 'ds' and curr_user == 'admin': display_stats()
        elif menu == 'e': exit()

if __name__ == "__main__":
    main()