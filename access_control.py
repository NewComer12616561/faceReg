import json

class Role:
    def __init__(self, name):
        self.name = name
        self.permissions = []

class Permission:
    def __init__(self, name):
        self.name = name

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role.name
        }

# Define roles
admin_role = Role("Admin")
teacher_role = Role("Teacher")

# Define permissions
capture_image_permission = Permission("capture_image")
detect_faces_permission = Permission("detect_faces")
assign_teacher_class_permission = Permission("assign_teacher_class")
add_student_permission = Permission("add_student")
check_attendance_permission = Permission("check_attendance")

# Assign permissions to roles
admin_role.permissions.extend([capture_image_permission, detect_faces_permission, assign_teacher_class_permission])
teacher_role.permissions.extend([add_student_permission, check_attendance_permission])

# In-memory user storage
users = []

def authenticate_user(username, password):
    for user in users:
        if user.username == username and user.password == password:
            return user
    return None

def create_teacher(username, password):
    new_teacher = User(username, password, teacher_role)
    users.append(new_teacher)
    print(f"Teacher {username} created successfully.")
    save_users_to_file()  # Save the updated user list to the file

def create_admin(username, password):
    new_admin = User(username, password, admin_role)
    users.append(new_admin)
    print(f"Admin {username} created successfully.")

def save_users_to_file(filename='users.json'):
    with open(filename, 'w') as f:
        json.dump([user.to_dict() for user in users], f)

def load_users_from_file(filename='users.json'):
    global users
    try:
        with open(filename, 'r') as f:
            user_data = json.load(f)
            for data in user_data:
                role = admin_role if data['role'] == 'Admin' else teacher_role
                user = User(data['username'], data['password'], role)
                users.append(user)
    except FileNotFoundError:
        print("User data file not found. Starting with an empty user list.")

def add_student_to_teacher_class(teacher_username, student_name):
    print(f"Student {student_name} added to {teacher_username}'s class.")        

def initialize_admin():
    # Pre-defined admin credentials
    admin_username = "admin"
    admin_password = "password"  # Change this to a more secure password in production

    # Check if the admin user already exists
    if not any(user.username == admin_username for user in users):
        create_admin(admin_username, admin_password)
