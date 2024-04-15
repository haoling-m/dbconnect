## Notes on using Pgadmin
* pgadmin has psql and pquery tool 

#### insert a row
* table 'items' have 'id' and 'name' columns
* ```INSERT INTO items(id,name) VALUES (0,'Canon') RETURNING *;```
* use single quote not double
* ```INSERT INTO items(name) VALUES ('SIEMENS')```
* auto increse 'id'
