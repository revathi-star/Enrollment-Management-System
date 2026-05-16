# 🎓 Student Course Enrollment Management API

This project is a simple yet practical **Student Course Enrollment Management System** built using Flask, Flask-RESTful, and SQLAlchemy.
It provides a RESTful backend service that allows users to manage students, courses, and enrollments efficiently through API endpoints.

The application simulates how colleges, universities, or online learning platforms maintain student records and handle course registrations.

---

# 🚀 What This Application Does

The system mainly focuses on three core entities:

* **Students**
* **Courses**
* **Enrollments**

Using REST APIs, the app allows users to:

✅ Add new students
✅ Create and manage courses
✅ Enroll students into courses
✅ Update student/course details
✅ Delete records when needed
✅ Retrieve enrollment information dynamically

The backend uses a local SQLite database to store all information persistently.

---

# 🧩 Core Features

## 👨‍🎓 Student Management

The application allows complete CRUD operations for students:

* Create a student record
* Retrieve student details
* Update student information
* Delete student records

Each student contains:

* Student ID
* Roll Number
* First Name
* Last Name

The app also ensures:

* Roll numbers are unique
* Mandatory fields are validated properly

---

## 📚 Course Management

The system also manages courses through dedicated APIs.

Each course contains:

* Course ID
* Course Name
* Course Code
* Course Description

Features include:

* Adding new courses
* Updating course details
* Preventing duplicate course codes
* Deleting courses safely

---

## 🔗 Enrollment System

A many-to-many relationship exists between students and courses.

This is handled through the `Enrollment` table, which acts as a bridge between:

* `Student`
* `Course`

Using the enrollment APIs, users can:

* Enroll a student into a course
* View all courses taken by a student
* Remove enrollments

This models how real educational platforms track registrations.

---

# 🛠️ Technologies Used

| Technology    | Purpose                     |
| ------------- | --------------------------- |
| Python        | Core programming language   |
| Flask         | Web framework               |
| Flask-RESTful | REST API development        |
| SQLAlchemy    | ORM and database management |
| SQLite        | Lightweight database        |

---

# ⚙️ API Endpoints Overview

## Student APIs

| Method | Endpoint                    | Description                |
| ------ | --------------------------- | -------------------------- |
| GET    | `/api/student/<student_id>` | Fetch student details      |
| POST   | `/api/student`              | Create a new student       |
| PUT    | `/api/student/<student_id>` | Update student information |
| DELETE | `/api/student/<student_id>` | Delete a student           |

---

## Course APIs

| Method | Endpoint                  | Description               |
| ------ | ------------------------- | ------------------------- |
| GET    | `/api/course/<course_id>` | Fetch course details      |
| POST   | `/api/course`             | Create a new course       |
| PUT    | `/api/course/<course_id>` | Update course information |
| DELETE | `/api/course/<course_id>` | Delete a course           |

---

## Enrollment APIs

| Method | Endpoint                                       | Description                |
| ------ | ---------------------------------------------- | -------------------------- |
| GET    | `/api/student/<student_id>/course`             | View student enrollments   |
| POST   | `/api/student/<student_id>/course`             | Enroll student into course |
| DELETE | `/api/student/<student_id>/course/<course_id>` | Remove enrollment          |

---

# 🧠 Error Handling & Validation

The project includes custom exception handling for better API responses.

Examples include:

* Missing required fields
* Duplicate entries
* Invalid student or course IDs
* Enrollment validation errors

Custom error codes like:

* `COURSE001`
* `STUDENT001`
* `ENROLLMENT001`

make debugging and API integration easier.

---

# 💡 Why This Project Is Useful

This project is a great beginner-to-intermediate backend development project because it demonstrates:

* REST API design
* Database relationships
* CRUD operations
* Input validation
* Exception handling
* ORM usage
* Backend architecture principles

It closely resembles how real-world academic management systems work internally.

---

# 🎯 Final Thoughts

Overall, this application is a clean and structured backend system for managing academic data. It showcases how modern web APIs can organize relationships between students and courses while maintaining data integrity and scalability.

It is an excellent project for learning backend development concepts and serves as a strong foundation for building larger systems such as:

* Learning Management Systems (LMS)
* College ERP platforms
* Online course portals
* Student administration dashboards
