# Capstone Project Development Plan

This repository contains the development roadmap and implementation plan for a Capstone Project focusing on **user authentication, role-based access control, and feature-rich user/admin functionalities** using **FastAPI, SQLAlchemy, or MySQL - and JWT authentication**.  

---

## Table of Contents
1. [Project Overview](#project-overview)  
2. [Tech Stack](#tech-stack)  
3. [Development Plan](#development-plan)  
    - [Day 1: Database Setup](#day-1-database-setup)  
    - [Day 2: User Registration (API + DB Setup)](#day-2-user-registration-api--db-setup)  
    - [Day 3: Login with SSO + JWT Authentication](#day-3-login-with-sso--jwt-authentication)  
    - [Day 4: Role-Based Access Control (RBAC)](#day-4-role-based-access-control-rbac)  
    - [Day 5: Logging & Monitoring](#day-5-logging--monitoring)  
    - [Days 6–8: Role-Specific Feature Development](#days-6-8-role-specific-feature-development)  
    - [Days 9–10: Advanced Search Implementation](#days-9-10-advanced-search-implementation)  
4. [Project Deliverables](#project-deliverables)  
5. [References & Resources](#references--resources)  

---

## Project Overview
The goal of this capstone project is to build a **robust web application** with:  
- Secure user authentication (normal users and admins)  
- Role-based access control (RBAC)  
- Feature-rich functionalities like **movie management, reviews, ratings, watchlist, and admin moderation**  
- Structured logging, monitoring, and advanced search  

This project emphasizes **best practices, clean code standards, API documentation, and testing**.  

---

## Tech Stack
- **Backend:** FastAPI, SQLAlchemy  
- **Database:** PostgreSQL/MySQL (any relational DB)  
- **Authentication:** JWT (Access + Refresh Tokens), Optional SSO (OAuth2)  
- **Password Security:** bcrypt or passlib  
- **API Testing:** Postman  
- **Logging:** Python `logging` module / Loguru  
- **Documentation:** Swagger/API OPENAPI  

---

## Development Plan

### Day 1: Database Setup
**Tasks:**  
- Configure and initialize the database  
- Insert sample data for testing  
- Practice SQL queries to understand data structure  

**GitHub Setup:**  
- Configure Git credentials  
- Initialize repository and set up version control  

**Weekend Assignment:**  
- FastAPI CRUD tutorial with SQLAlchemy  
- API testing with Postman  
- Review Python PEP guidelines for clean code  

---

### Day 2 – User Registration (API + Database Setup)
**Goal:** Implement user registration for both **normal users** and **admins**.  

**Tasks:**  
- **Database:**  
  - Create `users` table/model  
  - Enum for roles: `USER`, `ADMIN`  
  - Unique index on `email`  
- **Password Handling:** Hash passwords using bcrypt/passlib  
- **API Endpoint:** `POST /auth/register`  
  - Validate input (email, password strength, role)  
  - Hash password before saving  
  - Return success or error response  
- **Testing:**  
  - Register as normal user and admin  
  - Handle duplicate emails and invalid data  

**Deliverables:**  
- `/auth/register` endpoint functional  
- Secure password storage  
- Postman test cases  

---

### Day 3 – Login with SSO + JWT Authentication
**Goal:** Enable JWT login and SSO support  

**Tasks:**  
- **Login API:** `POST /auth/login`  
  - Verify credentials, generate JWT tokens (Access + Refresh)  
  - Return user details and tokens  
- **SSO Integration (stub):** OAuth2 login (e.g., Google) placeholder  
- **Logout API:** `POST /auth/logout` (invalidate refresh token/blacklist)  
- **Middleware:** JWT verification, attach user to request  

**Deliverables:**  
- `/auth/login` & `/auth/logout` endpoints working  
- JWT access/refresh flow functional  
- Sample SSO stub added  

---

### Day 4 – Role-Based Access Control (RBAC)
**Goal:** Secure routes based on roles  

**Tasks:**  
- **Authorization Middleware:**  
  - Check JWT validity  
  - Verify role from token payload  
  - Restrict endpoints  
- **Decorators/Utilities:** `@login_required`, `@admin_required`  
- **Testing:**  
  - Admin-only route access  
- **Documentation:** Swagger/OpenAPI for auth endpoints  

**Deliverables:**  
- RBAC functional  
- Protected endpoints tested  
- Auth middleware integrated globally  
- Updated Swagger docs  

---

### Day 5 – Logging & Monitoring
**Goal:** Add structured logging for debugging and auditing  

**Tasks:**  
- **Logging Setup:**  
  - Configure Python’s logging module (or Loguru)  
  - Define log format: timestamp, level, module, message  
- **Log Events:**  
  - Registration (user created)  
  - Login (success/failure)  
  - Logout (token invalidation)  
  - Role-based access violation  
- **Log Levels:** Use INFO, WARNING, ERROR, DEBUG  
- **File & Console Handlers:**  
  - Rotating file handler  
  - Store logs in `/logs/auth.log`  

**Deliverables:**  
- Centralized logging system  
- Auth flow logs recorded  
- File rotation configured  
- Easy traceability for debugging  

---

### Days 6–8 – Role-Specific Feature Development
**Modules:**  
- **Module A (Admin):** Movie Management System  
- **Module B (User):** Reviews and Ratings functionality  
- **Module C (User):** Watchlist management  
- **Module D (Admin):** Admin Panel and content moderation tools  

---

### Days 9–10 – Advanced Search Implementation
**Tasks:**  
- Build a comprehensive search system for assigned features  
- Implement pagination for large result sets  
- Add filtering and sorting capabilities  

---

## Project Deliverables
- Fully functional user authentication system  
- Role-based access control  
- Admin and User features implemented  
- Structured logging and monitoring in place  
- Advanced search with pagination, filtering, and sorting  
- Complete API documentation with Swagger/OpenAPI  
- Postman test collection  

---

## References & Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)  
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)  
- [Postman API Testing](https://www.postman.com/)  
- [JWT Authentication](https://jwt.io/)  
- [Python Logging](https://docs.python.org/3/library/logging.html)  
