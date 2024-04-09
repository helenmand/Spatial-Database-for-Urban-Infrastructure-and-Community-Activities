import geopandas as gpd
import re
from matplotlib.lines import Line2D
from shapely import wkt
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

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
    "INSERT INTO Road (rid, name, lanes, type, location) VALUES (5, 'Central Street', 2, 'Local', ST_GeomFromText('LINESTRING(20 75, 30 75)'));",
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

def extract_spatial_data_with_names(queries):
    # regular expression patterns for extracting spatial data and names
    building_pattern = r"INSERT INTO Building .+ VALUES \((\d+), '(.+)', '(.+)', \d+, \d+, ST_GeomFromText\('(.+)'\)\);"
    landmark_pattern = r"INSERT INTO Landmark .+ VALUES \((\d+), '(.+)', '(.+)', .+, .+, ST_GeomFromText\('(.+)'\)\);"
    park_pattern = r"INSERT INTO Park .+ VALUES \((\d+), '(.+)', '(.+)', ST_GeomFromText\('(.+)'\)\);"
    road_pattern = r"INSERT INTO Road .+ VALUES \((\d+), '(.+)', \d+, '(.+)', ST_GeomFromText\('(.+)'\)\);"

    buildings, landmarks, parks, roads = [], [], [], []
    building_names, landmark_names, park_names, road_names = [], [], [], []

    for query in queries:
        
        building_match = re.search(building_pattern, query)
        if building_match:
            buildings.append(wkt.loads(building_match.group(4)))
            building_names.append(building_match.group(2))

        landmark_match = re.search(landmark_pattern, query)
        if landmark_match:
            landmarks.append(wkt.loads(landmark_match.group(4)))
            landmark_names.append(landmark_match.group(3))

        park_match = re.search(park_pattern, query)
        if park_match:
            parks.append(wkt.loads(park_match.group(4)))
            park_names.append(park_match.group(3))

        road_match = re.search(road_pattern, query)
        if road_match:
            roads.append(wkt.loads(road_match.group(4)))
            road_names.append(road_match.group(2))

    gdf_buildings = gpd.GeoDataFrame({'name': building_names, 'geometry': buildings})
    gdf_landmarks = gpd.GeoDataFrame({'name': landmark_names, 'geometry': landmarks})
    gdf_parks = gpd.GeoDataFrame({'name': park_names, 'geometry': parks})
    gdf_roads = gpd.GeoDataFrame({'name': road_names, 'geometry': roads})

    return gdf_buildings, gdf_landmarks, gdf_parks, gdf_roads

def visualize_spatial_data_with_better_road_labels(gdf_buildings, gdf_landmarks, gdf_parks, gdf_roads):
    fig, ax = plt.subplots(figsize=(10, 10))

    # font size
    font_size = 5

    # Grand Central Park with cutouts
    park_main_wkt = 'POLYGON((20 70, 20 80, 80 80, 80 70, 20 70))'
    park_cutouts_wkt = [
        'POLYGON((20 70, 30 75, 20 80, 20 70))',
        'POLYGON((80 70, 70 75, 80 80, 80 70))'
    ]
    park_main = wkt.loads(park_main_wkt)
    park_cutouts = [wkt.loads(shape) for shape in park_cutouts_wkt]
    park_shape = park_main

    for cutout in park_cutouts:
        park_shape = park_shape.difference(cutout)
    
    # southwest Park
    bottom_left_park_coords = [(5, 5), (5, 15), (25, 15), (25, 5)]
    bottom_left_park = Polygon(bottom_left_park_coords)
    
    # GeoDataFrame for parks
    parks_extra_gdf = gpd.GeoDataFrame({
        'name': ['Grand Central Park', 'Southwest Park'],
        'geometry': [park_shape, bottom_left_park]
    })
    
    # central Statue
    statue_point = Point(50, 75).buffer(2)
    statue_gdf = gpd.GeoDataFrame({
        'name': ['Central Statue'],
        'geometry': [statue_point]
    }, geometry='geometry')
    
    gdf_buildings.plot(ax=ax, color="skyblue", label="Buildings", marker="o", markersize=50, alpha=0.6, edgecolor="k")
    gdf_landmarks.plot(ax=ax, color="gold", label="Landmarks", marker="^", markersize=70, alpha=0.7, edgecolor="k")
    gdf_parks.plot(ax=ax, color="lightgreen", label="Parks", marker="s", markersize=50, alpha=0.5, edgecolor="k")
    gdf_roads.plot(ax=ax, color="grey", linewidth=2, label='Roads')

    # plot manually created parks and statue GeoDataFrames with edgecolor
    parks_extra_gdf.plot(ax=ax, color="lightgreen", label="Parks", marker="s", markersize=50, alpha=0.5, edgecolor="k")
    statue_gdf.plot(ax=ax, color="gold", label="Landmarks", marker="^", markersize=70, alpha=0.7, edgecolor="k")
    
    for _, row in parks_extra_gdf.iterrows():
        if row['name'] == 'Grand Central Park':
            # shifting the label to the left by subtracting from the centroid's x-coordinate
            label_x_position = row['geometry'].centroid.x - 10 
            label_y_position = row['geometry'].centroid.y
            ax.text(label_x_position, label_y_position, row['name'],
                    fontsize=font_size, ha='center', va='center', color='green', backgroundcolor='white')
        else:
            # for all other parks and the statue, use the centroid's position
            ax.text(row['geometry'].centroid.x, row['geometry'].centroid.y, row['name'],
                    fontsize=font_size, ha='center', va='center', color='green', backgroundcolor='white')

    for _, row in statue_gdf.iterrows():
        ax.text(row['geometry'].centroid.x, row['geometry'].centroid.y, row['name'],
                fontsize=font_size, ha='center', va='center', color='darkgoldenrod', backgroundcolor='white')

    # adding road names in the middle of each road line
    for _, row in gdf_roads.iterrows():
        if row['name'] == 'East-West Boulevard':
            # check if the geometry is not simple
            if not row['geometry'].is_simple:
                midpoint = row['geometry'].representative_point()
            else:
                # otherwise, interpolate to get the middle point
                midpoint = row['geometry'].interpolate(0.5, normalized=True)
            # adjust the y-position to be slightly lower for "East West Boulevard"
            adjusted_midpoint_y = midpoint.y - 2 
            ax.text(midpoint.x, adjusted_midpoint_y, row['name'], fontsize=font_size, ha='center', va='center', backgroundcolor='white')
        else:
            # for all other roads, use the original code to place the name
            if not row['geometry'].is_simple:
                midpoint = row['geometry'].representative_point()
            else:
                # otherwise, interpolate to get the middle point
                midpoint = row['geometry'].interpolate(0.5, normalized=True)
            ax.text(midpoint.x, midpoint.y, row['name'], fontsize=font_size, ha='center', va='center', backgroundcolor='white')

    # adding name labels for buildings, landmarks, and parks in their centroid
    for _, row in gdf_buildings.iterrows():
        ax.text(row['geometry'].centroid.x, row['geometry'].centroid.y, row['name'],
                fontsize=font_size, ha='center', va='center', color='blue', backgroundcolor='white')
    for _, row in gdf_landmarks.iterrows():
        ax.text(row['geometry'].centroid.x, row['geometry'].centroid.y, row['name'],
                fontsize=font_size, ha='center', va='center', color='darkgoldenrod', backgroundcolor='white')
    for _, row in gdf_parks.iterrows():
        if row['name'] == 'Triangle Park':
            # adjust the y-position to be slightly lower for "Triangle Park"
            adjusted_centroid_y = row['geometry'].centroid.y - 2  
            ax.text(row['geometry'].centroid.x, adjusted_centroid_y, row['name'],
                    fontsize=font_size, ha='center', va='center', color='green', backgroundcolor='white')
        else:
            # for all other parks, use the original centroid position
            ax.text(row['geometry'].centroid.x, row['geometry'].centroid.y, row['name'],
                    fontsize=font_size, ha='center', va='center', color='green', backgroundcolor='white')
            
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Building', markerfacecolor='skyblue', markersize=15),
        Line2D([0], [0], marker='^', color='w', label='Landmark', markerfacecolor='gold', markersize=15),
        Line2D([0], [0], marker='s', color='w', label='Park', markerfacecolor='lightgreen', markersize=15),
        Line2D([0], [0], color='grey', lw=2, label='Road')
    ]

    # legend
    ax.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.show()

# get geodataframes
gdf_buildings, gdf_landmarks, gdf_parks, gdf_roads = extract_spatial_data_with_names(insert_queries)
# plot
visualize_spatial_data_with_better_road_labels(gdf_buildings, gdf_landmarks, gdf_parks, gdf_roads)