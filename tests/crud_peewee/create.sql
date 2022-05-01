CREATE TABLE persons (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    FirstName varchar(255) NOT NULL,
    LastName varchar(255) NOT NULL,
    Address varchar(255),
    City varchar(255)
);