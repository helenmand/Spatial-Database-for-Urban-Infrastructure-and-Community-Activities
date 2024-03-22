import psycopg2

#Establishing the connection
conn = psycopg2.connect(
   database="demodb", 
   user='elenimandana',
   host='127.0.0.1', 
   port= '5432'
)

# Create a cursor object
cursor = conn.cursor()
conn.autocommit = True

# Create the EMPLOYEE table if it doesn't exist
create_table_query = '''
CREATE TABLE EMPLOYEE (
    FIRST_NAME VARCHAR(50),
    LAST_NAME VARCHAR(50),
    AGE INT,
    SEX CHAR(1)
);
'''

cursor.execute(create_table_query)
conn.commit()

# Insert data into the EMPLOYEE table
insert_query = '''
INSERT INTO EMPLOYEE (FIRST_NAME, LAST_NAME, AGE, SEX)
VALUES (%s, %s, %s, %s);
'''

data = ('Shikhar', 'Dhawan', 33, 'M')
cursor.execute(insert_query, data)
conn.commit()

# Close cursor and connection
cursor.close()
conn.close()
