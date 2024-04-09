import psycopg2

def get_predefined_query(choice):
    queries = {
        1: "SELECT Citizen.first_name, Citizen.last_name, Building.address FROM Citizen JOIN Building ON Citizen.livesIn = Building.bid;",
        2: "SELECT Building.address, COUNT(Citizen.cid) AS num_of_citizens FROM Citizen JOIN Building ON Citizen.livesIn = Building.bid GROUP BY Building.bid;",
        3: "SELECT AVG(age) AS average_age FROM Citizen;",
        4: "SELECT address, constructionYear FROM Building WHERE constructionYear = (SELECT MIN(constructionYear) FROM Building);",
        5: """SELECT Business.name, ProductService.price AS max_price FROM Business JOIN ProductService ON Business.buid = ProductService.offeredByBusiness WHERE ProductService.price = (
                SELECT MAX(price) FROM ProductService);""",
        6: """SELECT name FROM Business WHERE buid IN (
                SELECT offeredByBusiness FROM ProductService GROUP BY offeredByBusiness HAVING COUNT(prid) > (
                    SELECT AVG(count) FROM (SELECT COUNT(prid) AS count FROM ProductService GROUP BY offeredByBusiness) AS average_products)
            );""",
        7: """CREATE VIEW BusinessEmployeeCount AS SELECT Business.buid, Business.name, COUNT(Employment.cid) AS num_of_employees FROM Business JOIN Employment ON Business.buid = Employment.buid GROUP BY Business.buid;
        SELECT name, num_of_employees FROM BusinessEmployeeCount WHERE num_of_employees > 0;""",
        
        8: "SELECT pid, ST_Area(location) AS area, location AS geometry FROM Park WHERE name = 'Grand Central Park';",
        9: "SELECT Landmark.name, Park.name, ST_Distance(Landmark.location, Park.location) AS distance, Landmark.location AS landmark_geometry, Park.location AS park_geometry FROM Landmark, Park WHERE Landmark.name = 'Expanded City Museum' AND Park.name = 'Grand Central Park';",
        10: "SELECT r.name AS road_name, p.name AS park_name, ST_AsText(r.location) AS road_geometry, ST_AsText(p.location) AS park_geometry FROM Road r, Park p WHERE ST_Intersects(r.location, p.location);",
        11: "SELECT Landmark.name AS LandmarkName, Park.name AS ParkName, Landmark.location AS geometry FROM Landmark, Park WHERE ST_Within(Landmark.location, Park.location);",
        12: "SELECT p.name AS park_name, r.name AS road_name, p.location AS park_geometry, r.location AS road_geometry FROM Park p, Road r WHERE ST_Touches(p.location, r.location);",
        13: "SELECT name, location AS geometry FROM Park WHERE ST_Area(location) > (SELECT AVG(ST_Area(location)) FROM Park);",
        14: """CREATE VIEW RoadsTouchingBuildings AS
                SELECT b.bid AS building_id, b.address AS building_address, r.rid AS road_id, r.name AS road_name,
                    ST_AsText(b.location) AS building_geometry,
                    ST_AsText(r.location) AS road_geometry
                FROM Building b, Road r
                WHERE ST_Touches(b.location, r.location);
                SELECT * FROM RoadsTouchingBuildings;""",
        15: "SELECT Building.address, Building.location AS geometry FROM Building, Park WHERE ST_Disjoint(Building.location, Park.location) AND Park.name = 'Triangle Park';",
        16: "SELECT Park.name, Landmark.name, ST_Intersection(Park.location, Landmark.location) AS intersection_geometry FROM Park, Landmark WHERE ST_Overlaps(Park.location, Landmark.location);"
    }

    return queries.get(choice, "")

# prompt for database connection details
database_name = input("Enter the database name: ")
user_name = input("Enter the user name: ")

# establishing the connection dynamically based on user input
conn = psycopg2.connect(
   database=database_name, 
   user=user_name,
   host='127.0.0.1', 
   port='5432'
)

# create a cursor object
cursor = conn.cursor()
print(f"Successfully connected to the '{database_name}' database!")
conn.autocommit = True

while True:
    # ask the user for input
    choice = input("Do you want to provide a query (enter '1') or select a predefined one (enter '2')? ")

    if choice.lower() == '1':
        query = input("Please enter your SQL query: ")
    elif choice.lower() == '2':
        print("""Choose one of the following queries by number:
    - Non-Spatial Queries Available:
        1. JOIN Query: Find the names of citizens and the buildings they live in.
        2. GROUP BY Query with COUNT: Count how many citizens live in each building.
        3. AVG Query: Calculate the average age of citizens.
        4. MIN Query: Identifies the oldest building(s).
        5. MAX Query: Find the maximum price across all products/services.
        6. Nested Query: Find the names of businesses that have more than the average number of products.
        7. VIEW Creation and Usage: Create a view for the number of employees per business.
              
    - Spatial Queries Available:
        8. Area Calculation: Calculate the area of a park.
        9. Distance Calculation: Calculate the distance between two points of interest.
        10. Intersect Query: Find roads that intersect with parks.
        11. Within Query: Find landmarks within parks.
        12. Touch Query: Find roads that touch parks.
        13. Nested Query: Find parks that are larger than the average size.
        14. VIEW Creation and Usage: Find roads that touch buildings.
        15. Disjoint Query: Find buildings that do not intersect with parks.
        16. Overlap Query: Find parks that overlap landmarks.              
        """)
        query_choice = int(input("Enter the number of the query you want to execute: "))
        query = get_predefined_query(query_choice)
    else:
        print("Invalid choice. Please enter '1' for custom or '2' for predefined.")
        continue

    # execute the query
    try:
        cursor.execute(query)
        if query.startswith("CREATE VIEW"):
            print("View created successfully.")
        else:
            # fetch all results
            results = cursor.fetchall()

            # process the results (example: print them)
            for row in results:
                print(row)
    except Exception as e:
        print(f"An error occurred: {e}")

    # ask if the user wants to continue
    cont = input("Do you want to execute another query? (y/n): ")
    if cont.lower() != 'y':
        print(f"Exiting program..")
        break

# close the cursor and connection
cursor.close()
conn.close()