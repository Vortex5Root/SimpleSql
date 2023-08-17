
# SimpleSQL documentation

## Introduction

- SimpleSQL is a Python module that provides an object-oriented approach for working with SQLite databases. It allows creating and managing database tables, as well as querying and updating their contents. SimpleSQL is built on top of the SQLite3 module that comes with Python.

## Installation

- To install you can use.
  ```bash
    poetry install git+https://github.com/Vortex5Root/SimpleSql/
  ```

## Usage

### DataBase class

> The `DataBase` class represents a SQLite database. It provides methods for executing queries and managing tables.

#### Creating a database

- To create a database, instantiate the `DataBase` class with a name and optional path where the database should be stored. If no path is specified, the database will be created in a directory named `database` in the current working directory.

```python
db = DataBase('my_database')
```

#### Executing queries

- To execute a SQL query on the database, call the `exec()` method of the `DataBase` object and pass the query as a string. The method returns a list with two elements: a boolean indicating whether the query was executed successfully, and a cursor object that can be used to retrieve the query results.

```python
status, cursor = db.exec("SELECT * FROM my_table")
```

#### Managing tables

- To manage tables in the database, use the `get_table()` method of the `DataBase` object. This method returns a `Table` object that represents a table in the database.

```python
table = db.get_table('my_table')
```

#### Renaming a database

- To rename a database, use the `rename()` method of the `DataBase` object and pass the new name as a string. This method also updates the `db_name` attribute of the `DataBase` object.

```python
db.rename('new_database_name')
```

#### Getting a list of tables

- To get a list of tables in the database, use the `get_tables` property of the `DataBase` object. This property returns a list of strings representing the names of the tables.

```python
tables = db.get_tables
```

### Table class

- The `Table` class represents a table in a SQLite database. It provides methods for creating, querying, and updating table contents.

#### Creating a table

- To create a table, instantiate the `Table` class with a database name and a table name. If the table already exists in the database, this method will do nothing.

```python
table = Table('my_database', 'my_table')
```

#### Generating table schema

- To generate a table schema, use the `gen()` method of the `Table` object and pass the variable names as a string. This method creates a table in the database with a column named "ell" and additional columns for each variable.

```python
table.gen('var1, var2, var3')
```

#### Retrieving column names

- To retrieve the column names of a table, use the `get_rows` property of the `Table` object. This property returns a list of strings representing the names of the columns.

```python
columns = table.get_rows
```

#### Querying table contents

- To query the contents of a table, use the `get()` method of the `Table` object and pass the query parameters as strings. This method returns a list of tuples representing the rows of the table that match the query.

```python
rows = table.get('var1 = "value1"')
```

#### Updating table contents

- To update the contents of a table, use the `exec()` method of the `Table` object and pass the update

### Class Table

The `Table` class provides an interface to interact with a table of a database. The class takes two arguments: `database` and `table_name`.

#### Properties

- `database`: Returns the database instance associated with the table.
- `tb_name`: Returns the name of the table.

#### Methods

##### `gen(variables)`

Generates a table with given variable names. The `variables` parameter is a string containing the variable names separated by commas. If the table is already created, this method has no effect. This method returns nothing.

##### `get_rows()`

Returns a list of rows in the table. If the table does not exist, it returns `False`.

##### `get(code='', value='', Expecial='')`

Returns a generator object that yields the rows of the table. The `code` parameter is a string containing the name of the column to filter by, and `value` is the value to filter. If the `code` is empty, it will return all rows. The `Expecial` parameter is a string that can contain additional SQL queries.

##### `update(target, set)`

Updates a row in the table. The `target` parameter is a tuple containing the name of the column to update and the value to filter. The `set` parameter is a tuple containing the name of the column to update and the new value. This method returns `True` if the update was successful, otherwise, it returns `False`.

##### `rename(table_name)`

Renames the table to a new name specified by the `table_name` parameter. This method returns `True` if the rename was successful, otherwise, it returns `False`.

##### `bluk_headler(query)`

Handles the bulk queries of the table. If bulk mode is turned on, it appends the query to the query list. When the query list reaches a certain number (default is 500), it will execute all queries. This method returns `False` if the table is in the blocked state, otherwise, it returns `True`.

##### `__iadd__(str_data)`

Adds a new row to the table. The `str_data` parameter is a string containing the values separated by commas. This method returns `self`.

##### `__isub__(str_query)`

Deletes a row from the table. The `str_query` parameter is a string containing the column name and value to filter by separated by commas. This method returns `self`.

### Example Usage

```python
from SimpleSQL import Table, DataBase

# create a database instance
database = DataBase("example.db")

# create a table instance
table = Table(database, "my_table")

# generate the table
table.gen("col1, col2, col3")

# add a row to the table
table += "value1, value2, value3"

# get all rows from the table
for row in table.get():
    print(row)

# update a row in the table
table.update(("col1", "value1"), ("col2", "new_value2"))

# rename the table
table.rename("new_table_name")

# delete a row from the table
table -= "col1,value1"
```
