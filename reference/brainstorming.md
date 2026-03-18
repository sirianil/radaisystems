Dataset: Mobile Food Facilities (Trucks) in SF.
Goal: Build an application.

Data:
1. locationid: string
2. Applicant: string
3. Facility Type: Push Cart | Truck
4. cnn: string ??
5. LocationDescription:
6. Address:
7. blocklot
8. block
9. lot
10. permit
11. status: APPROVED | REQUESTED | EXPIRED 
12. Food items
13. x
14. y
15. latitue
16. longitude
17. schedule
18. dayhours
19. NOISent
20. Approved: DateTime
21. Recieved: Date
22: PriorPermit: Number
23: ExpirationDate: Date Time
25. Location

Backend:
1. search by name of applicant
2. search by street name
3. Given latitude and longitude -> return 5 nearest food trucks.
4. tests

1. Application.
2. we have some data -> and essentially we are querying on that data. 
3. so my initial thoughts -> HTTP Server and REST APIs
4. server hosted locally - maybe local host
5. you can send a request to the local server -> server returns the response.
6. designing responses is important too -> like 404.
7. how to store the data -> locally? local database? how to ingest the data into the database?
8. if server is in python, what python framework to use to host the server?
9. what best way to write tests?
10. how to set up the project to run with docker and how to provide the dockerfile

Write down any thoughts in this document as you go, so in the end you can turn this into a README with all thoughts.

Things to keep in mind:
1. keep code simple and think of maintainablity
2. think of python style standards and guidelines
3. be consistent in all parts of the codebase
4. make the right technical choice for libraries, databases.
5. think of Object oriented programming principles.
6. write down everything and explain well in README.
7. ensure what is asked for is implemented.

1. test as you go. write the smallest piece of logic and test. and build on top of that. 
both local testing and automated tests.

Task Breakdown:
1. SPIKEs on:
    a. what packages or libraries to use - for python for server locally.
    b. what database to use for this data
    c. how to host this data locally
    d. how to run a simple server locally, run a REST API request and fetch something from database
    e. how to set up a dockerfile for this
2. how to break down things well:
    a. separate the API definitions: make that public and exportable.
    b. how to separate the business logic from the api definitions
    c. validation of the provided parameters
    d. fetching from the database effeciently
    e. transforming the data as required or business logic
    f. returning
    e. designing such that it is maintainable and well separated logic, like uses OOP concepts well.
    f. designs well with tests in mind. best way to write and run tests.



