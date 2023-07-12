import linecache
import FamIndDtl
import Utilities

def load_familymaster(Customer_Id, conn, file_path, linenumber):

    family_dict = {'family_id' : '',
                   'marr_date': '',
                   'div_date': ''}
    line = linecache.getline(file_path, linenumber)

    family_split = line.split('@')
    family_dict['family_id'] = family_split[1].rstrip()

# load FamilyMaster
    insert_query = "INSERT INTO FamilyMaster (CustomerId, FamilyId) VALUES (%s, %s)"
    cursor = conn.cursor()
    data = [Customer_Id, 
            family_dict['family_id']]
    cursor.execute(insert_query, data)
    conn.commit()
    cursor.close()

    linenumber += 1
    line = linecache.getline(file_path, linenumber)
    while line and  line[0] != '0':
        line = line.strip()
        if line[0:6] == '1 MARR':
           linenumber += 1
           line = linecache.getline(file_path, linenumber).rstrip()
           family_dict['marr_date'] = Utilities.date_parser(line[7:])
           cursor = conn.cursor()
           update_query = "UPDATE FamilyMaster SET MarrDate = %s WHERE CustomerId = %s and FamilyId = %s"
           cursor.execute(update_query, (family_dict['marr_date'], Customer_Id, family_dict['family_id']))
 #         print(cursor.statement)
           conn.commit()
           cursor.close()
           linenumber += 1
           line = linecache.getline(file_path, linenumber)
        elif line[0:5] == '1 DIV':
           linenumber += 1
           line = linecache.getline(file_path, linenumber).rstrip()
           family_dict['div_date'] = Utilities.date_parser(line[7:])
           update_query = "UPDATE FamilyMaster  SET DivDate = %s WHERE CustomerId = %s and FamilyId = %s"
           cursor = conn.cursor()
           cursor.execute(update_query, (family_dict['div_date'], Customer_Id, family_dict['family_id']))
#          print(cursor.statement)
           conn.commit()
           cursor.close()
           linenumber += 1
           line = linecache.getline(file_path, linenumber)
        elif line[0:6] in ['1 HUSB', '1 WIFE', '1 CHIL']:
# Load FamIndDtl
           linenumber = FamIndDtl.load_faminddtl(Customer_Id, conn, file_path, linenumber, family_dict['family_id'])
           line = linecache.getline(file_path, linenumber)
        else:
           linenumber += 1
           line = linecache.getline(file_path, linenumber)

    return linenumber
