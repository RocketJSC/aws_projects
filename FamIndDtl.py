import linecache

def insert_faminddtl(Customer_Id, conn, data):
    insert_query = "INSERT INTO FamIndDtl (CustomerId, FamilyId, IndividualId, Position) VALUES (%s, %s, %s, %s)"
    cursor = conn.cursor()
    cursor.execute(insert_query, data)
    conn.commit()
    cursor.close()


def load_faminddtl(Customer_Id, conn, file_path, linenumber, family_id):

    famind_dict = {'family_id' : family_id,
                   'individual_id' : '',
                   'position': ''}
    line = linecache.getline(file_path, linenumber)

    while line and  line[0] != '0':
        line = line.strip()
        if line[0:6] in ['1 HUSB', '1 WIFE', '1 CHIL']:
           individual_split = line.split('@')
           famind_dict['individual_id'] = individual_split[1].rstrip()
           famind_dict['position'] = line[2:6]
           data = [Customer_Id, 
                   famind_dict['family_id'], 
                   famind_dict['individual_id'], 
                   famind_dict['position']]
           insert_faminddtl(Customer_Id, conn, data)
           linenumber += 1
           line = linecache.getline(file_path, linenumber)
           line = line.strip()
           while line[0] == '2':
              if '_FREL adopted' in line:
                 cursor = conn.cursor()
                 update_query = "UPDATE FamIndDtl SET FAdopted = %s WHERE CustomerId = %s and FamilyId = %s and IndividualId = %s"
                 cursor.execute(update_query, ('Y', Customer_Id, famind_dict['family_id'], famind_dict['individual_id']))
#                 print(cursor.statement)
                 conn.commit()
                 cursor.close()
                 linenumber += 1
                 line = linecache.getline(file_path, linenumber)
              elif '_MREL adopted' in line:
                 cursor = conn.cursor()
                 update_query = "UPDATE FamIndDtl SET MAdopted = %s WHERE CustomerId = %s and FamilyId = %s and IndividualId = %s"
                 cursor.execute(update_query, ('Y', Customer_Id, famind_dict['family_id'], famind_dict['individual_id']))
#                 print(cursor.statement)
                 conn.commit()
                 cursor.close()
                 linenumber += 1
                 line = linecache.getline(file_path, linenumber)
              elif '_FREL step' in line:
                 cursor = conn.cursor()
                 update_query = "UPDATE FamIndDtl SET FStep = %s WHERE CustomerId = %s and FamilyId = %s and IndividualId = %s"
                 cursor.execute(update_query, ('Y', Customer_Id, famind_dict['family_id'], famind_dict['individual_id']))
#                print(cursor.statement)
                 conn.commit()
                 cursor.close()
                 linenumber += 1
                 line = linecache.getline(file_path, linenumber)
              elif '_MREL step' in line:
                 cursor = conn.cursor()
                 update_query = "UPDATE FamIndDtl SET MStep = %s WHERE CustomerId = %s and FamilyId = %s and IndividualId = %s"
                 cursor.execute(update_query, ('Y', Customer_Id, famind_dict['family_id'], famind_dict['individual_id']))
#                 print(cursor.statement)
                 conn.commit()
                 cursor.close()
                 linenumber += 1
                 line = linecache.getline(file_path, linenumber)
              else:
                 linenumber += 1
                 line = linecache.getline(file_path, linenumber)
        else:
           return linenumber

    return linenumber
