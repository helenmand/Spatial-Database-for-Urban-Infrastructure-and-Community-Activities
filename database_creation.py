import psycopg2

# connection to the DB
conn = psycopg2.connect(
   #database="demodb", 
   #user='elenimandana',
   host='127.0.0.1', 
   port= '5432'
)

cursor = conn.cursor()
conn.autocommit = True

# cursor.execute("CREATE EXTENSION postgis;")

# create non-spatial entities
# citizen
createTable = '''  
CREATE TABLE citizen (
    cid varchar(10) NOT NULL,
    first_name varchar(30) DEFAULT NULL,
    last_name varchar(30) DEFAULT NULL,
    occupation varchar(30) DEFAULT NULL,
    age INT DEFAULT NULL,
    sex INT DEFAULT NULL,
    livesIn varchar(10) NULL,
    owns varchar(10) NULL,
    PRIMARY KEY (cid)
);
'''
cursor.execute(createTable)

# business
createTable = '''  
CREATE TABLE business (
    buid varchar(10) NOT NULL,
    name varchar(50) DEFAULT NULL,
    field varchar(30) DEFAULT NULL,
    type varchar(30) DEFAULT NULL,
    provides varchar(10) NULL,
    basedIn varchar(10) NULL,
    PRIMARY KEY (buid)
);
'''
cursor.execute(createTable)

# product (or service)
createTable = '''  
CREATE TABLE product (
    prid varchar(10) NOT NULL,
    name varchar(50) DEFAULT NULL,
    price INT DEFAULT NULL,
    description varchar(100) DEFAULT NULL,
    isoffered varchar(10) NULL,
    PRIMARY KEY (prid)
);
'''
cursor.execute(createTable)

# happening
createTable = '''  
CREATE TABLE happening (
    hid varchar(10) NOT NULL,
    name varchar(50) DEFAULT NULL,
    organizer varchar(50) DEFAULT NULL,
    type varchar(30) DEFAULT NULL,
    date DATE DEFAULT NULL, 
    fee INT DEFAULT NULL,
    description varchar(100) DEFAULT NULL,
    PRIMARY KEY (hid)
);
'''
cursor.execute(createTable)

# create spatial entities
createTable = '''  
CREATE TABLE building (
    bid varchar(10) NOT NULL,
    address varchar(15) DEFAULT NULL,
    type varchar(30) DEFAULT NULL,
    floors INT DEFAULT NULL,
    constructionyear INT DEFAULT NULL,
    location GEOMETRY DEFAULT NULL,
    PRIMARY KEY (bid)
);
'''
cursor.execute(createTable)


# Close cursor and connection
cursor.close()
conn.close()
