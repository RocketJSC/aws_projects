import sys
from dateutil.parser import parse
import re
import requests

# Not being used right now
def get_FAG_page(Customer_Id, conn, individual_id):
    select_query = "SELECT * FROM ObjectMaster WHERE CustomerID = %s AND ObjectId = %s"
    cursor = conn.cursor()
    data = [Customer_Id, 'O0']
    cursor.execute(select_query, data)
    row = cursor.fetchone()
    cursor.close()

    url = 'https://www.ancestry.com/family-tree/person/tree/' + row[3] + '/person/' + individual_id[1:] + '/facts'
    response = requests.get(url)
    if response.status_code == 200:
       with open('webpage.html','w') as file:
            file.write(response.text)
    else:
       print('Failed to get ' + url)
    

def date_parser(date_value):
    return_date = ''
    try:
       return_date = parse(date_value)
    except ValueError:
       return_date = 'v ' + date_value
    except TypeError:
       return_date = 't ' + date_value
    return return_date

def load_miscfiles(Customer_Id, conn, file_path):

    with open(file_path, "r") as file:
         for line in file:
             if line[0:7] == '2 _TREE':
                line = file.readline()
                if '3 RIN' in  line:
                   tree_id = line[6:].rstrip()
                   insert_query = "INSERT INTO ObjectMaster (CustomerId, ObjectId, ObjectType, ObjectValue) VALUES (%s, %s, %s, %s)"
                   data = (Customer_Id, 'O0', 'RIN', tree_id)
                   cursor = conn.cursor()
                   cursor.execute(insert_query, data)
                   conn.commit()
                   cursor.close()
                line = file.readline()
             elif line[0:1] == "0" and "OBJE" in line:
                object_split = line.split("@")
                object_id = object_split[1].rstrip()
                line = file.readline()
                while line:
                      if "1 _ATL" in line:
                         break
                      elif line[0:6] == "2 _URL":
                           object_value = line[7:].rstrip()
                           if "findagrave" in line:
                              object_type = "FAG"
                           elif "fold3" in line:
                              object_type = "FOLD3"
                           else:
                              object_type = "Obit"
                           insert_query = "INSERT INTO ObjectMaster (CustomerId, ObjectId, ObjectType, ObjectValue) VALUES (%s, %s, %s, %s)"
                           cursor = conn.cursor()
                           data = (Customer_Id, object_id, object_type, object_value)
                           cursor.execute(insert_query, data)
                           conn.commit()
                           cursor.close()
                      elif 'Find A Grave Memorial# ' in line:
                           match = re.search(r'w+', line)
                           if match:
                              object_type = "FAG"
                              object_value = "https://www.findagrave.com/memorial/" + match.group()
                              insert_query = "INSERT INTO ObjectMaster (CustomerId, ObjectId, ObjectType, ObjectValue) VALUES (%s, %s, %s, %s)"
                              cursor = conn.cursor()
                              data = (Customer_Id, object_id, object_type, object_value)
                              cursor.execute(insert_query, data)
                              conn.commit()
                              cursor.close()
                           
                      line = file.readline()
                
             elif line[0:1] == "0" and "_MTTAG" in line:
                  tag_split = line.split('@')
                  tag_id = tag_split[1].rstrip()
                  line = file.readline()
                  line = line.strip() 
                  tag_desc = line[6:]
                  insert_query = "INSERT INTO TagMaster (CustomerId, TagId, TagDesc) VALUES (%s, %s, %s)"
                  cursor = conn.cursor()
                  data = (Customer_Id, tag_id, tag_desc)
                  cursor.execute(insert_query, data)
                  conn.commit()
                  cursor.close()
             elif line[0:1] == "0" and "SOUR" in line:
                  source_split = line.split('@')
                  source_id = source_split[1].rstrip()
                  line = file.readline()
                  line = line.strip()
                  source_desc = line[7:]
                  insert_query = "INSERT INTO SourceMaster (CustomerId, SourceId, SourceDesc) VALUES (%s, %s, %s)"
                  cursor = conn.cursor()
                  data = (Customer_Id, source_id, source_desc)
                  cursor.execute(insert_query, data)
                  conn.commit()
                  cursor.close()

