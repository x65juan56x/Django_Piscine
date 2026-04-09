# 🏊‍♂️ Piscine Django - 42 Network

Welcome to my **Piscine Django**! This repository documents my progress throughout this intensive program, covering everything from the foundational concepts of the web to the creation of complex real-time applications using Django, WebSockets, and relational databases.

This repository culminates in a **Monolithic Portfolio Project** that unifies the final, most advanced modules of the piscine under a single robust architecture.

---

## 🌟 Main Project: Django Portfolio

In the [`django_practice/portfolio_django`](django_practice/portfolio_django/) folder, you will find the definitive project that integrates the three final applications of the piscine into a single ecosystem. 

To achieve this, I designed a **DRY (Don't Repeat Yourself)** architecture with the following features:
- **Single Source of Truth (Template Inheritance Pattern):** A global `base.html` that manages the navigation bar, layout, and Bootstrap 5 dependencies for all sub-applications.
- **Global AJAX Authentication:** A dynamic login/register system in the top navbar that works without reloading the page across any module, handling dynamic CSRF token rotation.
- **Multi-language Support:** Native integration of translations (Spanish/English) and internationalization (`.po`/`.mo`) applied throughout the entire portal.

### The 3 Integrated Applications:
1. 💡 **Tips (Module 06):** An application for publishing and voting on "Life Pro Tips". It uses session-based authentication, custom Middlewares, permission control, and Django Forms.
2. 📖 **Articles (Module 07):** A robust publishing platform. It makes extensive use of **Class-Based Views (CBV)**, complex routing, advanced ORM modeling (Many-to-Many relationships), and a system for marking articles as favorites.
3. 💬 **Chat (Module 08):** A real-time messaging application separated into different rooms. Implemented using **Asynchronous Django**, WebSockets, and **Django Channels**.

---

## 📚 The Path of the Piscine: Module Summary

The root folder contains the daily exercises that built the foundations of this learning journey:

* **`Module 00` - Web Fundamentals:** First steps with HTML5, CSS3, and JavaScript. DOM manipulation, responsive design, and basic audio/video events.
* **`Module 01` - Python Basics:** Data types, dictionaries, loops, script creation, and control structure management.
* **`Module 02` - Python OOP:** Object-Oriented Programming in Python. Class creation, inheritance, magic methods, and a basic engine to render HTML from pure Python.
* **`Module 03` - Scraping & First Servers:** HTTP requests, web scraping (navigating Wikipedia), geohashing, and an introduction to the Django framework (virtual environments and apps).
* **`Module 04` - Introduction to Django:** Creation of the first "apps", URL mapping, template configuration, and function-based views.
* **`Module 05` - Models & ORM:** Database connection (SQLite/PostgreSQL), Django migrations, and querying relational databases using Object-Relational Mapping (ORM).
* **`Module 06` - Sessions & Middlewares (Tips):** Deep dive into cookies, security (CSRF), model-based form validation, and user registration.
* **`Module 07` - Advanced Features (Articles):** Mastery of Class-Based Views (ListView, DetailView, CreateView), mixins (LoginRequiredMixin), permissions, and M2M relationships.
* **`Module 08` - Asynchronism & WebSockets (Chat):** Integration of ASGI over WSGI to provide Django with asynchronous networking capabilities, using Channels to achieve real-time interactivity (Chat Rooms).

---

## 🚀 Local Installation and Deployment

Follow these steps to run the Monolithic Project on your local machine:

### 1. Clone the repository and access the project
```bash
git clone <REPO_URL>
cd piscine_django/django_practice/portfolio_django
```

### 2. Create and activate a virtual environment
```bash
./my_script.sh
```

### 4. Compile Translations and Apply Migrations
```bash
python3 manage.py compilemessages
python3 manage.py makemigrations
python3 manage.py migrate
```

### 5. Start the Server (ASGI/WSGI)
```bash
python3 manage.py runserver
```
Done! The application will be available at `http://127.0.0.1:8000/`.

---

## 👨‍💻 Author
Developed and integrated by **Juan Mondón (jmondon on the 42 INTRA)**.