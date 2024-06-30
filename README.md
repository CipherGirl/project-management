# Project Management System

## Description

Users can create account, projects. Include other users as team members inside the projects created by them. Inside projects members can create tasks, assign to any team member, change status of the task.

## Features

- **Project Management:**
  - List, create, update, and delete projects.
  - Detailed project view showing tasks associated with each project.
- **Task Management:**
  - List, create, update, and delete tasks within projects.
- **User Authentication:**
  - User registration, login, and authentication.
- **Permissions:**
  - Custom handling for PermissionDenied with dedicated error pages.

# Technologies Used

- Django
- Python
- HTML/CSS
- Bootstrap

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd project-directory
   ```

2. **Setup Virtual Environment:**

   ```bash
   python -m venv env
   source env/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
    pip install -r requirements.txt
   ```

4. **Apply Migration:**
   ```bash
    python manage.py migrate
   ```

## Usage

1. **Run the Development Server:**

   ```bash
   python manage.py runserver
   ```

2. **Accessing Admin Panel:**

   ```bash
    python manage.py createsuperuser
   ```

# Views

- `ProjectList`: Lists all projects the user is involved in.
- `ProjectDetail`: Details of a specific project, including associated tasks.
- `ProjectCreate`: Form to create a new project.
- `ProjectUpdate`: Form to update an existing project.
- `ProjectDelete`: Confirmation and deletion of a project.
- `TaskCreate`: Form to create a new task within a project.
- `TaskUpdate`: Form to update an existing task.
- `TaskDelete`: Confirmation and deletion of a task.

# Custom Error Handling

### Custom handling for PermissionDenied:

    Custom view (custom_permission_denied_view) and error page (projects/403.html) for permission errors.
