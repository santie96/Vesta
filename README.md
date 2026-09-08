# Vesta

> **Modern full-stack fashion e-commerce platform built with React and FastAPI.**

Vesta è un progetto **full-stack e-commerce** dedicato al settore fashion, progettato per offrire un'esperienza di acquisto moderna, responsive e strutturata.

Il progetto è attualmente **in sviluppo** e nasce con l'obiettivo di realizzare una piattaforma completa per la gestione di prodotti, categorie, utenti, recensioni e flussi di acquisto.

L'applicazione utilizza un'architettura separata **Frontend / REST API / Backend / Database**, con React per il client, FastAPI per le API e PostgreSQL per la persistenza dei dati.

> 🚧 **Project Status: In Development**
>
> Alcune funzionalità sono ancora in fase di implementazione e la struttura del progetto è soggetta a evoluzione.

---

## ✨ Features

| Area                  | Stato | Funzionalità                                      |
| --------------------- | :---: | ------------------------------------------------- |
| 🏠 **Homepage**       |   🟢  | Interfaccia principale e navigazione del catalogo |
| 👕 **Prodotti**       |   🟢  | Gestione e visualizzazione dei prodotti           |
| 🏷️ **Categorie**     |   🟢  | Organizzazione dei prodotti per categoria         |
| 👤 **Autenticazione** |   🟡  | Registrazione, login e gestione utenti            |
| 🛒 **Carrello**       |   🟡  | Gestione dei prodotti selezionati                 |
| 💳 **Checkout**       |   🟡  | Flusso di acquisto                                |
| ⭐ **Recensioni**      |   🟡  | Gestione delle recensioni dei prodotti            |
| 📍 **Localizzazione** |   🟢  | Integrazione Google Maps                          |
| 📱 **Responsive UI**  |   🟢  | Interfaccia adattiva per diversi dispositivi      |
| 🔐 **Security**       |   🟢  | JWT, bcrypt e gestione delle autorizzazioni       |
| 🗄️ **Database**      |   🟢  | PostgreSQL con SQLAlchemy                         |
| 🔄 **Migrations**     |   🟢  | Alembic                                           |
| 🐳 **Docker**         |   🟢  | Containerizzazione backend e database             |
| 📦 **API REST**       |   🟢  | Backend FastAPI organizzato per dominio           |

> **Legenda:** 🟢 Implementato · 🟡 In sviluppo · ⚪ Pianificato

---

# 🛠️ Tech Stack

## Frontend

| Tecnologia                    | Utilizzo                        |
| ----------------------------- | ------------------------------- |
| **React 19**                  | Libreria principale per la UI   |
| **Vite**                      | Development server e build tool |
| **React Router 7**            | Routing dell'applicazione       |
| **Tailwind CSS 4**            | Styling e responsive design     |
| **React Icons**               | Iconografia                     |
| **@vis.gl/react-google-maps** | Integrazione Google Maps        |
| **ESLint**                    | Code quality e linting          |

Le dipendenze e gli script frontend sono definiti nel `package.json`.

---

## Backend

| Tecnologia            | Utilizzo                    |
| --------------------- | --------------------------- |
| **Python**            | Linguaggio backend          |
| **FastAPI**           | REST API framework          |
| **Uvicorn**           | ASGI server                 |
| **SQLAlchemy 2**      | ORM e gestione del database |
| **asyncpg**           | Driver PostgreSQL asincrono |
| **Alembic**           | Database migrations         |
| **Pydantic**          | Data validation             |
| **Pydantic Settings** | Gestione configurazione     |
| **python-jose**       | JWT                         |
| **bcrypt**            | Password hashing            |
| **SlowAPI**           | Rate limiting               |

Le principali dipendenze backend sono definite in `backend/requirements.txt`.

---

## Database

| Tecnologia     | Utilizzo                   |
| -------------- | -------------------------- |
| **PostgreSQL** | Database relazionale       |
| **SQLAlchemy** | ORM                        |
| **asyncpg**    | Connessione asincrona      |
| **Alembic**    | Versionamento dello schema |

---

## Development & DevOps

| Tecnologia         | Utilizzo                       |
| ------------------ | ------------------------------ |
| **Git**            | Version control                |
| **GitHub**         | Repository e collaborazione    |
| **Docker**         | Containerizzazione             |
| **Docker Compose** | Orchestrazione dei servizi     |
| **ESLint**         | Analisi statica frontend       |
| **PRD**            | Documentazione e progettazione |

---

# 🏗️ Architecture

Vesta segue un'architettura **client-server full stack**.

```text
┌──────────────────────────────────────┐
│               FRONTEND               │
│                                      │
│ React 19 + Vite                      │
│ React Router                         │
│ Tailwind CSS                         │
│ Components                           │
│ Pages / UI                           │
└──────────────────┬───────────────────┘
                   │
                   │ HTTP / REST API
                   ▼
┌──────────────────────────────────────┐
│               BACKEND                │
│                                      │
│ Python + FastAPI                     │
│                                      │
│ Routes / Endpoints                   │
│ Schemas                              │
│ Business Logic                       │
│ Authentication                       │
│ Database Layer                       │
└──────────────────┬───────────────────┘
                   │
                   │ SQLAlchemy
                   ▼
┌──────────────────────────────────────┐
│              PostgreSQL              │
│                                      │
│ Users                                │
│ Products                             │
│ Categories                           │
│ Reviews                              │
│ Orders / Cart                        │
└──────────────────────────────────────┘
```

Il backend è organizzato per **dominio funzionale**, con moduli dedicati a categorie, prodotti, recensioni, utenti, database e componenti core.

---

# 🔄 Application Flow

Il flusso generale previsto dall'applicazione è:

```text
User
 │
 ▼
React UI
 │
 ▼
React Router
 │
 ▼
Frontend API Request
 │
 │ HTTP
 ▼
FastAPI
 │
 ▼
Validation / Authentication
 │
 ▼
Business Logic
 │
 ▼
SQLAlchemy
 │
 ▼
PostgreSQL
 │
 ▼
API Response
 │
 ▼
React State / UI
```

Questo permette di mantenere separati:

* presentation layer;
* routing;
* API layer;
* business logic;
* persistence layer.

---

# 🔌 REST API

Il backend utilizza **FastAPI** per fornire API REST al frontend.

I domini principali presenti nella struttura backend sono:

| Modulo       | Responsabilità                        |
| ------------ | ------------------------------------- |
| `users`      | Utenti e autenticazione               |
| `products`   | Prodotti e relative informazioni      |
| `categories` | Categorie del catalogo                |
| `reviews`    | Recensioni                            |
| `database`   | Connessione e gestione database       |
| `core`       | Configurazione e componenti condivisi |

La struttura attuale del backend riflette questa separazione per dominio.

---

# 👕 Product Management

La gestione dei prodotti rappresenta uno dei domini principali dell'applicazione.

Un prodotto e-commerce può essere associato a informazioni quali:

| Informazione  | Utilizzo                              |
| ------------- | ------------------------------------- |
| Nome          | Identificazione del prodotto          |
| Descrizione   | Informazioni dettagliate              |
| Prezzo        | Prezzo di vendita                     |
| Categoria     | Organizzazione del catalogo           |
| Immagine      | Presentazione visuale                 |
| Disponibilità | Gestione dello stock                  |
| Varianti      | Taglie / caratteristiche del prodotto |

La logica relativa ai prodotti è separata all'interno del backend nel modulo `products`.

---

# 🏷️ Categories

Le categorie permettono di organizzare il catalogo e facilitare la navigazione.

```text
Categories
    │
    ├── Category A
    │      ├── Product
    │      ├── Product
    │      └── Product
    │
    ├── Category B
    │      ├── Product
    │      └── Product
    │
    └── Category C
           └── Product
```

Il backend dedica un modulo specifico alla gestione delle categorie.

---

# ⭐ Reviews

Il progetto prevede un dominio specifico per le **recensioni dei prodotti**.

```text
User
 │
 ▼
Product
 │
 ▼
Review
 │
 ├── Rating
 ├── Comment
 └── Author
```

La separazione del dominio `reviews` permette di mantenere indipendente la gestione delle recensioni rispetto ai prodotti e agli utenti.

---

# 🔐 Authentication & Security

L'autenticazione è progettata utilizzando **JWT**, mentre le password vengono protette tramite **bcrypt**.

| Meccanismo            | Tecnologia        | Obiettivo                                   |
| --------------------- | ----------------- | ------------------------------------------- |
| Authentication        | JWT               | Identificazione dell'utente                 |
| Password Hashing      | bcrypt            | Protezione delle password                   |
| Validation            | Pydantic          | Validazione dei dati                        |
| Rate Limiting         | SlowAPI           | Limitazione delle richieste                 |
| Configuration         | Pydantic Settings | Gestione sicura della configurazione        |
| Environment Variables | `.env`            | Separazione della configurazione dal codice |

Le dipendenze per JWT, bcrypt, Pydantic e SlowAPI sono presenti nella configurazione backend.

---

# 🧠 Frontend Architecture

Il frontend è realizzato con **React 19** e organizzato tramite componenti riutilizzabili.

La struttura attuale comprende:

```text
frontend/
│
├── Brand Identity/
├── Public/
├── UX/
│
└── src/
    ├── component/
    ├── img/
    ├── App.css
    ├── App.jsx
    ├── index.css
    └── main.jsx
```

Sono inoltre presenti:

* configurazione Vite;
* configurazione ESLint;
* routing tramite React Router;
* Tailwind CSS;
* componenti React modulari.

---

# 🎨 UI / UX

Il progetto non si limita alla sola implementazione tecnica: la repository contiene anche materiale dedicato alla progettazione visuale e all'esperienza utente.

| Directory        | Scopo                                |
| ---------------- | ------------------------------------ |
| `Brand Identity` | Identità visiva del progetto         |
| `Public`         | Materiale pubblico / contenuti       |
| `UX`             | Progettazione dell'esperienza utente |
| `src/component`  | Componenti dell'interfaccia          |
| `src/img`        | Asset grafici                        |

Questa separazione evidenzia l'intenzione di mantenere distinti **design, UX e implementazione frontend**.

---

# 📍 Google Maps

Il frontend utilizza:

```text
@vis.gl/react-google-maps
```

per l'integrazione con **Google Maps**.

Questa funzionalità può essere utilizzata per mostrare informazioni geografiche relative a negozi, punti vendita o altre informazioni legate alla localizzazione.

La libreria è presente tra le dipendenze ufficiali del frontend.

---

# 🗄️ Database & Migrations

Il progetto utilizza **Alembic** per il versionamento dello schema PostgreSQL.

Struttura:

```text
backend/
│
├── alembic/
├── alembic.ini
├── app/
└── database/
```

L'utilizzo di Alembic permette di gestire l'evoluzione dello schema del database attraverso migration versionate.

---

# 🐳 Docker

Il progetto include una configurazione **Docker Compose** per eseguire backend e PostgreSQL tramite container.

```text
┌──────────────────────────┐
│       Docker Compose     │
│                          │
│  ┌────────────────────┐  │
│  │      Backend       │  │
│  │ FastAPI + Uvicorn  │  │
│  │     :8000          │  │
│  └─────────┬──────────┘  │
│            │             │
│            ▼             │
│  ┌────────────────────┐  │
│  │     PostgreSQL     │  │
│  │       :5432        │  │
│  └────────────────────┘  │
│                          │
└──────────────────────────┘
```

Il `docker-compose.yml` definisce:

| Service   | Tecnologia        |  Porta |
| --------- | ----------------- | -----: |
| `backend` | FastAPI + Uvicorn | `8000` |
| `db`      | PostgreSQL 18     | `5432` |

Il backend viene avviato tramite Uvicorn sulla porta `8000`, mentre PostgreSQL utilizza la porta `5432`.

---

# 🚀 Installation

## Prerequisites

| Software       | Versione / Requisito                           |
| -------------- | ---------------------------------------------- |
| **Node.js**    | Versione compatibile con il frontend           |
| **npm**        | Incluso con Node.js                            |
| **Python**     | Versione compatibile con le dipendenze backend |
| **PostgreSQL** | Oppure Docker                                  |
| **Docker**     | Consigliato per l'ambiente completo            |
| **Git**        | Per clonare il repository                      |

---

## 1. Clone Repository

```bash
git clone https://github.com/santie96/Vesta.git
cd Vesta
```

---

# 💻 Frontend Setup

```bash
cd frontend
npm install
```

Avvio dell'ambiente di sviluppo:

```bash
npm run dev
```

Build di produzione:

```bash
npm run build
```

Lint:

```bash
npm run lint
```

Preview della build:

```bash
npm run preview
```

Gli script sono definiti nel `package.json` del frontend.

---

# 🐍 Backend Setup

Entrare nella directory backend:

```bash
cd backend
```

Creare l'ambiente virtuale:

```bash
python -m venv .venv
```

Attivarlo:

### Windows

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

Installare le dipendenze:

```bash
pip install -r requirements.txt
```

Creare il file `.env` partendo dal template:

```bash
cp .env.example .env
```

Il backend dispone anche di una configurazione `.env.docker.example` dedicata all'ambiente Docker.

---

# ▶️ Start Backend

Il backend utilizza **Uvicorn** per eseguire FastAPI.

```bash
uvicorn app.main:app --reload
```

API disponibili su:

```text
http://localhost:8000
```

FastAPI fornisce inoltre automaticamente la documentazione interattiva delle API:

```text
http://localhost:8000/docs
```

---

# 🐳 Run with Docker

Per avviare backend e database:

```bash
docker compose up --build
```

Il compose configura automaticamente:

```text
Backend → localhost:8000
PostgreSQL → localhost:5432
```

Il database utilizza un volume Docker persistente per evitare la perdita dei dati durante il riavvio dei container.

Per arrestare i container:

```bash
docker compose down
```

---

# 📁 Project Structure

```text
Vesta/
│
├── PRD/
│   ├── Vesta_PRD_Frontend_Backend-ChatGPT.md
│   └── Vesta_PRD_Frontend_Backend-Claude.md
│
├── backend/
│   │
│   ├── alembic/
│   │
│   ├── app/
│   │   ├── categories/
│   │   ├── core/
│   │   ├── database/
│   │   ├── products/
│   │   ├── reviews/
│   │   ├── users/
│   │   └── main.py
│   │
│   ├── scripts/
│   │
│   ├── .env.example
│   ├── .env.docker.example
│   ├── Dockerfile
│   ├── alembic.ini
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── Brand Identity/
│   ├── Public/
│   ├── UX/
│   │
│   ├── src/
│   │   ├── component/
│   │   ├── img/
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── docker-compose.yml
└── .gitignore
```

La repository attuale mantiene quindi separati **requisiti/progettazione, frontend, backend e infrastruttura Docker**.

---

# 📚 Project Documentation

La directory `PRD` contiene documentazione dedicata alla progettazione del progetto:

```text
PRD/
│
├── Vesta_PRD_Frontend_Backend-ChatGPT.md
└── Vesta_PRD_Frontend_Backend-Claude.md
```

La presenza di questi documenti permette di mantenere una distinzione tra:

```text
Requirements
     ↓
Architecture
     ↓
Implementation
     ↓
Future Features
```

---

# 🚧 Development Status

Vesta è attualmente in **fase di sviluppo**.

L'architettura principale è già impostata:

| Componente                | Stato |
| ------------------------- | :---: |
| React frontend            |   🟢  |
| Vite                      |   🟢  |
| Tailwind CSS              |   🟢  |
| React Router              |   🟢  |
| FastAPI backend           |   🟢  |
| PostgreSQL                |   🟢  |
| SQLAlchemy                |   🟢  |
| Alembic                   |   🟢  |
| Docker Compose            |   🟢  |
| Product domain            |   🟢  |
| Category domain           |   🟢  |
| User domain               |   🟢  |
| Reviews domain            |   🟢  |
| E-commerce flows          |   🟡  |
| Checkout                  |   🟡  |
| Complete order management |   🟡  |
| Production deployment     |   ⚪   |

> Lo stato delle funzionalità è soggetto a cambiamento durante lo sviluppo.

---

# 🗺️ Roadmap

Le funzionalità previste per l'evoluzione del progetto comprendono:

### 🛍️ E-commerce

* [ ] Catalogo completo
* [ ] Filtri avanzati
* [ ] Ricerca prodotti
* [ ] Product detail
* [ ] Varianti prodotto
* [ ] Carrello
* [ ] Wishlist
* [ ] Checkout
* [ ] Gestione ordini

### 👤 User Experience

* [ ] Registrazione
* [ ] Login
* [ ] Profilo utente
* [ ] Storico ordini
* [ ] Gestione indirizzi
* [ ] Recensioni
* [ ] Wishlist

### ⚙️ Backend

* [ ] Completamento API
* [ ] Authentication flow
* [ ] Authorization
* [ ] Product management
* [ ] Category management
* [ ] Review management
* [ ] Order management

### 🛡️ Security

* [ ] Hardening authentication
* [ ] API validation
* [ ] Rate limiting
* [ ] Secure environment configuration
* [ ] Production security review

### 🚀 Deployment

* [ ] Production Docker configuration
* [ ] CI/CD
* [ ] Production database
* [ ] Frontend deployment
* [ ] Backend deployment

---

# 🎯 Project Goals

Vesta nasce con l'obiettivo di realizzare un **e-commerce moderno e scalabile**, mettendo in pratica competenze relative a:

* sviluppo frontend con React;
* progettazione di componenti riutilizzabili;
* routing client-side;
* responsive UI;
* Tailwind CSS;
* sviluppo di API REST;
* Python e FastAPI;
* ORM con SQLAlchemy;
* PostgreSQL;
* database migrations;
* autenticazione JWT;
* password hashing;
* validazione dei dati;
* gestione degli utenti;
* gestione di prodotti e categorie;
* gestione delle recensioni;
* containerizzazione Docker;
* progettazione software tramite PRD.

---

# 📊 Project Highlights

| Area                | Competenze dimostrate                         |
| ------------------- | --------------------------------------------- |
| **Frontend**        | React 19, Vite, React Router, Tailwind CSS    |
| **UI**              | Component architecture, responsive design, UX |
| **Backend**         | Python, FastAPI, REST API                     |
| **Database**        | PostgreSQL, SQLAlchemy, asyncpg               |
| **Migrations**      | Alembic                                       |
| **Authentication**  | JWT, bcrypt                                   |
| **Validation**      | Pydantic                                      |
| **Security**        | Rate limiting, authentication, validation     |
| **Maps**            | Google Maps API                               |
| **DevOps**          | Docker, Docker Compose                        |
| **Architecture**    | Frontend / REST API / Backend / Database      |
| **Documentation**   | PRD e progettazione tecnica                   |
| **Version Control** | Git / GitHub                                  |

---

# 📌 Current Status

**Vesta is an ongoing project.**

L'architettura full-stack, la separazione tra frontend e backend, la base del database e l'infrastruttura Docker sono già presenti. La piattaforma continua a evolversi con l'implementazione progressiva delle funzionalità e dei flussi e-commerce.

L'obiettivo finale è ottenere una piattaforma fashion e-commerce completa, mantenendo una struttura **modulare, manutenibile e scalabile**.

---

## 📄 License

La licenza del progetto verrà definita nella fase finale di sviluppo.
