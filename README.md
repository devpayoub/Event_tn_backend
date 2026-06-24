# Event TN — Backend

FastAPI backend for the Event TN platform — a social events, posts, and meetings application with JWT authentication.

## Tech Stack

- **Python 3.11+** / **FastAPI** — async-first web framework
- **MongoDB** via **MongoEngine** ODM (MongoDB Atlas)
- **JWT** authentication (python-jose + passlib/bcrypt)
- **Pydantic v2** — request/response schema validation

## Setup

```bash
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

Create `.env`:

```
MONGODB_URI=mongodb+srv://<user>:<pass>@<cluster>.mongodb.net/
JWT_SECRET=<your-secret>
```

Run:

```bash
uvicorn main:app --reload --port 8000
```

API docs at [http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)

## API Endpoints

### Auth (`/api/auth`)
| Method | Path | Description |
|--------|------|-------------|
| POST | `/signup` | Register a new user |
| POST | `/login` | Login, returns JWT |

### Users (`/api/users`)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/me` | Get current user profile |

### Events (`/api/events`)
| Method | Path | Description |
|--------|------|-------------|
| GET | `` | List events (published only for anonymous) |
| POST | `` | Create an event (auth required) |
| GET | `/{id}` | Get event by ID |
| PATCH | `/{id}` | Update event (owner only) |
| DELETE | `/{id}` | Delete event (owner only) |

### Posts (`/api/posts`)
| Method | Path | Description |
|--------|------|-------------|
| GET | `` | List posts (published only for anonymous) |
| POST | `` | Create a post (auth required) |
| GET | `/{id}` | Get post by ID |
| PATCH | `/{id}` | Update post / toggle like (owner only, except likes) |
| DELETE | `/{id}` | Delete post (owner only) |

### Comments (`/api/comments`)
| Method | Path | Description |
|--------|------|-------------|
| GET | `` | List comments (filtered by `postId` or `eventId`) |
| POST | `` | Create a comment (auth required) |
| PATCH | `/{id}` | Update comment (author only) |
| DELETE | `/{id}` | Delete comment (author only) |

### Meetings (`/api/meetings`)
| Method | Path | Description |
|--------|------|-------------|
| GET | `` | List meetings |
| POST | `` | Create a meeting (auth required) |
| GET | `/{id}` | Get meeting by ID |
| PATCH | `/{id}` | Update meeting (owner only) |
| DELETE | `/{id}` | Delete meeting (owner only) |

## Project Structure

```
back/
├── main.py             # FastAPI app, CORS, router registration
├── config.py           # Pydantic Settings (env vars)
├── auth.py             # JWT creation / password hashing
├── dependencies.py     # Auth dependency (get_current_user)
├── models/             # MongoEngine document models
│   ├── user.py
│   ├── event.py
│   ├── post.py
│   ├── comment.py
│   └── meeting.py
├── schemas/            # Pydantic request/response schemas
│   ├── user.py
│   ├── event.py
│   ├── post.py
│   ├── comment.py
│   └── meeting.py
└── routes/             # Route handlers
    ├── auth.py
    ├── users.py
    ├── events.py
    ├── posts.py
    ├── comments.py
    └── meetings.py
```
