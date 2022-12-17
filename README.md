# Roddit
 Vasilevich Maksim | 053504

**Theme of database**: social media (analogy of Rediit)

**Technology**: PostgreSQL, Python, FastAPI

**Used functionalities**: Transactions, Procedures, Functions, Triggers, Joins, Unions, Subqueries, Advanced SQL queries

## Labaratory work 1:
In this laboratory work, it is necessary to:
1. Determine the topic of the project being developed in the semester.
2. Define the functional requirements for the project.
3. Define and justify the list of DB entities that meet the functional requirements of the project.
4. The number of related entities must be at least 8.
5. Each of the types of connections must be present.
6. Schematically depict a non-normalized database schema.
7. Describe each entity (field name, type, constraints, relationship to other entities)

## Labaratory work 2:
In this laboratory work it is necessary:
1. To develop a datalogical model approved in the first laboratory database.
2. Bring the database to the third normal form.
3. If it is necessary to denormalize the database, be ready to prove your point of view.

## Labaratory work 3:
In this laboratory work, it is necessary to:
1. Develop a physical database model (create a database on your device).
2. Impose restrictions on the database.
3. Fill the database with test values.
4. Create a pool of queries required for simple operations on data in the database.

Acceptance Criteria:
- A physical database model with imposed restrictions has been created in accordance with the scheme approved in the second laboratory work.
- All tables, relationships, entities should be written using SQL scripts independently, without automatic code generation by the environment.
- ALL REQUESTS for creating and filling in the database must be SAVED for demonstration to the teacher.
- Indexes, constrints, and other restrictions have been put down.
- The database is filled with test data.
- A pool of SQL queries has been compiled for simple database operations.
- Willingness to demonstrate working with the simplest (and slightly complicated) SQL queries on an existing database.
- Willingness to explain the meaning of all SQL statements used in the code + operators for the simplest sampling and filtering.

## Labaratory work 4:
In this laboratory work, it is necessary:
1. Create a pool of queries for a complex selection from the database.
2. Create a pool of queries to get views in the database.
3. Create a pool of queries to get grouped data.
4. Create a pool of queries required for complex operations on data in the database.
5. Check the written queries on your database.

Acceptance Criteria:
- A pool of SQL queries has been compiled for a complex selection from the database:
a. Queries with multiple conditions.
b. Queries with nested constructs
c. Other complex selections required in your project.
- A pool of SQL queries has been compiled to get views in the database:
a. JOIN queries of various types (INNER, OUTER, FULL, CROSS, SELF)
- A pool of SQL queries has been compiled to get grouped data:
a. GROUP BY + aggregating functions
b. HAVING
c. UNION
- A pool of SQL queries has been compiled for complex data operations:
a. EXISTS
b. INSERT INTO SELECT
c. CASE
d. EXPLAIN
- The above queries are only approximate, it is not necessary to use everything in the code for your database.
- Willingness to explain the meaning of all SQL statements used in the code + operators listed above + willingness to write the code of any operator from the laboratory for your data.
- Theoretical knowledge on queries and operators.

## Labaratory work 5:
In this laboratory work, it is necessary:
1. Create a pool of triggers necessary for the correct operation of your database logic.
2. Create a pool of stored procedures necessary for the correct operation of your database.
3. Check the written triggers and procedures on your database.

Acceptance Criteria:
- A pool of triggers necessary for the correct operation of the database in the context of your existing TOR and approved scheme has been compiled:
a. Example: recalculation of the order amount when adding a new product to the order / logging
b. Triggers are written in SQL and connected to the database
c. Triggers should implement the necessary logic of the future application
- A pool of stored SQL procedures has been compiled to perform the necessary operations on the database:
a. Procedures should be created logically for queries that are frequently used during the operation of the application
b. Procedures should be stored in the database and called from other queries or the console
- Ability to demonstrate the operation of triggers and procedures
- Ability to implement new triggers and procedures
- Theoretical knowledge in the context of laboratory

## Labaratory work 6:
In this laboratory work, it is necessary:
1. Create an application with a user interface in which the database developed during the semester acts as the main database of the project.

Acceptance Criteria:
- The application must have a user interaction interface:
a. If the application is console-based: a list of commands is implemented through which the user interacts with the system
b. If the application is web/desktop: a conditional frontend is implemented through which the user interacts with the system
-The application must comply with the TOR approved in the 2nd laboratory
- The database for the project is a database designed in LR 1-5 and connected to the project directly
- Work and interaction with the database is carried out in one of three ways:
a. Direct queries to the database from the application
b. Self-written ORM (demonstration of YOUR ORM source code is mandatory)
c. ORM.raw_sql() or analogues in your technologies
d. Thus, interaction with the database should be carried out EXCLUSIVELY using SQL one way or another. Otherwise, the laboratory WILL NOT BE counted
- To interact with the database, it is necessary to use queries developed in LR 3-5
- The ability to add some details to the project code directly upon delivery
- Theoretical knowledge in the context of laboratory

© iMaksus, 2022
