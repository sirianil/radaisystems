Running the application:

`docker build -t radaisystems .`

`docker run -p 80:80 radaisystems`

The application is running now. Navigate to on your browser locally to send requests.

Running Tests:

`source .venv/bin/activate`

`pip install -r requirements.txt`

`pytest tests/`

Setup explanation:

I have a simple Dockerfile that creates a working directory, copies and installs requiements in requirements.txt, copies the raw data into the container, navigates to the app directory and runs the app using the fastapi command.
Upon app start up, the raw data in CSV file is seeded into the database. Once the seeding is complete, the app is ready to take requests.

Design and Architectural choices:

I am choosing to implement the backend portion of the takehome exerise and I have implemented it in Python.

I have chosen to work with FastAPI for the web application template. I made FastAPI as my choice since it is the most popular and standard choice in the Python community, it is easy to work with and it provides off-the-shelf OpenAPI documentation for the APIs in my application.

Since the food facilities For the Database i am going with SQLAlchemy and SQLLite, because this works well with FastAPI. I have chosen relational database because it the nature of the food facilities dataset being Structured and Tabluar maps naturally to a table and also for querying easily.

I am using Pandas to easily be able to convert the simple dataset into a pandas dataframe. This pandas dataframe is used to seed the database.

I considered some different alternatives for storage:
1. Simple In-memory approach: Because the particualr dataset we are considering, the simplest and least code would just be to load the whole dataset in memory. But this will quickly become ineffecient as the size of dataset grows. Having a SQLite DB helps us load only relevant rows in memory, and also add indexes to make search faster as dataset size grows.

When the docker image is run and on app start, the database will start and we'll create tables. Once table is created, we will seed it with data from the raw csv file. Once this is complete, we are ready to take requests from users.

I also went with a simple container and decided to seed on startup and decided to go against more complex solutions like external database or external file mount. We could consider doing this if the size of the dataset was larger.

Ie have also decided to drop data the following columns from the database: cnn, blocklot, block, lot, X, Y, NOISent, Received, PriorPermit, Location. The reason is that we do not need these for the current endpoints. we might consider adding it if we're expanding the application to support additional endpoints that may require this data. 

