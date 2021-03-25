# HonoursThesis
Repository for COSC449 Honour's Thesis

## System Information
Relational Model

DBMS: SQL SERVER Management Studio

Host: localhost 

Related Files: sql_data.sql proxi_mk01.ddl sql_data01.sql sql_data10e3.sql sql_data10e6.sql


Graph Model

DBMS: Neo4J Browser

Host: localhost

Related Files: cypher_node_data.cql cypher_rel_data.cql


## data_generation.py
Language: Python 3

Libraries: Faker

Dependencies: common-verbs.txt common-nouns.txt common-interests.txt

Breakdown:

  The data generation is divided up into different functions, each responsible for generating data for a specific table or node. Some cypher relationships are generated alongside the nodes they connect to ensure consistency between SQL Foreign keys and Cypher relationships. Each function can take a set of parameters; (n) is the number of tuples the function should create, (x, y, z) each holds the number of one of (Users, Groups, Events, Interests, Posts) to make sure that a relationship or foreign key does not reference a node that does not exist. Each table/node is indexed by an incremental integer.
  The script creates three files; sql_file, cypher_node_file, cypher_rel_file. The sql_file contains the INSERTS for every table in order to watch for dependencies. The cypher_node_file contains the CREATE node statements for every node, and the cypher_rel_file contains the MATCH CREATE statements that match the two nodes to connect, then creates a relationship between them. The final function header generateAllData takes in a number for each table and generates the data accordingly.

Known Issues: Can generate duplicates. Interest nodes have a limit (473). 

*Can now generate data given number of rows required.


