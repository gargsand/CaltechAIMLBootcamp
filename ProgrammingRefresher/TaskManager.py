import hashlib
import json
import os

USERS_FILE = "users.json"
TASKS_DIR = "tasks"

if not os.path.exists(TASKS_DIR):
    os.makedirs(TASKS_DIR)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    return {}


def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)


def register():
    users = load_users()
    username = input("Enter a username: ")
    if username in users:
        print("Username already exists!")
        login(username)
    else:
        password = input("Enter a password: ")
        users[username] = hash_password(password)
        save_users(users)
        print("Registration successful!")


def login(username):
    users = load_users()
    if username is None:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
    else:
        password = input("Enter your password or press enter to exit: ")
    if username in users and users[username] == hash_password(password):
        print("Login successful!")
        return username
    print("Invalid username or password!")
    return None


def get_task_file(username):
    return os.path.join(TASKS_DIR, f"{username}.json")


def load_tasks(username):
    task_file = get_task_file(username)
    if os.path.exists(task_file):
        with open(task_file, "r") as file:
            return json.load(file)
    return []


def save_tasks(username, tasks):
    task_file = get_task_file(username)
    with open(task_file, "w") as file:
        json.dump(tasks, file)


def add_task(username):
    tasks = load_tasks(username)
    task_id = len(tasks) + 1
    description = input("Enter task description: ")
    tasks.append({"id": task_id, "description": description, "status": "Pending"})
    save_tasks(username, tasks)
    print("Task added successfully!")


def view_tasks(username):
    tasks = load_tasks(username)
    if not tasks:
        print("No tasks found.")
    else:
        for task in tasks:
            print(f"{task['id']}. {task['description']} - {task['status']}")


def mark_task_completed(username):
    tasks = load_tasks(username)
    task_id = int(input("Enter task ID to mark as completed: "))
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "Completed"
            save_tasks(username, tasks)
            print("Task marked as completed!")
            return
    print("Task not found.")


def delete_task(username):
    tasks = load_tasks(username)
    task_id = int(input("Enter task ID to delete: "))
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(username, tasks)
    print("Task deleted successfully!")


if __name__ == "__main__":
    user = None
    while True:
        if user is None:
            print("1. Register")
            print("2. Login")
            print("Press <<Enter>> to exit")
            choice = input("Choose an option: ")
            if choice == "1":
                register()
            elif choice == "2":
                user = login()
            elif choice == "":
                break
            else:
                print("Invalid choice!")

        while True and user is not None:
            print("\nTask Manager")
            print("1. Add Task")
            print("2. View Tasks")
            print("3. Mark Task as Completed")
            print("4. Delete Task")
            print("5. Logout")

            choice = input("Choose an option: ")
            if choice == "1":
                add_task(user)
            elif choice == "2":
                view_tasks(user)
            elif choice == "3":
                mark_task_completed(user)
            elif choice == "4":
                delete_task(user)
            elif choice == "5":
                print("Logging out...")
                break
                user = None
            else:
                print("Invalid choice. Please try again.")
