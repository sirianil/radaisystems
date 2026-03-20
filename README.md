# RadAI Systems — Food Facility Permit API

## Running the Application

```bash
docker build -t radaisystems .
docker run -p 80:80 radaisystems
```

The application will run locally. Navigate to `http://0.0.0.0/` in your browser to send requests, or follow the FastAPI instructions printed to your terminal. The app is served at `/` and API documentation is available at `/docs`.

### Setup Explanation

The Dockerfile creates a working directory, copies and installs the dependencies from `requirements.txt`, copies the raw data into the container, navigates to the app directory, and starts the app using the `fastapi` command. On startup, the raw CSV data is seeded into the database. Once seeding is complete, the app is ready to accept requests.

---

## Running Tests

Set up and activate a virtual environment, install the required packages, then run the tests:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests/
```

---

## Repository Structure

```
app/
├── main.py              # App initialization, static route, router registration
├── api/
│   └── permits.py       # Route handlers
├── services/
│   └── permits.py       # Business logic
├── models/
│   ├── orm.py           # Permit SQLAlchemy model
│   └── schemas.py       # PermitResponse, NearestPermitResponse
└── db/
    ├── session.py       # Engine, Base, get_db
    └── seed.py          # seed()
```

The source files are organized around separation of concerns. At the root level, `main.py` initializes the app, sets up the database, calls the seed method to populate the SQLite DB from the CSV file in `raw_data/`, and registers the routes defined in `api/permits.py`. There are three routes — one for each required task. Once a request is received, it is handed off to `services/permits.py` which handles all database access and business logic. Schemas for both database tables and API responses are defined in `models/`.

---

## Design and Architectural Choices

### Libraries and Packages

I chose to implement the backend portion of this exercise in Python.

**FastAPI and Pydantic** — I chose FastAPI as the web framework because it is the most popular and standard choice in the Python ecosystem. It is easy to work with and provides off-the-shelf OpenAPI documentation for all endpoints.

**SQLAlchemy and SQLite** — For the database, I went with SQLAlchemy and SQLite because they integrate well with FastAPI. I chose a relational database because the food facilities dataset is structured and tabular, which maps naturally to a relational table and makes querying straightforward.

### Business Logic

**Search by applicant and address** — implemented using a SQL query that fetches the matching rows directly.

**Nearest 5 trucks by coordinates** — the brute force approach would be to fetch all rows from the permits table and pick the 5 closest trucks. However, this would load the entire table into memory and is inefficient.

Instead, I implemented a bounding box approach to limit the number of rows returned by the SQL query. The bounding box fetches all trucks within a specified distance, and then those results are sorted to find the five closest. If there are no trucks within the initial bounding box, the box is incrementally expanded until it covers enough of the SF region to return at least 5 results.

---

## Alternatives Considered

### Storage

**In-memory storage** — given the size of this particular dataset, the simplest approach would be to load the entire dataset into memory. However, this quickly becomes inefficient as the dataset grows. Using SQLite means only relevant rows are loaded into memory, and indexes can be added to speed up searches as the data scales.

I also decided against more complex solutions like an external database or an external file mount, in favor of a simple self-contained container that seeds on startup. That trade-off would need revisiting if the dataset were significantly larger.

I dropped the following columns from the database as they are not needed for the current endpoints: `cnn`, `blocklot`, `block`, `lot`, `X`, `Y`, `NOISent`, `Received`, `PriorPermit`, `Location`. They can be added back if additional endpoints requiring this data are introduced.

### Nearest Permit Business Logic

I considered using the [Google Maps Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/overview) to find the nearest 5 trucks. One advantage is that it calculates actual road distance rather than straight-line displacement, which would be a useful feature as the app gains real users.

The main reason I didn't implement it is that it requires a Google Maps API key, and each call is charged on a per-request basis. Given the testing overhead this would introduce, I decided to go with the simpler bounding box approach instead.

---

## Current Problems and Scaling Considerations

**Choice of database** — as the dataset grows, switching to a more capable database such as PostgreSQL would improve performance and concurrency.

**Database indexes** — indexes could be added to the most frequently queried columns, such as `applicant`, `address`, `latitude`, and `longitude`.

**Choice of Python web framework** — Flask and Django are both viable alternatives that could be evaluated as requirements evolve.

**Authentication and authorization** — as the app scales, proper authentication and authorization will be necessary. Even though the current data is public, future versions might include sensitive information about truck owners, which would require enforcing access controls before honoring requests.

---

## Things I Would Do with More Time

- Add a linter to enforce code quality and consistency as more developers contribute to the project.
- Add end-to-end and integration tests in addition to the existing unit tests.
- Set up a CI/CD pipeline or commit hooks to run tests and the linter on each commit or when a pull request is opened against the main branch.
- Replace the static HTML page with embedded JavaScript and CSS with a proper frontend framework to support a more sophisticated UI with additional features.
- Add structured logging throughout the system with consistent log levels. Currently only `print` statements are used, but more granular logging would greatly improve observability.
