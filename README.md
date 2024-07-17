# Spatial Database for Urban Infrastructure and Community Activities
This project involves designing and implementing a spatial database to model city interactions between businesses and citizens. 

## Installation

1. Ensure you have PostgreSQL and PostGIS installed.
2. Install Python and psycopg2 library if not already installed:
   ```bash
   pip install psycopg2
   ```

## Usage

1. Clone the repository.
2. Run the provided Python script to set up the database:
  ```bash
   python setup_database.py
   ```

## Database Schema

- Building: Stores information about buildings in the city.
- Citizen: Contains details about the citizens.
- Business: Includes data about businesses operating in the city.
- ProductService: Lists products and services offered by businesses.
- Park: Represents parks in the city.
- Road: Details about roads in the city.
- Landmark: Information about landmarks.
- Happening: Events or happenings within the city.
- Employment: Relates citizens to businesses for employment data.
- RoadLeadsToPark, RoadLeadsToLandmark, RoadLeadsToBuilding: Relationships between roads and other entities.
- Sponsorship: Links businesses to events they sponsor.

## Predefined Queries

The `execute_queries.py` script allows users to execute predefined queries or custom SQL queries. 
The predefined queries are as follows:

### Non-Spatial Queries

1. **JOIN Query**: Find the names of citizens and the buildings they live in.
    ```sql
    SELECT Citizen.first_name, Citizen.last_name, Building.address 
    FROM Citizen 
    JOIN Building ON Citizen.livesIn = Building.bid;
    ```

2. **GROUP BY Query with COUNT**: Count how many citizens live in each building.
    ```sql
    SELECT Building.address, COUNT(Citizen.cid) AS num_of_citizens 
    FROM Citizen 
    JOIN Building ON Citizen.livesIn = Building.bid 
    GROUP BY Building.bid;
    ```

3. **AVG Query**: Calculate the average age of citizens.
    ```sql
    SELECT AVG(age) AS average_age 
    FROM Citizen;
    ```

4. **MIN Query**: Identifies the oldest building(s).
    ```sql
    SELECT address, constructionYear 
    FROM Building 
    WHERE constructionYear = (SELECT MIN(constructionYear) FROM Building);
    ```

5. **MAX Query**: Find the maximum price across all products/services.
    ```sql
    SELECT Business.name, ProductService.price AS max_price 
    FROM Business 
    JOIN ProductService ON Business.buid = ProductService.offeredByBusiness 
    WHERE ProductService.price = (SELECT MAX(price) FROM ProductService);
    ```

6. **Nested Query**: Find the names of businesses that have more than the average number of products.
    ```sql
    SELECT name 
    FROM Business 
    WHERE buid IN (
        SELECT offeredByBusiness 
        FROM ProductService 
        GROUP BY offeredByBusiness 
        HAVING COUNT(prid) > (
            SELECT AVG(count) 
            FROM (
                SELECT COUNT(prid) AS count 
                FROM ProductService 
                GROUP BY offeredByBusiness
            ) AS average_products
        )
    );
    ```

7. **VIEW Creation and Usage**: Create a view for the number of employees per business.
    ```sql
    CREATE VIEW BusinessEmployeeCount AS 
    SELECT Business.buid, Business.name, COUNT(Employment.cid) AS num_of_employees 
    FROM Business 
    JOIN Employment ON Business.buid = Employment.buid 
    GROUP BY Business.buid;

    SELECT name, num_of_employees 
    FROM BusinessEmployeeCount 
    WHERE num_of_employees > 0;
    ```

### Spatial Queries

8. **Area Calculation**: Calculate the area of a park.
    ```sql
    SELECT pid, ST_Area(location) AS area, location AS geometry 
    FROM Park 
    WHERE name = 'Grand Central Park';
    ```

9. **Distance Calculation**: Calculate the distance between two points of interest.
    ```sql
    SELECT Landmark.name, Park.name, ST_Distance(Landmark.location, Park.location) AS distance, 
           Landmark.location AS landmark_geometry, Park.location AS park_geometry 
    FROM Landmark, Park 
    WHERE Landmark.name = 'Expanded City Museum' AND Park.name = 'Grand Central Park';
    ```

10. **Intersect Query**: Find roads that intersect with parks.
    ```sql
    SELECT r.name AS road_name, p.name AS park_name, ST_AsText(r.location) AS road_geometry, 
           ST_AsText(p.location) AS park_geometry 
    FROM Road r, Park p 
    WHERE ST_Intersects(r.location, p.location);
    ```

11. **Within Query**: Find landmarks within parks.
    ```sql
    SELECT Landmark.name AS LandmarkName, Park.name AS ParkName, Landmark.location AS geometry 
    FROM Landmark, Park 
    WHERE ST_Within(Landmark.location, Park.location);
    ```

12. **Touch Query**: Find roads that touch parks.
    ```sql
    SELECT p.name AS park_name, r.name AS road_name, p.location AS park_geometry, 
           r.location AS road_geometry 
    FROM Park p, Road r 
    WHERE ST_Touches(p.location, r.location);
    ```

13. **Nested Query**: Find parks that are larger than the average size.
    ```sql
    SELECT name, location AS geometry 
    FROM Park 
    WHERE ST_Area(location) > (SELECT AVG(ST_Area(location)) FROM Park);
    ```

14. **VIEW Creation and Usage**: Find roads that touch buildings.
    ```sql
    CREATE VIEW RoadsTouchingBuildings AS
    SELECT b.bid AS building_id, b.address AS building_address, r.rid AS road_id, r.name AS road_name,
           ST_AsText(b.location) AS building_geometry,
           ST_AsText(r.location) AS road_geometry
    FROM Building b, Road r
    WHERE ST_Touches(b.location, r.location);

    SELECT * FROM RoadsTouchingBuildings;
    ```

15. **Disjoint Query**: Find buildings that do not intersect with parks.
    ```sql
    SELECT Building.address, Building.location AS geometry 
    FROM Building, Park 
    WHERE ST_Disjoint(Building.location, Park.location) AND Park.name = 'Triangle Park';
    ```

16. **Overlap Query**: Find parks that overlap landmarks.
    ```sql
    SELECT Park.name, Landmark.name, ST_Intersection(Park.location, Landmark.location) AS intersection_geometry 
    FROM Park, Landmark 
    WHERE ST_Overlaps(Park.location, Landmark.location);
    ```
