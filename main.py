print("*" * 40)

print("Welcome to StudyPilot!")
print("Your Personal Student Success Assistant")

print("*" * 40)



print("\n1) Register")
print("2) Login")
print("3) Exit")
choice=int(input("Enter your choice(1-3): "))



if choice==1:
    print("You have selected Register")
    Name=input("Please entter your name: ")
    RollNo=int(input("Please enter your Roll Number: "))

    # ---- Duplicate Roll Number Check ----
    roll_exists=False
    file = open("users.txt", "a+")
    file.seek(0)
    for line in file:
        data = line.strip().split(",")
        if int(data[1]) == RollNo:
            roll_exists=True
    file.close()

    if roll_exists:
        print("Roll Number already exists!")
    else:
        Password=int(input("Please enter your Password: "))

        file = open("users.txt", "a")
        file.write(f"{Name},{RollNo},{Password}\n")
        file.close()
        print("Registration Successful! You can now login with your credentials.")
        print("Welcome!", Name)

elif choice==2:
    print("You have selected Login")
    RollNo=int(input("Please enter your Roll Number: "))
    Password=int(input("Please enter your Password: "))   
    file = open("users.txt", "r")
    all_users_lines = file.readlines()
    file.close()

    found=False
    for line in all_users_lines:
        data = line.strip().split(",")
        if int(data[1]) == RollNo and int(data[2]) == Password:
            found=True
            print("Login Successful!")
            print("Welcome!", data[0])
            while True:
              print("\n========== STUDYPILOT DASHBOARD ==========")
              print("1. View Profile")
              print("2. Change Password")
              print("3. Study Planner")
              print("4. Logout")

              dashboard = int(input("Enter your choice: "))
              if dashboard == 1:
                print("\n========== MY PROFILE ==========")
                print("Name       :", data[0])
                print("Roll Number:", data[1])

              elif dashboard == 2:
                print("\nChange Password feature is under development.")
                old_password=(int(input("Enter your old password: ")))

                if old_password==Password:
                    new_password=(int(input("Enter your new password: ")))
                    users=[]

                    file = open("users.txt", "r")
                    for line in file:
                        user = line.strip().split(",")
                        if int(user[1]) == RollNo:
                            user[2] = str(new_password)
                        users.append(user)
                    file.close()

                    file = open("users.txt", "w")
                    for user in users:
                        file.write(f"{user[0]},{user[1]},{user[2]}\n")
                    file.close()

                    print("Password Changed Successfully!")
                else:
                    print("Old Password Incorrect!")

              elif dashboard == 3:
                 while True:
                   print("\n========== STUDY PLANNER ==========")
                   print("1. Add Task")
                   print("2. View Tasks")
                   print("3. Mark Task Completed")
                   print("4. Delete Task")
                   print("5. Back")
                   planner = int(input("Enter your choice: "))

                   if planner == 1:

                    task = input("Enter your study task: ")

                    if task.strip() == "":
                        print("Task cannot be empty!")
                    else:
                        # ---- Duplicate Task Check ----
                        duplicate=False
                        file = open("tasks.txt", "a+")
                        file.seek(0)
                        for line in file:
                            existing = line.strip().split(",")
                            if existing[0] == data[0] and existing[1].lower() == task.lower():
                                duplicate=True
                        file.close()

                        if duplicate:
                            print("Task already exists!")
                        else:
                            file = open("tasks.txt", "a")
                            file.write(f"{data[0]},{task},Pending\n")
                            file.close()
                            print("Task Added Successfully!")

                   elif planner == 2:

                    file = open("tasks.txt", "r")

                    print("\n========== YOUR TASKS ==========")

                    found_task = False

                    for line in file:
                        task = line.strip().split(",")

                        if task[0] == data[0]:
                            print("Task   :", task[1])
                            print("Status :", task[2])
                            print("---------------------------")
                            found_task = True

                    file.close()

                    if not found_task:
                        print("No Tasks Found!")

                   elif planner == 3:

                    print("\n===== MARK TASK COMPLETED =====")

                    file = open("tasks.txt", "r")

                    count = 1
                    all_tasks = []

                    for line in file:
                        task = line.strip().split(",")
                        all_tasks.append(task)

                        if task[0] == data[0]:
                            print(count, "-", task[1], "-", task[2])
                            count += 1

                    file.close()

                    if count == 1:
                        print("No Tasks Found!")
                    else:
                        task_number = int(input("\nEnter Task Number to Complete: "))

                        count = 1
                        for task in all_tasks:
                            if task[0] == data[0]:
                                if count == task_number:
                                    task[2] = "Completed"
                                count += 1

                        file = open("tasks.txt", "w")
                        for task in all_tasks:
                            file.write(f"{task[0]},{task[1]},{task[2]}\n")
                        file.close()

                        print("Task Marked as Completed Successfully!")

                   elif planner == 4:

                    print("\n===== DELETE TASK =====")

                    file = open("tasks.txt", "r")

                    count = 1
                    all_tasks = []

                    for line in file:
                        task = line.strip().split(",")
                        all_tasks.append(task)

                        if task[0] == data[0]:
                            print(count, "-", task[1], "-", task[2])
                            count += 1

                    file.close()

                    if count == 1:
                        print("No Tasks Found!")
                    else:
                        task_number = int(input("\nEnter Task Number to Delete: "))

                        count = 1
                        remaining_tasks = []
                        for task in all_tasks:
                            if task[0] == data[0]:
                                if count == task_number:
                                    count += 1
                                    continue
                                count += 1
                            remaining_tasks.append(task)

                        file = open("tasks.txt", "w")
                        for task in remaining_tasks:
                            file.write(f"{task[0]},{task[1]},{task[2]}\n")
                        file.close()

                        print("Task Deleted Successfully!")

                   elif planner == 5:
                    print("\nReturning to StudyPilot dashboard")
                    break

                   else:
                    print("Invalid Choice!")

              elif dashboard == 4:
                print("\nLogged Out Successfully!")

              else:
                print("Invalid Choice!")
    file.close()
    if not found:
        print("Invalid Roll Number or Password.")  
elif choice==3:
  print("Thank you for using StudyPilot! ")
  exit()
else:
    print("Invalid choice. Please try again.")