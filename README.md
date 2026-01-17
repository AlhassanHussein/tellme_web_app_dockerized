# TellMe – Anonymous Temporary Messages Web App

TellMe is a full-stack web application that allows users to receive **anonymous messages** through **temporary links**.  
Each generated session creates a **public link** to receive messages and a **private link** to view them.  
All data is automatically deleted after a selected time period (6, 12, or 24 hours).

This project is built as a **monolithic application**   and is fully containerized for easy deployment and future scaling.

---

## ✨ Features

- Generate **temporary anonymous messaging links**
- Public link to receive anonymous messages
- Private link to view received messages
- Message sender identity is completely hidden
- Automatic expiration (6 / 12 / 24 hours)
- Countdown timer before expiration
- Auto-delete all data after expiration
- Multi-language support:
  - English
  - Arabic (RTL)
  - Spanish
- Clean, modern, responsive UI
- No authentication required

---

## 🖼️ Screenshots

### public – Generate Links
![public Page](screenshots/public.png)

### links – Generate Links
![links Page](screenshots/links.png)

### send messags – Generate Links
![send messags Page](screenshots/send_message.png)

###  sent – Generate Links
![sent Page](screenshots/sent.png)

### recived messags – Generate Links
![recived messags Page](screenshots/recived_messags.png)




> 📌 Screenshots are located in the `screenshots/` folder.

---

## 📦 Installation


git clone https://github.com/AlhassanHussein/tellme_web_app_dockerized.git

cd tellme_web_app_dockerized/

docker build -t tellme-app .
docker run -p 8000:8000 tellme-app


## 🛠 Tech Stack

- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **Server:** Uvicorn
- **Architecture:** Dockerized (Cloud-ready)

---

## 📁 Project Structure


## Project Structure

```text
.
├── backend/                # FastAPI Server Logic
│   ├── main.py             # Application entry point
│   ├── database.py         # Database connection configuration
│   ├── models.py           # SQLAlchemy/SQLModel data definitions
│   ├── scheduler.py        # Background tasks and periodic jobs
│   └── routers/            
│       └── api.py          # API route definitions
├── frontend/               # Web Interface
│   ├── index.html          # Main landing page
│   ├── public.html         # Publicly accessible view
│   ├── private.html        # Authenticated user view
│   ├── app.js              # Frontend logic and API integration
│   ├── i18n.js             # Internationalization/Translations
│   └── style.css           # Global styles
├── database.db             # SQLite database file
├── requirements.txt        # Python dependencies
├── README.md         
├── Dockerfile              # Docker configuration
└── .dockerignore           # Docker ignore file

