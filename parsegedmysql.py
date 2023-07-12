# imported libraries
from collections import OrderedDict
import mysql.connector
import sys
import TagMaster
import FamilyMaster
import IndividualMaster
import Utilities
import linecache

if len(sys.argv) < 2:
    raise ValueError('usage: CustomerId')

Customer_Id = sys.argv[1]
file_path = "Lindahl_Cooper_Ralston_Family.ged"

# configure mysql database connection
db_host = 'gedcom-database1.c0kyhj1ysfg1.us-east-1.rds.amazonaws.com'
db_port = 3306
db_user = 'admin'
db_password = 'Wolves83%%'
db_database = 'gedcomdb'

# connect to mysql database
try:
    conn = mysql.connector.connect(host=db_host, port=db_port, user=db_user, password=db_password, database=db_database)

    if conn.is_connected():
        print('Connected to the MySQL database')

except mysql.connector.Error as e:
    print('Error connecting to the MySQL database:', e)

# erase tables for Customer_Id
cursor = conn.cursor()
delete_command = "DELETE FROM FamIndDtl WHERE CustomerId = '" + Customer_Id + "'"
print(delete_command)
cursor.execute(delete_command)
cursor.close()

cursor = conn.cursor()
delete_command = "DELETE FROM IndividualMaster WHERE CustomerId = '" + Customer_Id + "'"
print(delete_command)
cursor.execute(delete_command)
cursor.close()

cursor = conn.cursor()
delete_command = "DELETE FROM FamilyMaster WHERE CustomerId = '" + Customer_Id + "'"
print(delete_command)
cursor.execute(delete_command)
cursor.close()

cursor = conn.cursor()
delete_command = "DELETE FROM TagMaster WHERE CustomerId = '" + Customer_Id + "'"
print(delete_command)
cursor.execute(delete_command)
cursor.close()

cursor = conn.cursor()
delete_command = "DELETE FROM ObjectMaster WHERE CustomerId = '" + Customer_Id + "'"
print(delete_command)
cursor.execute(delete_command)
cursor.close()

cursor = conn.cursor()
delete_command = "DELETE FROM SourceMaster WHERE CustomerId = '" + Customer_Id + "'"
print(delete_command)
cursor.execute(delete_command)
cursor.close()
print('Deleted all records')


# initialize record type collection
record_type = {
    'HEAD': 0,
    'SUBM': 0,
    'INDI': 0,
    'FAM': 0,
    'MTTAG': 0,
    'Total': 0
}


# Load ObjectMaster and TagMaster tables
Utilities.load_miscfiles(Customer_Id, conn, file_path)
print('Loaded Misc Tables')

print('Load IndividualMaster, FamilyMaster, FamIndDtl Tables')

# open the file
file_path = "Lindahl_Cooper_Ralston_Family.ged"
try:
    file = open(file_path,'r')
except IOError:
    print('Error opening file')

# Loop thru file
linenumber = 1
line = linecache.getline(file_path,linenumber)
while line:
    line = linecache.getline(file_path,linenumber)
    line = line.strip()
    if line[0] == "0":
       if "@ HEAD" in line:
          record_type['HEAD'] += 1
          linenumber += 1
          line = linecache.getline(file_path, linenumber)
       elif "@ SUBM" in line:
          record_type['SUBM'] += 1
          linenumber += 1
          line = linecache.getline(file_path, linenumber)
       elif "@ INDI" in line:
          record_type['INDI'] += 1
          linenumber = IndividualMaster.load_individualmaster(Customer_Id, conn, file_path, linenumber)
       elif "@ FAM" in line:
          record_type['FAM'] += 1
          linenumber = FamilyMaster.load_familymaster(Customer_Id, conn, file_path, linenumber)
#       elif "@ _MTTAG" in line:
#          record_type['MTTAG'] += 1
#          linenumber = TagMaster.load_tagmaster(Customer_Id, conn, file_path, linenumber)
       else:
          linenumber += 1
          line = linecache.getline(file_path, linenumber)
    else:
       linenumber += 1
       line = linecache.getline(file_path, linenumber)

    record_type['Total'] += 1

# print record totals
print('Individuals %6d' % (record_type['INDI']))
print('Families    %6d' % (record_type['FAM']))
print('Total Recs  %6d' % (record_type['Total']))

# Close the database connection
if conn and conn.is_connected():
   conn.close()
   print('Connection to the MySQL database closed')

# close gedcom file
file.close()
