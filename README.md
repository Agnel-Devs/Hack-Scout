# 🚀 Hack Scout

### Discover. Track. Build. Win.

**Hack Scout** is a live, self-updating platform for discovering **hackathons, coding competitions, developer events, and technology opportunities across South India**.

Instead of searching through multiple event platforms, social-media posts, college communities, and individual websites, Hack Scout brings relevant opportunities into one simple interface.

Currently, the project focuses on events across:

* 🇮🇳 Kerala
* 🇮🇳 Tamil Nadu
* 🇮🇳 Karnataka
* 🇮🇳 Andhra Pradesh
* 🇮🇳 Telangana

🌐 **Live Website:** https://hack-scout-xi.vercel.app/

---

## 📌 Table of Contents

* [Overview](#-overview)
* [Problem Statement](#-problem-statement)
* [Our Solution](#-our-solution)
* [Key Features](#-key-features)
* [How It Works](#-how-it-works)
* [System Architecture](#-system-architecture)
* [Technology Stack](#-technology-stack)
* [Project Structure](#-project-structure)
* [Data Pipeline](#-data-pipeline)
* [Database](#-database)
* [Automated Updates](#-automated-updates)
* [Progressive Web App](#-progressive-web-app)
* [Getting Started](#-getting-started)
* [Supabase Configuration](#-supabase-configuration)
* [Running the Scraper](#-running-the-scraper)
* [Deployment](#-deployment)
* [Security](#-security)
* [Future Improvements](#-future-improvements)
* [Contributing](#-contributing)
* [License](#-license)

---

# 🎯 Overview

Hackathons are an excellent way for students and developers to:

* Build real-world projects
* Learn new technologies
* Meet other developers
* Build their portfolios
* Solve practical problems
* Win prizes and recognition
* Connect with companies and communities

However, discovering these opportunities can be difficult because event information is distributed across different platforms.

**Hack Scout solves this discovery problem by creating a centralized, continuously updated event hub.**

The platform automatically collects event information and presents it through a simple web interface.

---

# ❗ Problem Statement

Students and developers often miss hackathons and technology events because:

* Event information is scattered across multiple websites.
* Many opportunities are promoted only through community channels.
* Events have different registration deadlines.
* Finding events based on location can be difficult.
* Manually checking platforms every day is time-consuming.
* New events appear continuously.

This creates a simple but important problem:

> **There are many opportunities, but discovering the right opportunity at the right time is difficult.**

Hack Scout aims to reduce this friction.

---

# 💡 Our Solution

Hack Scout acts as a centralized discovery platform for hackathons and technology events.

The system:

1. Collects event information.
2. Stores the information in a structured database.
3. Automatically refreshes the data.
4. Displays available events through a responsive interface.
5. Allows users to discover opportunities without manually checking multiple sources.

The project is designed around **automation rather than manual event entry**.

---

# ✨ Key Features

## 🔎 Hackathon Discovery

Users can browse available hackathons and technology events from a centralized interface.

The platform focuses on events relevant to developers and students across South India.

---

## 🌎 Regional Coverage

Hack Scout currently focuses on five South Indian states:

| State          | Coverage |
| -------------- | -------- |
| Kerala         | ✅        |
| Tamil Nadu     | ✅        |
| Karnataka      | ✅        |
| Andhra Pradesh | ✅        |
| Telangana      | ✅        |

The architecture can be extended to additional regions in the future.

---

## 🔄 Automatic Data Updates

Hack Scout includes an automated scraping pipeline.

The Python scraper retrieves event information and updates the Supabase database.

This means the website does not need to depend entirely on manually entered event data.

---

## ⏰ Daily Automation

The project uses **GitHub Actions** to execute the scraper automatically.

The workflow is configured to run daily, allowing the event database to stay updated without requiring manual execution.

---

## 📱 Progressive Web App

Hack Scout includes Progressive Web App functionality.

The project contains:

* `manifest.json`
* `sw.js`
* Application icons

This allows the website to behave more like an installable application on supported devices.

Users can potentially add Hack Scout to their phone's home screen for faster access.

---

## ⚡ Lightweight Frontend

The frontend is intentionally simple.

The primary interface is implemented using:

* HTML
* CSS
* JavaScript

There is no frontend build process required.

The `index.html` application can be deployed directly as a static website.

---

# ⚙️ How It Works

The overall workflow is:

```text
                ┌──────────────────┐
                │   Event Sources  │
                │                  │
                │   Hackathons /   │
                │   Tech Events     │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Python Scraper   │
                │                  │
                │ scrape_devfolio  │
                │   _to_db.py      │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │    Supabase      │
                │                  │
                │   Events Table   │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │  Hack Scout      │
                │    Frontend      │
                │                  │
                │    index.html    │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │      Users       │
                │                  │
                │ Discover Events  │
                └──────────────────┘
```

---

# 🏗️ System Architecture

Hack Scout consists of four major components.

### 1. Frontend

The frontend provides the user-facing interface.

```text
index.html
```

It is a static application and can be deployed directly without a traditional frontend build pipeline.

---

### 2. Scraping Layer

The scraper is implemented in Python:

```text
scrape_devfolio_to_db.py
```

Its responsibility is to collect event information and write structured records into Supabase.

---

### 3. Database

Supabase acts as the project's backend data layer.

Event information is stored in an:

```text
events
```

table.

This allows the frontend to retrieve structured event data instead of relying directly on scraped pages.

---

### 4. Automation

GitHub Actions handles scheduled execution of the scraper.

```text
.github/
└── workflows/
    └── scrape.yml
```

The workflow runs automatically according to its configured schedule.

---

# 🧰 Technology Stack

| Layer        | Technology                        |
| ------------ | --------------------------------- |
| Frontend     | HTML, CSS, JavaScript             |
| Database     | Supabase                          |
| Scraper      | Python                            |
| Automation   | GitHub Actions                    |
| PWA          | Web App Manifest + Service Worker |
| Hosting      | Vercel                            |
| Event Source | Devfolio                          |

---

# 📁 Project Structure

```text
Hack-Scout/
│
├── .github/
│   └── workflows/
│       └── scrape.yml
│
├── icons/
│   └── PWA application icons
│
├── index.html
│
├── manifest.json
│
├── sw.js
│
├── scrape_devfolio_to_db.py
│
└── README.md
```

### `index.html`

The main frontend application.

It contains the user-facing interface for discovering events.

---

### `scrape_devfolio_to_db.py`

Python-based data collection script.

Its primary responsibility is to collect event information and store it in Supabase.

---

### `.github/workflows/scrape.yml`

GitHub Actions workflow responsible for automated execution of the scraper.

---

### `manifest.json`

Defines the Progressive Web App metadata such as application identity and installation behavior.

---

### `sw.js`

Service worker used to support PWA-related functionality and caching behavior.

---

### `icons/`

Contains application icons used by the PWA.

---

# 🔄 Data Pipeline

Hack Scout uses an automated data pipeline.

```text
Devfolio
   │
   ▼
Python Scraper
   │
   ├── Extract event information
   │
   ├── Process/structure data
   │
   ▼
Supabase
   │
   ▼
Events Database
   │
   ▼
Hack Scout Frontend
   │
   ▼
Users
```

The key advantage of this architecture is that **data collection and presentation are separated**.

The frontend doesn't need to scrape event websites directly.

Instead:

> Scraper → Database → Frontend

This makes the system easier to maintain and extend.

---

# 🗄️ Database

Hack Scout uses **Supabase** as its database layer.

The main database entity is:

```text
events
```

The exact schema should be configured according to the application's current frontend queries and scraper output.

Typical event information can include concepts such as:

* Event name
* Event URL
* Organizer
* Location
* Event date
* Registration deadline
* Event type
* Description
* Eligibility
* Registration information

The database structure can be expanded as the platform grows.

---

# 🤖 Automated Updates

One of Hack Scout's main architectural features is automated data refresh.

GitHub Actions periodically executes:

```text
scrape_devfolio_to_db.py
```

The workflow can be represented as:

```text
Scheduled GitHub Action
        ↓
Start Python Environment
        ↓
Run Scraper
        ↓
Collect Event Data
        ↓
Connect to Supabase
        ↓
Insert / Update Events
        ↓
Database Updated
```

This removes the need for the project maintainer to manually run the scraper every day.

---

# 📱 Progressive Web App

Hack Scout is designed with PWA support.

The project includes:

```text
manifest.json
sw.js
icons/
```

### Benefits

A PWA approach can provide:

* Installability
* Home-screen access
* Faster repeat visits
* Application-like experience
* Offline/caching capabilities where implemented

This is particularly useful because the platform is intended for students who may frequently check upcoming events from their phones.

---

# 🚀 Getting Started

## Prerequisites

Before running the project locally, make sure you have:

* Git
* Python 3.x
* A Supabase account
* A Supabase project

For deployment, you can also use:

* Vercel
* GitHub

---

## 1. Clone the Repository

```bash
git clone https://github.com/Agnel-Devs/Hack-Scout.git
```

Move into the project:

```bash
cd Hack-Scout
```

---

# 🗄️ Supabase Setup

Create a new project in Supabase.

Create the required:

```text
events
```

table.

The table schema must match the fields expected by:

```text
scrape_devfolio_to_db.py
```

and the frontend.

---

# 🔐 Environment Variables

The scraper requires Supabase credentials.

Configure the following values as environment variables/secrets:

```text
SUPABASE_URL
SUPABASE_SECRET_KEY
```

### GitHub Actions

Add these values to the repository's GitHub Actions secrets.

```text
Repository
   ↓
Settings
   ↓
Secrets and variables
   ↓
Actions
   ↓
New repository secret
```

Add:

```text
SUPABASE_URL
SUPABASE_SECRET_KEY
```

> Never commit private database credentials directly into the repository.

---

# 🐍 Running the Scraper Locally

Install the required Python dependencies according to the current project configuration.

Then execute:

```bash
python scrape_devfolio_to_db.py
```

The script should collect the configured event information and update the Supabase database.

---

# 🌐 Running the Frontend

Hack Scout uses a static frontend.

You can open:

```text
index.html
```

directly in a browser for basic local testing.

For development, you can also serve the directory using a simple local HTTP server.

For example:

```bash
python -m http.server 8000
```

Then visit:

```text
http://localhost:8000
```

---

# ☁️ Deployment

## Vercel

Because the frontend is static, Hack Scout can be deployed easily using Vercel.

Basic deployment flow:

```text
GitHub Repository
       ↓
      Vercel
       ↓
Static Deployment
       ↓
Hack Scout Website
```

No traditional frontend build command is required for the current architecture.

---

# 🔁 Continuous Updates

After deployment, GitHub Actions can continue running the scraper independently.

Therefore:

```text
Frontend Deployment
        +
Supabase Database
        +
GitHub Actions
        ↓
Continuously Updated Hackathon Platform
```

The frontend and data collection pipeline remain loosely coupled.

---

# 🔒 Security

Security is important because the application interacts with a hosted database.

### Never commit secrets

Do not place credentials such as:

```text
SUPABASE_SECRET_KEY
```

inside:

* `index.html`
* Python source code
* GitHub commits
* Public documentation

Use environment variables or GitHub Actions secrets instead.

---

## Database Security

Supabase access policies should be configured carefully so that public users can only perform the operations required by the frontend.

Administrative credentials should remain restricted to trusted backend/automation environments.

---

# 📈 Future Improvements

Hack Scout can be expanded considerably.

## 🔍 Advanced Search

Add filtering by:

* State
* City
* Online/offline
* Hackathon type
* Technology
* Registration status
* Event date

---

## ⭐ Bookmark Events

Allow users to save interesting hackathons.

```text
Event
  ↓
Save
  ↓
My Hackathons
```

---

## 🔔 Deadline Notifications

Notify users when:

* Registration is closing soon
* A new hackathon is added
* An event starts soon

---

## 🎯 Personalized Recommendations

A future recommendation system could use user preferences such as:

```text
Interests
+
Skills
+
Location
+
Event Type
        ↓
Recommended Hackathons
```

---

## 📅 Calendar Integration

Allow users to add events directly to:

* Google Calendar
* Apple Calendar
* Outlook Calendar

---

## 🏆 Competition Tracking

A dedicated dashboard could allow users to track:

```text
Upcoming
   ↓
Registered
   ↓
Participating
   ↓
Completed
```

---

## 🤖 AI-Powered Event Discovery

A future AI layer could help users discover events based on natural-language queries.

For example:

> "Find beginner-friendly AI hackathons near Kerala."

The system could then combine:

* Event data
* User preferences
* Location
* Skills
* Eligibility

to produce relevant results.

---

## 🌍 Expand Beyond South India

The current focus is South India.

Future versions could expand to:

```text
South India
     ↓
India
     ↓
Asia
     ↓
Global
```

---

# 🧪 Testing

Before deployment, verify:

### Frontend

* [ ] Website loads correctly
* [ ] Events are displayed
* [ ] Links work
* [ ] Responsive layout works
* [ ] Mobile experience works

### Database

* [ ] Supabase project is active
* [ ] `events` table exists
* [ ] Required columns are present
* [ ] Frontend can retrieve event data

### Scraper

* [ ] Python script executes successfully
* [ ] Event data is collected
* [ ] Database updates correctly
* [ ] Duplicate events are handled appropriately

### Automation

* [ ] GitHub Actions workflow is enabled
* [ ] Required secrets are configured
* [ ] Scheduled workflow executes successfully

### PWA

* [ ] Manifest loads correctly
* [ ] Icons are available
* [ ] Service worker registers correctly

---

# 🤝 Contributing

Contributions are welcome.

### 1. Fork the repository

```bash
git fork
```

or fork the repository through GitHub.

### 2. Clone your fork

```bash
git clone <your-fork-url>
```

### 3. Create a feature branch

```bash
git checkout -b feature/your-feature
```

### 4. Make your changes

Implement and test your changes locally.

### 5. Commit

```bash
git add .
git commit -m "Add: your feature"
```

### 6. Push

```bash
git push origin feature/your-feature
```

### 7. Open a Pull Request

Describe:

* What changed
* Why it was changed
* How it was tested

---

# 🛣️ Roadmap

| Feature                    | Status |
| -------------------------- | ------ |
| Hackathon discovery        | ✅      |
| South India event coverage | ✅      |
| Supabase database          | ✅      |
| Automated scraping         | ✅      |
| GitHub Actions automation  | ✅      |
| Static web application     | ✅      |
| PWA support                | ✅      |
| Advanced filters           | 🔜     |
| Event bookmarking          | 🔜     |
| Notifications              | 🔜     |
| Calendar integration       | 🔜     |
| AI recommendations         | 🔜     |
| User accounts              | 🔜     |
| Global event coverage      | 🔜     |

---

# 🌟 Why Hack Scout?

Hack Scout is built around a simple idea:

> **Students shouldn't have to hunt for opportunities. Opportunities should be easy to discover.**

By combining:

**Automated data collection + centralized storage + a lightweight frontend + scheduled updates**

Hack Scout creates a foundation for a scalable hackathon discovery platform.

---

# 📊 Project Architecture at a Glance

```text
                    ┌─────────────────────┐
                    │   Event Platforms   │
                    │     / Sources       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Python Scraper    │
                    │                     │
                    │ scrape_devfolio_    │
                    │      to_db.py       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Supabase       │
                    │                     │
                    │    Events Table     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Hack Scout       │
                    │      Frontend       │
                    │                     │
                    │     index.html      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Users         │
                    │                     │
                    │ Discover & Explore  │
                    └─────────────────────┘


             ┌──────────────────────────────┐
             │       GitHub Actions        │
             │                              │
             │   Scheduled Daily Scraper   │
             └──────────────┬───────────────┘
                            │
                            └──────► Scraper
```

---

# 🔗 Links

**GitHub Repository:**
https://github.com/Agnel-Devs/Hack-Scout

**Live Application:**
https://hack-scout-xi.vercel.app/

---

# 👨‍💻 Project

Built by **Agnel-Devs** with the goal of making hackathons and technology opportunities easier to discover for students and developers.

⭐ If you find the project useful, consider starring the repository and contributing improvements.

---

## 📄 License

Add the project's chosen open-source license here.

If no license has been selected yet, choose an appropriate license before presenting the repository as an open-source project.
