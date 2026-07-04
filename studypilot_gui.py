"""
StudyPilot - GUI Version
-------------------------
Same features as the console main.py (Register, Login, View Profile,
Change Password, Study Planner: Add/View/Mark Complete/Delete Task),
styled with a dark / gold theme (black background + gold accents +
bordered cards), matching the reference design.

Uses the SAME files as the console app:
    users.txt  -> Name,RollNo,Password
    tasks.txt  -> Name,Task,Status

This file does NOT modify or replace main.py - it is a separate,
additional way to use StudyPilot with a GUI.
"""

import tkinter as tk
from tkinter import messagebox

# ------------------------------------------------------------------
# THEME / COLORS  (dark + gold)
# ------------------------------------------------------------------
BG_COLOR      = "#0D0D0D"   # near-black app background
CARD_COLOR    = "#1B1B1B"   # dark card background
HEADER_COLOR  = "#111111"   # header strip
ACCENT_COLOR  = "#F2C230"   # gold
ACCENT_HOVER  = "#D9AC1F"   # darker gold (hover)
ENTRY_BG      = "#262626"   # dark input box
TEXT_DARK     = "#1A1A1A"   # dark text (on gold buttons)
TEXT_LIGHT    = "#F5F5F5"   # light body text
TEXT_MUTED    = "#C9AF5E"   # muted gold-gray (subtitles)
ERROR_COLOR   = "#E05C5C"
SUCCESS_COLOR = "#4CAF6D"

FONT_TITLE  = ("Georgia", 22, "bold")
FONT_SUB    = ("Segoe UI", 10)
FONT_HEAD   = ("Georgia", 16, "bold")
FONT_OPTION = ("Segoe UI", 12, "bold")
FONT_LABEL  = ("Segoe UI", 11)
FONT_ENTRY  = ("Segoe UI", 12)


# ------------------------------------------------------------------
# FILE / DATA HELPERS  (independent of the GUI; same file format and
# behavior as the console app)
# ------------------------------------------------------------------
USERS_FILE = "users.txt"
TASKS_FILE = "tasks.txt"


def read_users():
    try:
        file = open(USERS_FILE, "r")
    except FileNotFoundError:
        return []
    lines = file.readlines()
    file.close()
    users = []
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        users.append(line.split(","))
    return users


def write_users(users):
    file = open(USERS_FILE, "w")
    for user in users:
        file.write(f"{user[0]},{user[1]},{user[2]}\n")
    file.close()


def read_tasks():
    try:
        file = open(TASKS_FILE, "r")
    except FileNotFoundError:
        return []
    lines = file.readlines()
    file.close()
    tasks = []
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        tasks.append(line.split(","))
    return tasks


def write_tasks(tasks):
    file = open(TASKS_FILE, "w")
    for task in tasks:
        file.write(f"{task[0]},{task[1]},{task[2]}\n")
    file.close()


def roll_number_exists(roll_no):
    for user in read_users():
        if int(user[1]) == roll_no:
            return True
    return False


def register_user(name, roll_no, password):
    if roll_number_exists(roll_no):
        return False, "Roll Number already exists!"
    users = read_users()
    users.append([name, str(roll_no), str(password)])
    write_users(users)
    return True, "Registration Successful! You can now login."


def login_user(roll_no, password):
    for user in read_users():
        if int(user[1]) == roll_no and int(user[2]) == password:
            return user
    return None


def change_password(roll_no, old_password, new_password):
    users = read_users()
    matched = None
    for user in users:
        if int(user[1]) == roll_no:
            matched = user
            break

    if matched is None:
        return False, "User not found!"

    if int(matched[2]) != old_password:
        return False, "Old Password Incorrect!"

    for user in users:
        if int(user[1]) == roll_no:
            user[2] = str(new_password)
    write_users(users)
    return True, "Password Changed Successfully!"


def task_already_exists(name, task_text):
    for task in read_tasks():
        if task[0] == name and task[1].lower() == task_text.lower():
            return True
    return False


def add_task(name, task_text):
    if task_text.strip() == "":
        return False, "Task cannot be empty!"
    if task_already_exists(name, task_text):
        return False, "Task already exists!"
    tasks = read_tasks()
    tasks.append([name, task_text, "Pending"])
    write_tasks(tasks)
    return True, "Task Added Successfully!"


def get_tasks_for_user(name):
    result = []
    for task in read_tasks():
        if task[0] == name:
            result.append(task)
    return result


def mark_task_complete_by_index(name, index_in_user_list):
    all_tasks = read_tasks()
    user_task_positions = [i for i, t in enumerate(all_tasks) if t[0] == name]
    if index_in_user_list < 0 or index_in_user_list >= len(user_task_positions):
        return False
    real_index = user_task_positions[index_in_user_list]
    all_tasks[real_index][2] = "Completed"
    write_tasks(all_tasks)
    return True


def delete_task_by_index(name, index_in_user_list):
    all_tasks = read_tasks()
    user_task_positions = [i for i, t in enumerate(all_tasks) if t[0] == name]
    if index_in_user_list < 0 or index_in_user_list >= len(user_task_positions):
        return False
    real_index = user_task_positions[index_in_user_list]
    all_tasks.pop(real_index)
    write_tasks(all_tasks)
    return True


# ------------------------------------------------------------------
# ROUNDED RECT HELPER
# ------------------------------------------------------------------
def round_rect_points(x1, y1, x2, y2, radius):
    return [
        x1 + radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
        x2, y2 - radius, x2, y2, x2 - radius, y2, x1 + radius, y2,
        x1, y2, x1, y2 - radius, x1, y1 + radius, x1, y1,
    ]


# ------------------------------------------------------------------
# REUSABLE WIDGETS
# ------------------------------------------------------------------
class RoundedButton(tk.Canvas):
    """
    variant="primary"   -> solid gold fill, dark text   (main actions)
    variant="secondary" -> dark fill, gold outline + gold text (Back, etc.)
    """
    def __init__(self, parent, text, command, width=320, height=50,
                 radius=12, variant="primary", icon=None, font=FONT_OPTION,
                 parent_bg=CARD_COLOR):
        super().__init__(parent, width=width, height=height,
                          bg=parent_bg, highlightthickness=0)
        self.command = command
        self.width = width
        self.height = height
        self.radius = radius
        self.text = text
        self.icon = icon
        self.font = font

        if variant == "primary":
            self.fill = ACCENT_COLOR
            self.fill_hover = ACCENT_HOVER
            self.text_color = TEXT_DARK
            self.border = ""
        else:
            self.fill = parent_bg
            self.fill_hover = "#231D08"
            self.text_color = ACCENT_COLOR
            self.border = ACCENT_COLOR

        self._draw(self.fill)

        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Enter>", lambda e: self._draw(self.fill_hover))
        self.bind("<Leave>", lambda e: self._draw(self.fill))

    def _draw(self, fill_color):
        self.delete("all")
        outline_width = 2 if self.border else 0
        self.create_polygon(
            round_rect_points(2, 2, self.width - 2, self.height - 2, self.radius),
            smooth=True, fill=fill_color, outline=self.border, width=outline_width)

        label = f"{self.icon}  {self.text}" if self.icon else self.text
        self.create_text(self.width / 2, self.height / 2, text=label,
                          fill=self.text_color, font=self.font, anchor="center")


class EntryField(tk.Frame):
    """Gold label above a rounded dark input box."""
    def __init__(self, parent, label_text, show=None, width=320, parent_bg=CARD_COLOR):
        super().__init__(parent, bg=parent_bg)

        tk.Label(self, text=label_text, bg=parent_bg, fg=ACCENT_COLOR,
                  font=("Segoe UI", 9, "bold"), anchor="w"
                  ).pack(fill="x", pady=(0, 4))

        box = tk.Canvas(self, width=width, height=46, bg=parent_bg,
                         highlightthickness=0)
        box.pack()
        box.create_polygon(round_rect_points(1, 1, width - 1, 45, 10),
                            smooth=True, fill=ENTRY_BG, outline="")

        self.var = tk.StringVar()
        entry = tk.Entry(box, textvariable=self.var, show=show,
                          font=FONT_ENTRY, bg=ENTRY_BG, fg=TEXT_LIGHT,
                          insertbackground=TEXT_LIGHT, relief="flat",
                          highlightthickness=0)
        entry.place(x=14, y=9, width=width - 28, height=28)
        self.entry = entry

    def get(self):
        return self.var.get()


class Card(tk.Frame):
    """Dark bordered card container (gold outline), like the reference
    design's rounded panel."""
    def __init__(self, parent, width=380):
        super().__init__(parent, bg=CARD_COLOR, highlightbackground=ACCENT_COLOR,
                          highlightthickness=1, bd=0)
        self.inner = tk.Frame(self, bg=CARD_COLOR)
        self.inner.pack(padx=24, pady=24, fill="both")


# ------------------------------------------------------------------
# MAIN APPLICATION
# ------------------------------------------------------------------
class StudyPilotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("StudyPilot")
        self.geometry("440x680")
        self.resizable(False, False)
        self.configure(bg=BG_COLOR)

        self.current_user = None  # [Name, RollNo, Password]

        self.header = tk.Frame(self, bg=HEADER_COLOR, height=110)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        tk.Label(self.header, text="📖 StudyPilot", bg=HEADER_COLOR,
                  fg=ACCENT_COLOR, font=FONT_TITLE).pack(pady=(20, 0))
        tk.Label(self.header, text="Your Personal Student Success Assistant",
                  bg=HEADER_COLOR, fg=TEXT_MUTED, font=FONT_SUB).pack()

        border_line = tk.Frame(self, bg=ACCENT_COLOR, height=2)
        border_line.pack(fill="x")

        self.body = tk.Frame(self, bg=BG_COLOR)
        self.body.pack(fill="both", expand=True, padx=20, pady=20)

        self.show_welcome()

    # ---------- helpers ----------
    def clear_body(self):
        for widget in self.body.winfo_children():
            widget.destroy()

    def new_card(self):
        card = Card(self.body)
        card.pack(fill="both", expand=True)
        return card.inner

    def card_title(self, parent, text):
        tk.Label(parent, text=text, bg=CARD_COLOR, fg=ACCENT_COLOR,
                  font=FONT_HEAD).pack(pady=(0, 20))

    # ---------- WELCOME ----------
    def show_welcome(self):
        self.clear_body()
        c = self.new_card()
        self.card_title(c, "Welcome!")

        RoundedButton(c, "Register", self.show_register,
                      icon="👤", parent_bg=CARD_COLOR).pack(pady=8)
        RoundedButton(c, "Login", self.show_login,
                      icon="🔑", parent_bg=CARD_COLOR).pack(pady=8)
        RoundedButton(c, "Exit", self.destroy, icon="🚪",
                      variant="secondary", parent_bg=CARD_COLOR).pack(pady=8)

    # ---------- REGISTER ----------
    def show_register(self):
        self.clear_body()
        c = self.new_card()
        self.card_title(c, "Create Account")

        name_field = EntryField(c, "NAME"); name_field.pack(pady=6)
        roll_field = EntryField(c, "ROLL NUMBER"); roll_field.pack(pady=6)
        pass_field = EntryField(c, "PASSWORD", show="*"); pass_field.pack(pady=6)

        def do_register():
            name = name_field.get().strip()
            roll_text = roll_field.get().strip()
            pass_text = pass_field.get().strip()

            if name == "" or roll_text == "" or pass_text == "":
                messagebox.showwarning("StudyPilot", "Please fill all fields.")
                return
            try:
                roll_no = int(roll_text)
                password = int(pass_text)
            except ValueError:
                messagebox.showwarning(
                    "StudyPilot", "Roll Number and Password must be numbers.")
                return

            ok, msg = register_user(name, roll_no, password)
            if ok:
                messagebox.showinfo("StudyPilot", msg)
                self.show_welcome()
            else:
                messagebox.showerror("StudyPilot", msg)

        RoundedButton(c, "Register", do_register, icon="✅",
                      parent_bg=CARD_COLOR).pack(pady=(16, 8))
        RoundedButton(c, "Back", self.show_welcome, icon="←",
                      variant="secondary", parent_bg=CARD_COLOR).pack(pady=6)

    # ---------- LOGIN ----------
    def show_login(self):
        self.clear_body()
        c = self.new_card()
        self.card_title(c, "Login")

        roll_field = EntryField(c, "ROLL NUMBER"); roll_field.pack(pady=6)
        pass_field = EntryField(c, "PASSWORD", show="*"); pass_field.pack(pady=6)

        def do_login():
            roll_text = roll_field.get().strip()
            pass_text = pass_field.get().strip()
            if roll_text == "" or pass_text == "":
                messagebox.showwarning("StudyPilot", "Please fill all fields.")
                return
            try:
                roll_no = int(roll_text)
                password = int(pass_text)
            except ValueError:
                messagebox.showwarning(
                    "StudyPilot", "Roll Number and Password must be numbers.")
                return

            user = login_user(roll_no, password)
            if user is None:
                messagebox.showerror(
                    "StudyPilot", "Invalid Roll Number or Password.")
                return

            self.current_user = user
            self.show_dashboard()

        RoundedButton(c, "Login", do_login, icon="🔑",
                      parent_bg=CARD_COLOR).pack(pady=(16, 8))
        RoundedButton(c, "Back", self.show_welcome, icon="←",
                      variant="secondary", parent_bg=CARD_COLOR).pack(pady=6)

    # ---------- DASHBOARD ----------
    def show_dashboard(self):
        self.clear_body()
        c = self.new_card()
        name = self.current_user[0]
        self.card_title(c, f"Welcome, {name}!")

        RoundedButton(c, "View Profile", self.show_profile, icon="👤",
                      parent_bg=CARD_COLOR).pack(pady=6)
        RoundedButton(c, "Change Password", self.show_change_password, icon="🔒",
                      parent_bg=CARD_COLOR).pack(pady=6)
        RoundedButton(c, "Study Planner", self.show_planner, icon="📘",
                      parent_bg=CARD_COLOR).pack(pady=6)
        RoundedButton(c, "Logout", self.do_logout, icon="🚪",
                      variant="secondary", parent_bg=CARD_COLOR).pack(pady=6)

    def do_logout(self):
        self.current_user = None
        messagebox.showinfo("StudyPilot", "Logged Out Successfully!")
        self.show_welcome()

    # ---------- PROFILE ----------
    def show_profile(self):
        self.clear_body()
        c = self.new_card()
        self.card_title(c, "My Profile")

        name, roll_no, _ = self.current_user
        info = tk.Frame(c, bg=ENTRY_BG)
        info.pack(fill="x", pady=(0, 10))
        tk.Label(info, text=f"Name        :  {name}", bg=ENTRY_BG,
                  fg=TEXT_LIGHT, font=FONT_LABEL, anchor="w"
                  ).pack(fill="x", padx=16, pady=(14, 4))
        tk.Label(info, text=f"Roll Number :  {roll_no}", bg=ENTRY_BG,
                  fg=TEXT_LIGHT, font=FONT_LABEL, anchor="w"
                  ).pack(fill="x", padx=16, pady=(4, 14))

        RoundedButton(c, "Back", self.show_dashboard, icon="←",
                      variant="secondary", parent_bg=CARD_COLOR).pack(pady=16)

    # ---------- CHANGE PASSWORD ----------
    def show_change_password(self):
        self.clear_body()
        c = self.new_card()
        self.card_title(c, "Change Password")

        old_field = EntryField(c, "OLD PASSWORD", show="*"); old_field.pack(pady=6)
        new_field = EntryField(c, "NEW PASSWORD", show="*"); new_field.pack(pady=6)

        def do_change():
            old_text = old_field.get().strip()
            new_text = new_field.get().strip()
            if old_text == "" or new_text == "":
                messagebox.showwarning("StudyPilot", "Please fill all fields.")
                return
            try:
                old_password = int(old_text)
                new_password = int(new_text)
            except ValueError:
                messagebox.showwarning("StudyPilot", "Password must be a number.")
                return

            roll_no = int(self.current_user[1])
            ok, msg = change_password(roll_no, old_password, new_password)
            if ok:
                self.current_user[2] = str(new_password)
                messagebox.showinfo("StudyPilot", msg)
                self.show_dashboard()
            else:
                messagebox.showerror("StudyPilot", msg)

        RoundedButton(c, "Update Password", do_change, icon="🔒",
                      parent_bg=CARD_COLOR).pack(pady=(16, 8))
        RoundedButton(c, "Back", self.show_dashboard, icon="←",
                      variant="secondary", parent_bg=CARD_COLOR).pack(pady=6)

    # ---------- STUDY PLANNER ----------
    def show_planner(self):
        self.clear_body()
        c = self.new_card()
        self.card_title(c, "Study Planner")

        RoundedButton(c, "Add Task", self.show_add_task, icon="➕",
                      parent_bg=CARD_COLOR).pack(pady=5)
        RoundedButton(c, "View Tasks", self.show_view_tasks, icon="📋",
                      parent_bg=CARD_COLOR).pack(pady=5)
        RoundedButton(c, "Mark Task Completed", self.show_mark_complete, icon="✅",
                      parent_bg=CARD_COLOR).pack(pady=5)
        RoundedButton(c, "Delete Task", self.show_delete_task, icon="🗑",
                      parent_bg=CARD_COLOR).pack(pady=5)
        RoundedButton(c, "Back", self.show_dashboard, icon="←",
                      variant="secondary", parent_bg=CARD_COLOR).pack(pady=5)

    # ---------- ADD TASK ----------
    def show_add_task(self):
        self.clear_body()
        c = self.new_card()
        self.card_title(c, "Add Task")

        task_field = EntryField(c, "STUDY TASK"); task_field.pack(pady=6)

        def do_add():
            task_text = task_field.get()
            ok, msg = add_task(self.current_user[0], task_text)
            if ok:
                messagebox.showinfo("StudyPilot", msg)
                self.show_planner()
            else:
                messagebox.showerror("StudyPilot", msg)

        RoundedButton(c, "Add Task", do_add, icon="➕",
                      parent_bg=CARD_COLOR).pack(pady=(16, 8))
        RoundedButton(c, "Back", self.show_planner, icon="←",
                      variant="secondary", parent_bg=CARD_COLOR).pack(pady=6)

    # ---------- VIEW TASKS ----------
    def show_view_tasks(self):
        self.clear_body()
        c = self.new_card()
        self.card_title(c, "Your Tasks")

        tasks = get_tasks_for_user(self.current_user[0])

        if not tasks:
            tk.Label(c, text="No Tasks Found!", bg=CARD_COLOR,
                      fg=TEXT_MUTED, font=FONT_LABEL).pack(pady=20)
        else:
            for i, task in enumerate(tasks, start=1):
                status_color = SUCCESS_COLOR if task[2] == "Completed" else ERROR_COLOR
                row = tk.Frame(c, bg=ENTRY_BG)
                row.pack(fill="x", pady=5)
                tk.Label(row, text=f"{i}. {task[1]}", bg=ENTRY_BG,
                          fg=TEXT_LIGHT, font=FONT_LABEL, anchor="w"
                          ).pack(side="left", padx=12, pady=10)
                tk.Label(row, text=task[2], bg=ENTRY_BG,
                          fg=status_color, font=("Segoe UI", 10, "bold")
                          ).pack(side="right", padx=12)

        RoundedButton(c, "Back", self.show_planner, icon="←",
                      variant="secondary", parent_bg=CARD_COLOR).pack(pady=16)

    # ---------- MARK TASK COMPLETED ----------
    def show_mark_complete(self):
        self.clear_body()
        c = self.new_card()
        self.card_title(c, "Mark Task Completed")

        tasks = get_tasks_for_user(self.current_user[0])

        if not tasks:
            tk.Label(c, text="No Tasks Found!", bg=CARD_COLOR,
                      fg=TEXT_MUTED, font=FONT_LABEL).pack(pady=20)
        else:
            for i, task in enumerate(tasks):
                label = f"{task[1]}  ({task[2]})"

                def make_handler(idx=i):
                    def handler():
                        mark_task_complete_by_index(self.current_user[0], idx)
                        self.show_mark_complete()
                    return handler

                RoundedButton(c, label, make_handler(), icon="✅",
                              parent_bg=CARD_COLOR).pack(pady=5)

        RoundedButton(c, "Back", self.show_planner, icon="←",
                      variant="secondary", parent_bg=CARD_COLOR).pack(pady=16)

    # ---------- DELETE TASK ----------
    def show_delete_task(self):
        self.clear_body()
        c = self.new_card()
        self.card_title(c, "Delete Task")

        tasks = get_tasks_for_user(self.current_user[0])

        if not tasks:
            tk.Label(c, text="No Tasks Found!", bg=CARD_COLOR,
                      fg=TEXT_MUTED, font=FONT_LABEL).pack(pady=20)
        else:
            for i, task in enumerate(tasks):
                label = f"{task[1]}  ({task[2]})"

                def make_handler(idx=i):
                    def handler():
                        if messagebox.askyesno("StudyPilot", "Delete this task?"):
                            delete_task_by_index(self.current_user[0], idx)
                            self.show_delete_task()
                    return handler

                RoundedButton(c, label, make_handler(), icon="🗑",
                              parent_bg=CARD_COLOR).pack(pady=5)

        RoundedButton(c, "Back", self.show_planner, icon="←",
                      variant="secondary", parent_bg=CARD_COLOR).pack(pady=16)


if __name__ == "__main__":
    app = StudyPilotApp()
    app.mainloop()