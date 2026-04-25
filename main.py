import json


tasks = []
print("WELCOME TO CLI TASK MANAGER")
tasks = json.load(open("tasks.json", "r"))
while True:
    print("                   ")
    print(" HABITRIX-MENU")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Mark Tasks Done")
    print("4. QUIT.")

    choice = input("WHAT DO YOU WANT TO DO??  ")

    if choice.upper() =="QUIT" or choice == "4":
        print("Thank you for using habitrix")
        break
    elif choice == "1":
        print("ADDING TASK......")
        name = input("enter the task name:")
        category = input("enter the category of the task")
        new_task = {
    "id": len(tasks) + 1,
    "name": name,
    "done": False,
    "category": category
}
        tasks.append(new_task)
        json.dump(tasks, open("tasks.json", "w"))

    elif choice =="2":
        print(" Listing TASKS.....")

        for task in tasks:
            if task["done"] == True:
                status ="[x]"
            else:
                status ="[ ]"
            print(status , task["name"], task["category"])

    elif choice =="3":
        print("Marking tasks done...")
        task_id = int(input("enter task id to mark done: "))
        for task in tasks:
            if task["id"] == task_id:
                task["done"] = True

    else:
        print(" Invalid choice , please try again :(")













