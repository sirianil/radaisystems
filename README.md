# Run the application

`docker build -t radaisystems .`

`docker run -p 80:80 radaisystems`

The application will run locally now. Navigate to on your browser to http://0.0.0.0/ to send requests or follow instructions from FastAPI on your terminal to run the app.
app is hosted in / and API documentaion in /docs.

#### Setup explanation

I have a simple Dockerfile that creates a working directory, copies and installs requiements in requirements.txt, copies the raw data into the container, navigates to the app directory and runs the app using the fastapi command.
Upon app start up, the raw data in CSV file is seeded into the database. Once the seeding is complete, the app is ready to take requests.

# Run Tests

First set up the virtual environment required to run the unit tests and activate it. Once the required packages are installed the tests can be run locally.

`python3 -m venv .venv`

`source .venv/bin/activate`

`pip install -r requirements.txt`

`pytest tests/`

# Repository Structure
app/
  ├── main.py              # app init, static route, router
  api/                                                                  
  │   └── permits.py       # route handlers                                                 
  services/                                                                                  
  │   └── permits.py       # Business logic   
  models/                                                                                    
  │   ├── orm.py           # Permit SQLAlchemy model                                             
  │   └── schemas.py       # PermitResponse, NearestPermitResponse                               
  db/                                                                                        
  ├── session.py           # engine, Base, get_db                                                
  └── seed.py              # seed()

The source files are organized to help with separation of concerns. At the root level is main.py which helps with initialzing the app and registering the required routes.
main.py also initializes the database in db/. Database is setup and the seed method is called which seeds the SQLite DB using the raw data from the CSV file in raw_data/.
main.py also sets up the required routes in api/permits.py. There are three routes one for each of the required task. Once the routes are set up and a request is recieved, it is handed over to the services/permits.py to access the db and handle the bussiness logic. Schemas for both the database tables and app responses are defined in models/.
This structure helps in separation of concern such that db access happens only in the service, schemas are kept separate and made accessible to business logic, etc,.

# Design and Architectural choices:

## Libraries and packages used.
I am choosing to implement the backend portion of the takehome exerise and I have implemented it in Python.

### FastAPI and pydantic
I have chosen to work with FastAPI for the web application template. I made FastAPI as my choice since it is the most popular and standard choice in the Python community, it is easy to work with and it provides off-the-shelf OpenAPI documentation for the APIs in my application.

### SQLAlchemy and SQLite

Since the food facilities For the Database i am going with SQLAlchemy and SQLLite, because this works well with FastAPI. I have chosen relational database because it the nature of the food facilities dataset being Structured and Tabluar maps naturally to a table and also for querying easily.

## Business logic design

The business logic for searching by applicants and addresses is by using a SQL Query to fetch the matching rows. 

The business logic for searching the 5 closest trucks given the latitude and longitude is:

The brute force solution was the fetch all the rows from the permits table and pick the 5 trucks that are closest. But this would be a very ineffecient design, because we would load the entire table into memory. 

So i decided to have a bounding box that would help us limit the number of rows we get as a result from our SQL Query. So we have a bounding box that fetches all trucks within the specified distance using the SQL query. And we then sort it to find the five closest.

But with the above approach, we may run into a case where there are no trucks within the specified limit of the bounding box. So we keep incremtally increasing the boundary of the box until we expand enough to cover the entire region. This approximately covers the entire SF region.

## Alternatives considered

### Storage 
1. Simple In-memory approach: Because the particualr dataset we are considering, the simplest and least code would just be to load the whole dataset in memory. But this will quickly become ineffecient as the size of dataset grows. Having a SQLite DB helps us load only relevant rows in memory, and also add indexes to make search faster as dataset size grows.

When the docker image is run and on app start, the database will start and we'll create tables. Once table is created, we will seed it with data from the raw csv file. Once this is complete, we are ready to take requests from users.

I also went with a simple container and decided to seed on startup and decided to go against more complex solutions like external database or external file mount. We could consider doing this if the size of the dataset was larger.

Ie have also decided to drop data the following columns from the database: cnn, blocklot, block, lot, X, Y, NOISent, Received, PriorPermit, Location. The reason is that we do not need these for the current endpoints. we might consider adding it if we're expanding the application to support additional endpoints that may require this data. 

### Nearest Permit business logic
I brainstormed using the ([Google Maps Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/overview)) to fetch the nearest 5 trucks. 
There are some advantages of this:
1. Unlike the current logic where we fetch the 5 trucks based on displacement distance, the distance API will help us calculate the actual distance by road. This might be a nice feature to have as we start having real users to the app.

One of the main reasons I didn't proceed with actually implementing it is that I discovered that I'll need a Google Maps API key and also that each API is charged on a per call basis. Because there would be a lot of testing overhead for this, i decided to go with a simpler approach.

# Current problems and Scaling considerations

## Choice of Database
As the size of the database increases, we may want to consider a different Database such as PostGres or other which helps with effiency.

## Database Index
We can add indices to most commonly accessed columns. This could be columns like Applicant, address or latitude and longitude.

## Choice of Python app library
There are a couple of other libraries i could have used such as Flask or Django. 

## Authentication and Authorization
As the app scales, we need to add more authenication and authorization. Even though the current data in the database may be public data, in future we may add more personal or sensistive information about the owners of the truck etc,. In such cases, we'd definiely need authentication before we can honor requests to the app.

# Things i would do if I had more time

I would add a linter to the repository to help with code quality and code consistency as we start having more developers contributing to the app. 

I would also add end to end tests or integration tests in addition to unit tests.

I would also add a good CI/CD pipeline or commit hooks that would run the tests and the linter upon each commit or when a Pull request is opened against the main branch.

Instead of having a static HTML page with embedded Javascript and CSS, i would use a different front end framework to support a more sophesticated UI with more features. 

I would add more structured logging through out the system with more consistent log level set up. Right now i only have print statments, but it might be useful to have more granular log levels and logging.
