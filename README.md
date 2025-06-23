# new-nest-dev-hive

## 🚀 Project Overview

**new-nest-dev-hive** is a full-stack, production-grade collaboration and project management platform, rebuilt from the ground up to demonstrate mastery of modern backend and frontend engineering.  
Unlike typical SaaS starter kits, this project is designed to give you full control over every layer of the stack, with no reliance on high-level backend-as-a-service platforms.  
The goal is to create a robust, scalable, and extensible system suitable for advanced portfolios, real-world deployments, and as a learning resource for deep full-stack architecture.

**Key features:**
- User authentication (JWT, OAuth2)
- Real-time presence and messaging (WebSockets, Redis)
- Project, friend, and messaging management (RESTful APIs)
- Full-text search and advanced filtering (PostgreSQL)
- Modern, responsive UI (React, Tailwind)
- Professional codebase structure and best practices

---

## 🏗️ Tech Stack (with Rationale & Details)

### **Frontend**
- **React (JavaScript, no TypeScript):**  
  Industry-standard for building interactive UIs. Chosen for flexibility, ecosystem, and familiarity.
- **Vite:**  
  Lightning-fast dev server and build tool. Modern alternative to Create React App.
- **Tailwind CSS:**  
  Utility-first CSS for rapid, consistent styling.
- **React Router:**  
  Declarative routing for single-page apps.
- **State Management:**  
  React Context and hooks for local/global state.
- **API Layer:**  
  Custom JS modules for interacting with backend REST/WebSocket endpoints.

### **Backend**
- **FastAPI (Python):**  
  High-performance, async-ready web framework for building APIs. Used for all HTTP endpoints and WebSocket support.
- **Uvicorn:**  
  ASGI server for running FastAPI apps, supports hot-reload for development.
- **SQLAlchemy (Core/ORM):**  
  Python SQL toolkit for defining DB models and queries. Used for all database access and schema definition.
- **Alembic:**  
  Database migrations and schema versioning. Ensures DB structure matches your models over time.
- **Pydantic & pydantic-settings:**  
  Data validation and settings management using Python type hints. Used for request/response schemas and loading environment variables.
- **python-jose:**  
  Library for creating and verifying JWT tokens (stateless authentication).
- **passlib[bcrypt]:**  
  Secure password hashing and verification.
- **psycopg2-binary:**  
  PostgreSQL driver for Python, used by SQLAlchemy.
- **redis:**  
  In-memory data store for real-time features (presence, pub/sub, caching).
- **email-validator:**  
  Validates email addresses for correctness (used by Pydantic's EmailStr).
- **Testing:**  
  Pytest for backend, React Testing Library for frontend.
- **DevOps:**  
  Docker & Docker Compose for local development and deployment.

### **Why This Stack?**
- **No vendor lock-in:** All open-source, self-hostable components.
- **Maximum control:** Every layer is explicit and customizable.
- **Scalability:** Designed for real-world, high-traffic use.
- **Portfolio-ready:** Demonstrates advanced backend and frontend skills.

---

## 📁 Folder Structure (with Detailed Explanations)

### **Typical Professional Project Structure**


```
/new-nest-dev-hive/
├── backend/
│ ├── app/
│ │ ├── api/
│ │ │ ├── v1/
│ │ │ │ ├── init.py
│ │ │ │ └── users.py
│ │ │ └── ws/
│ │ │ ├── init.py
│ │ │ └── presence.py
│ │ ├── core/
│ │ │ ├── init.py
│ │ │ ├── config.py
│ │ │ └── security.py
│ │ ├── db/
│ │ │ ├── init.py
│ │ │ ├── session.py
│ │ │ └── models.py
│ │ ├── schemas/
│ │ │ ├── init.py
│ │ │ └── user.py
│ │ ├── services/
│ │ │ ├── init.py
│ │ │ └── user_service.py
│ │ ├── websocket/
│ │ │ ├── init.py
│ │ │ └── connection_manager.py
│ │ └── main.py
│ ├── alembic/
│ │ └── versions/
│ ├── alembic.ini
│ ├── requirements.txt
│ └── README.md
├── frontend/
│ ├── public/
│ ├── src/
│ │ ├── components/
│ │ ├── hooks/
│ │ ├── pages/
│ │ ├── api/
│ │ ├── App.js
│ │ ├── index.js
│ │ └── ...
│ ├── tailwind.config.js
│ ├── vite.config.js
│ ├── package.json
│ └── README.md
├── docker-compose.yml
├── .env.example
├── NOTES.md
└── README.md
```


#### **What does each folder/file do?**

##### **Backend**
- **app/api/v1/**: REST API endpoints grouped by domain (users, projects, messages, etc).
- **app/api/ws/**: WebSocket endpoints for real-time features like chat and user presence.
- **app/core/**: App-wide configuration, security, JWT/OAuth2 logic, and environment settings.
- **app/db/**: SQLAlchemy models, database session management, and reusable CRUD utilities.
- **app/schemas/**: Pydantic models that define the structure and validation rules for requests and responses.
- **app/services/**: Business logic layer (the “brains” of your app); contains reusable service classes like authentication, messaging, etc.
- **app/websocket/**: WebSocket connection management including Redis pub/sub integration for real-time messaging.
- **app/main.py**: The entry point that creates the FastAPI app, registers routers, and sets up middleware.
- **alembic/**: Directory for managing database migrations via Alembic.
- **alembic/versions/**: Individual timestamped migration scripts auto-generated by Alembic.
- **alembic.ini**: Alembic configuration file specifying DB URL, migration script paths, etc.
- **requirements.txt**: Lists all Python dependencies required to run the backend.
- **README.md**: Documentation specific to the backend setup and usage.

##### **Frontend**
- **frontend/public/**: Static assets like `favicon.ico`, `robots.txt`, and other public-facing resources.
- **frontend/src/components/**: Reusable UI components such as buttons, forms, cards, modals, etc.
- **frontend/src/hooks/**: Custom React hooks to manage API calls, application state, and WebSocket events.
- **frontend/src/pages/**: Top-level route components representing pages like Home, Login, and Dashboard.
- **frontend/src/api/**: JavaScript modules that handle HTTP and WebSocket communication with the backend.
- **frontend/src/App.js**: Main React application shell that contains routing and global providers.
- **frontend/src/index.js**: React app entry point; renders `<App />` into the DOM.
- **frontend/tailwind.config.js**: Tailwind CSS configuration file defining custom styles and utilities.
- **frontend/vite.config.js**: Vite configuration for frontend build and dev server.
- **frontend/package.json**: Declares frontend dependencies, scripts, and metadata.
- **frontend/README.md**: Documentation specific to frontend architecture, setup, and usage.

##### **Project Root**
- **docker-compose.yml**: Orchestrates multi-service dev environment (PostgreSQL, Redis, backend, frontend).
- **.env.example**: Template environment variable file to guide `.env` setup for development or deployment.
- **NOTES.md**: Personal engineering notes, architecture decisions, or learning logs.
- **README.md**: Project-wide documentation explaining the full-stack structure, setup, and usage.

---

## 🛠️ Getting Started

1. **Clone the repo:**
   ```sh
   git clone https://github.com/Fawz-Haaroon/new-nest-dev-hive.git
   cd new-nest-dev-hive
   ```
2. **Copy `.env.example` to `.env` and fill in secrets.**
3. **Start with Docker Compose:**
   ```sh
   docker-compose up --build
   ```
4. **Or run backend/frontend separately (see backend/frontend README.md).**

---

## 🤝 Contributing

- Fork, branch, and submit PRs.
- Follow code style and commit guidelines.
- See `CONTRIBUTING.md` for more.

---

## 🗺️ Roadmap

- [ ] Backend: Auth, Users, Projects, Messaging, Presence
- [ ] Frontend: Auth, Dashboard, Messaging UI
- [ ] DevOps: CI/CD, Docker, Deployment
- [ ] Testing: Unit, Integration, E2E

---

## 📄 License

NIL

---

## 👤 Contact & Credits

- Author: Fawz Haaroon
- For portfolio, hiring, or questions: [GitHub](https://github.com/Fawz-Haaroon)