import psycopg2

# prompt the user for the database name and username
database_name = input("Enter the database name: ")
username = input("Enter the username: ")

# connection to the DB
conn = psycopg2.connect(
    database=database_name, 
    user=username,
    host='127.0.0.1', 
    port='5432'
)

cursor = conn.cursor()
conn.autocommit = True

# create extension postgis
cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
print("PostGIS extension created successfully.")

# create non-spatial entities
createTableQueries = [
'''
CREATE TABLE Building (
    bid INT NOT NULL PRIMARY KEY,
    address VARCHAR(255),
    type VARCHAR(255),
    floors INT,
    constructionYear INT,
    location GEOMETRY DEFAULT NULL
);
'''
'''
CREATE TABLE Citizen (
    cid INT NOT NULL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    age INT,
    sex CHAR(1),
    occupation VARCHAR(255),
    livesIn INT, 
    FOREIGN KEY (livesIn) REFERENCES Building(bid)
);
''',
'''
CREATE TABLE Business (
    buid INT NOT NULL PRIMARY KEY,
    name VARCHAR(255),
    field VARCHAR(255),
    type VARCHAR(255),
    businessBasedIn INT,
    FOREIGN KEY (businessBasedIn) REFERENCES Building(bid),
    owner_cid INT,
    FOREIGN KEY (owner_cid) REFERENCES Citizen(cid)
);
''',
'''
CREATE TABLE ProductService (
    prid INT NOT NULL PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10,2),
    description TEXT,
    offeredByBusiness INT,
    FOREIGN KEY (offeredByBusiness) REFERENCES Business(buid)
);
''',
'''
CREATE TABLE Park (
    pid INT NOT NULL,
    type VARCHAR(255),
    name VARCHAR(50) DEFAULT NULL,
    location GEOMETRY DEFAULT NULL, 
    PRIMARY KEY (pid)
);
''',
'''
CREATE TABLE Road (
    rid INT NOT NULL PRIMARY KEY,
    name VARCHAR(255),
    lanes INT,
    type VARCHAR(255),
    location GEOMETRY DEFAULT NULL
);
''',
'''
CREATE TABLE Landmark (
    lid INT NOT NULL PRIMARY KEY,
    type VARCHAR(255),
    name VARCHAR(255),
    fee DECIMAL(10,2),
    capacity INT,
    location GEOMETRY DEFAULT NULL
);
''',
'''
CREATE TABLE Happening (
    hid INT NOT NULL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    type VARCHAR(255),
    fee DECIMAL(10,2),
    date DATE,
    organizer VARCHAR(255),
    takesPlaceAt INT,
    FOREIGN KEY (takesPlaceAt) REFERENCES Park(pid)
);
''',
'''
CREATE TABLE Employment (
    cid INT NOT NULL,
    buid INT NOT NULL,
    PRIMARY KEY (cid, buid),
    FOREIGN KEY (cid) REFERENCES Citizen(cid),
    FOREIGN KEY (buid) REFERENCES Business(buid)
);
''',
'''
CREATE TABLE RoadLeadsToPark (
    rid INT NOT NULL,
    pid INT NOT NULL,
    PRIMARY KEY (rid, pid),
    FOREIGN KEY (rid) REFERENCES Road(rid),
    FOREIGN KEY (pid) REFERENCES Park(pid)
);
''',
'''
CREATE TABLE RoadLeadsToLandmark (
    rid INT NOT NULL,
    lid INT NOT NULL,
    PRIMARY KEY (rid, lid),
    FOREIGN KEY (rid) REFERENCES Road(rid),
    FOREIGN KEY (lid) REFERENCES Landmark(lid)
);
''',
'''
CREATE TABLE RoadLeadsToBuilding (
    rid INT NOT NULL,
    bid INT NOT NULL,
    PRIMARY KEY (rid, bid),
    FOREIGN KEY (rid) REFERENCES Road(rid),
    FOREIGN KEY (bid) REFERENCES Building(bid)
);
''',
'''
CREATE TABLE Sponsorship (
    buid INT NOT NULL,
    hid INT NOT NULL,
    PRIMARY KEY (buid, hid),
    FOREIGN KEY (buid) REFERENCES Business(buid),
    FOREIGN KEY (hid) REFERENCES Happening(hid)
);
'''
]

# creating the tables
for query in createTableQueries:
    cursor.execute(query=query)
    print(f"Table created successfully: {query.split('(')[0].split()[-1]}")

# add dummy data
insert_queries = [
    # buildings
    "INSERT INTO Building (bid, address, type, floors, constructionYear, location) VALUES (1, '1 Plaza Square', 'Commercial', 10, 2010, ST_GeomFromText('POLYGON((0 70, 0 80, 15 80, 20 75, 15 70, 0 70))'));",
    "INSERT INTO Building (bid, address, type, floors, constructionYear, location) VALUES (2, '2 Plaza Square', 'Commercial', 10, 2010, ST_GeomFromText('POLYGON((100 70, 100 80, 85 80, 80 75, 85 70, 100 70))'));",
    "INSERT INTO Building (bid, address, type, floors, constructionYear, location) VALUES (3, '300 Green St', 'Residential', 20, 2000, ST_GeomFromText('POLYGON((10 20, 10 50, 25 50, 25 20, 10 20))'));",
    "INSERT INTO Building (bid, address, type, floors, constructionYear, location) VALUES (4, '400 River St', 'Office', 15, 2005, ST_GeomFromText('POLYGON((30 0, 30 20, 49 20, 49 0, 30 0))'));",
    "INSERT INTO Building (bid, address, type, floors, constructionYear, location) VALUES (5, '500 Tower St St', 'Office', 15, 2005, ST_GeomFromText('POLYGON((80 42, 80 62, 100 62, 100 42, 80 42))'));"
    
    # parks
    """
    INSERT INTO Park (pid, type, name, location) VALUES (
        1, 
        'City', 
        'Grand Central Park', 
        ST_Difference(
            ST_GeomFromText('POLYGON((20 70, 20 80, 80 80, 80 70, 20 70))'), 
            ST_Union(
                ST_GeomFromText('POLYGON((20 70, 30 75, 20 80, 20 70))'), 
                ST_GeomFromText('POLYGON((80 70, 70 75, 80 80, 80 70))')  
            )
        )
    );
    """,
    """
    INSERT INTO Park (pid, type, name, location) VALUES (
        2,
        'City',
        'Southwest Park',
        ST_GeomFromText('POLYGON((5 5, 5 15, 25 15, 25 5, 5 5))')
    );
    """,
    "INSERT INTO Park (pid, type, name, location) VALUES (3, 'City', 'Triangle Park', ST_GeomFromText('POLYGON((85 40, 55 10, 55 40, 85 40))'));",
    
    # landmarks
    """
    INSERT INTO Landmark (lid, type, name, fee, capacity, location) VALUES (
        1, 
        'Monument', 
        'Central Statue', 
        5.00, 
        500, 
        ST_Buffer(ST_GeomFromText('POINT(50 75)'), 2)
    );
    """,
    "INSERT INTO Landmark (lid, type, name, fee, capacity, location) VALUES (2, 'Museum', 'Expanded City Museum', 10.00, 2000, ST_GeomFromText('POLYGON((28 33, 28 47, 42 47, 42 33, 28 33))'));",
    "INSERT INTO Landmark (lid, type, name, fee, capacity, location) VALUES (3, 'Bridge', 'Unique Bridge', 0.00, 0, ST_GeomFromText('POLYGON((52 39, 70 12, 81 29, 65 47, 52 39))'));",
    "INSERT INTO Landmark (lid, type, name, fee, capacity, location) VALUES (4, 'Tower', 'Downtown Tower', 0.00, 0, ST_GeomFromText('POLYGON((90 10, 90 20, 100 20, 100 10, 90 10))'));",
    
    # roads
    "INSERT INTO Road (rid, name, lanes, type, location) VALUES (1, 'Modified Road', 2, 'Local', ST_GeomFromText('LINESTRING(20 5, 20 -5, 90 -5, 95 10)'));",
    "INSERT INTO Road (rid, name, lanes, type, location) VALUES (2, 'Diagonal Road', 2, 'Local', ST_GeomFromText('LINESTRING(28 40, 25 15)'));",
    "INSERT INTO Road (rid, name, lanes, type, location) VALUES (3, 'East-West Boulevard', 2, 'Local', ST_GeomFromText('LINESTRING(25 35, 40 20)'));",
    "INSERT INTO Road (rid, name, lanes, type, location) VALUES (4, 'North-South Avenue', 2, 'Local', ST_GeomFromText('LINESTRING(15 15, 15 20)'));",
    "INSERT INTO Road (rid, name, lanes, type, location) VALUES (5, 'Central Street', 2, 'Local', ST_GeomFromText('LINESTRING(19.8 75, 29.8 75)'));",
    "INSERT INTO Road (rid, name, lanes, type, location) VALUES (6, 'Parkside Drive', 2, 'Local', ST_GeomFromText('LINESTRING(70 75, 80 75)'));",
    "INSERT INTO Road (rid, name, lanes, type, location) VALUES (7, 'Vertical Lane', 2, 'Local', ST_GeomFromText('LINESTRING(74 70, 74 40)'));",
    "INSERT INTO Road (rid, name, lanes, type, location) VALUES (8, 'Outer Loop Road', 2, 'Local', ST_GeomFromText('LINESTRING(100 15, 103 15, 103 55, 100 55)'));",
    "INSERT INTO Road (rid, name, lanes, type, location) VALUES (9, 'Peripheral Street', 2, 'Local', ST_GeomFromText('LINESTRING(95 70, 95 65, 35 65, 35 47)'));",
    "INSERT INTO Road (rid, name, lanes, type, location) VALUES (10, 'Transit Route', 2, 'Local', ST_GeomFromText('LINESTRING(80 57, 41 57, 41 47)'));",
    "INSERT INTO Road (rid, name, lanes, type, location) VALUES (11, 'Scenic Way', 2, 'Local', ST_GeomFromText('LINESTRING(50 77, 50 84, 0 84)'));",
    "INSERT INTO Road (rid, name, lanes, type, location) VALUES (12, 'Heritage Lane', 2, 'Local', ST_GeomFromText('LINESTRING(15 70, 59 43)'));",
    
    # citizen 
    "INSERT INTO Citizen (cid, first_name, last_name, age, sex, occupation, livesIn) VALUES (1, 'John', 'Doe', 35, 'M', 'Engineer', 1);",
    "INSERT INTO Citizen (cid, first_name, last_name, age, sex, occupation, livesIn) VALUES (2, 'Jane', 'Smith', 28, 'F', 'Teacher', 1);",
    "INSERT INTO Citizen (cid, first_name, last_name, age, sex, occupation, livesIn) VALUES (3, 'Mike', 'Brown', 40, 'M', 'Doctor', 2);",

    # business
    "INSERT INTO Business (buid, name, field, type, businessBasedIn, owner_cid) VALUES (1, 'Tech Innovations', 'Technology', 'Startup', 2, 1);",
    "INSERT INTO Business (buid, name, field, type, businessBasedIn, owner_cid) VALUES (2, 'Green Books', 'Retail', 'Bookstore', 3, 2);",
    "INSERT INTO Business (buid, name, field, type, businessBasedIn, owner_cid) VALUES (3, 'Epicurean Delights', 'Catering', 'Service', 1, 3);",
    "INSERT INTO Business (buid, name, field, type, businessBasedIn, owner_cid) VALUES (4, 'Art & Craft Supplies', 'Retail', 'Store', 4, 2);",
   
    # product/service
    "INSERT INTO ProductService (prid, name, price, description, offeredByBusiness) VALUES (1, 'Web Development Course', 199.99, 'Learn web development from scratch.', 1);",
    "INSERT INTO ProductService (prid, name, price, description, offeredByBusiness) VALUES (2, 'Fantasy Novel', 15.99, 'A gripping tale of magic and adventure.', 2);",
    "INSERT INTO ProductService (prid, name, price, description, offeredByBusiness) VALUES (3, 'Mobile App Development Course', 299.99, 'Comprehensive course on Android and iOS development.', 1);",
    "INSERT INTO ProductService (prid, name, price, description, offeredByBusiness) VALUES (4, 'Cybersecurity Workshop', 399.99, 'A workshop on cybersecurity essentials for beginners.', 1);",
    "INSERT INTO ProductService (prid, name, price, description, offeredByBusiness) VALUES (5, 'Historical Novels Collection', 59.99, 'A collection of best-selling historical novels.', 2);",
    "INSERT INTO ProductService (prid, name, price, description, offeredByBusiness) VALUES (6, 'Poetry Writing Course', 120.00, 'Learn to express yourself in verse with our online course.', 2);",
    "INSERT INTO ProductService (prid, name, price, description, offeredByBusiness) VALUES (7, 'Gourmet Catering Service', 500.00, 'Premium catering services for your events.', 3);",
    "INSERT INTO ProductService (prid, name, price, description, offeredByBusiness) VALUES (8, 'Wine Tasting Experience', 75.00, 'Explore fine wines with our sommelier.', 3);",
    "INSERT INTO ProductService (prid, name, price, description, offeredByBusiness) VALUES (9, 'Professional Artist Kit', 250.00, 'Everything an aspiring artist needs to get started.', 4);",
    "INSERT INTO ProductService (prid, name, price, description, offeredByBusiness) VALUES (10, 'Sculpture Materials Set', 180.00, 'High-quality materials for sculpture artists.', 4);",
    
    # happening
    "INSERT INTO Happening (hid, name, description, type, fee, date, organizer, takesPlaceAt) VALUES (1, 'Science Fair', 'Annual community science fair.', 'Educational', 0.00, '2024-05-15', 'City Council', 2);",
    "INSERT INTO Happening (hid, name, description, type, fee, date, organizer, takesPlaceAt) VALUES (2, 'Liberty Music Festival', 'A vibrant outdoor music festival featuring local and international artists.', 'Music', 25.00, '2024-07-20', 'Liberty Music Org', 2);",
    "INSERT INTO Happening (hid, name, description, type, fee, date, organizer, takesPlaceAt) VALUES (3, 'Skyline Art Expo', 'An exhibition of contemporary art and sculptures.', 'Art', 15.00, '2024-08-15', 'Artists United', 3);",
    "INSERT INTO Happening (hid, name, description, type, fee, date, organizer, takesPlaceAt) VALUES (4, 'Run for Hope', 'Annual charity run supporting local charities.', 'Charity', 10.00, '2024-09-05', 'Hope Foundation', 1);",
    "INSERT INTO Happening (hid, name, description, type, fee, date, organizer, takesPlaceAt) VALUES (5, 'Riverbank Food & Wine Fair', 'Experience the best local and international cuisines and wines.', 'Food & Wine', 0.00, '2024-10-10', 'City Culinary Club', 3);",
    "INSERT INTO Happening (hid, name, description, type, fee, date, organizer, takesPlaceAt) VALUES (6, 'Golden Gate History Tour', 'Guided historical tour of the Golden Gate Bridge.', 'Educational', 20.00, '2024-11-15', 'History Enthusiasts', 3);",

    # employment
    "INSERT INTO Employment (cid, buid) VALUES (1, 1);",
    "INSERT INTO Employment (cid, buid) VALUES (2, 2);",

    # sponsorship
    "INSERT INTO Sponsorship (buid, hid) VALUES (1, 1);"
    "INSERT INTO Sponsorship (buid, hid) VALUES (1, 2);",
    "INSERT INTO Sponsorship (buid, hid) VALUES (1, 4);",
    "INSERT INTO Sponsorship (buid, hid) VALUES (2, 3);",
    "INSERT INTO Sponsorship (buid, hid) VALUES (2, 5);",

    # RoadLeadsToBuilding
    "INSERT INTO RoadLeadsToBuilding (rid, bid) VALUES (2, 3);",
    "INSERT INTO RoadLeadsToBuilding (rid, bid) VALUES (2, 4);",
    "INSERT INTO RoadLeadsToBuilding (rid, bid) VALUES (4, 3);",
    "INSERT INTO RoadLeadsToBuilding (rid, bid) VALUES (5, 1);",
    "INSERT INTO RoadLeadsToBuilding (rid, bid) VALUES (6, 2);",
    "INSERT INTO RoadLeadsToBuilding (rid, bid) VALUES (8, 5);",
    "INSERT INTO RoadLeadsToBuilding (rid, bid) VALUES (9, 2);",
    "INSERT INTO RoadLeadsToBuilding (rid, bid) VALUES (10, 5);",
    "INSERT INTO RoadLeadsToBuilding (rid, bid) VALUES (12, 1);",

    # RoadLeadsToLandmark
    "INSERT INTO RoadLeadsToLandmark (rid, lid) VALUES (1, 4);",
    "INSERT INTO RoadLeadsToLandmark (rid, lid) VALUES (3, 2);",
    "INSERT INTO RoadLeadsToLandmark (rid, lid) VALUES (8, 4);",
    "INSERT INTO RoadLeadsToLandmark (rid, lid) VALUES (9, 2);",
    "INSERT INTO RoadLeadsToLandmark (rid, lid) VALUES (10, 2);",
    "INSERT INTO RoadLeadsToLandmark (rid, lid) VALUES (11, 1);",
    "INSERT INTO RoadLeadsToLandmark (rid, lid) VALUES (12, 3);",

    # RoadLeadsToPark
    "INSERT INTO RoadLeadsToPark (rid, pid) VALUES (1, 2);",
    "INSERT INTO RoadLeadsToPark (rid, pid) VALUES (3, 2);", 
    "INSERT INTO RoadLeadsToPark (rid, pid) VALUES (4, 2);",
    "INSERT INTO RoadLeadsToPark (rid, pid) VALUES (5, 1);",
    "INSERT INTO RoadLeadsToPark (rid, pid) VALUES (6, 1);",
    "INSERT INTO RoadLeadsToPark (rid, pid) VALUES (7, 1);",
    "INSERT INTO RoadLeadsToPark (rid, pid) VALUES (7, 3);",
    "INSERT INTO RoadLeadsToPark (rid, pid) VALUES (11, 1);",
]

# execute each insert query
for query in insert_queries:
    cursor.execute(query=query)
    print(f"Data inserted successfully: {query[:30]}...")

# close cursor and connection
cursor.close()
conn.close()

print("Database setup and data insertion completed successfully.")