import linecache
import sys
import Utilities

def load_individualmaster(Customer_Id, conn, file_path, linenumber):

    individual_dict = {'individual_id' : '',
                       'individual_name': '',
                       'individual_surname': '',
                       'individual_givenname': '',
                       'individual_suffix': '',
                       'gender': '',
                       'birthdate': '',
                       'deathdate': '',
                       'findagrave_url': '',
                       'obit_url': '',
                       'census_array': '',
                       'tag_array': ''}

    census_list = []

    line = linecache.getline(file_path, linenumber)

    individualid_split = line.split('@')
    individual_dict['individual_id'] = individualid_split[1].rstrip()

#   Utilities.get_FAG_page(Customer_Id, conn, individual_dict['individual_id'])

    linenumber += 1
    line = linecache.getline(file_path, linenumber)
    while line and  line[0] != '0':
        line = line.strip()
        if line[0:6] == '1 NAME':
           individual_dict['individual_name'] = line[7:]
           linenumber += 1
           line = linecache.getline(file_path, linenumber)
        elif line[0:6] == '1 BIRT':
           linenumber += 1
           line = linecache.getline(file_path, linenumber).rstrip()
           individual_dict['birthdate'] = Utilities.date_parser(line[7:])
           linenumber += 1
           line = linecache.getline(file_path, linenumber)
        elif line[0:6] == '1 DEAT':
           linenumber += 1
           line = linecache.getline(file_path, linenumber).rstrip()
           individual_dict['deathdate'] = Utilities.date_parser(line[7:])
           linenumber += 1
           line = linecache.getline(file_path, linenumber)
        elif line[0:5] == '1 SEX':
           individual_dict['gender'] = line[6:]
           linenumber += 1
           line = linecache.getline(file_path, linenumber)
        elif line[0:6] == '1 OBJE':
           object_split = line.split('@')
           object_id = object_split[1].rstrip()
           select_query = "SELECT * FROM ObjectMaster WHERE CustomerID = %s AND ObjectId = %s"
           cursor = conn.cursor()
           data = [Customer_Id, object_id]
           cursor.execute(select_query, data)
           row = cursor.fetchone()
           if row:
              if row[2] == "FAG":
                 individual_dict['findagrave_url'] = row[3]
              elif row[2] == "Obit":
                 individual_dict['obit_url'] = row[3]
           linenumber += 1
           line = linecache.getline(file_path, linenumber)
        elif line[0:8] == '1 _MTTAG':
           tag_split = line.split('@')
           tag_id = tag_split[1].rstrip()
           individual_dict['tag_array'] += tag_id + ' '
           linenumber += 1
           line = linecache.getline(file_path, linenumber)
        elif line[0:6] == '2 GIVN':
           individual_dict['individual_givenname'] = line[7:]
           linenumber += 1
           line = linecache.getline(file_path, linenumber)
        elif line[0:6] == '2 SURN':
           individual_dict['individual_surname'] = line[7:]
           linenumber += 1
           line = linecache.getline(file_path, linenumber)
        elif line[0:6] == '2 NSFX':
           individual_dict['individual_suffix'] = line[7:]
           linenumber += 1
           line = linecache.getline(file_path, linenumber)
        elif line[0:6] == '2 NOTE' and 'findagrave.com' in line.lower():
           individual_dict['findagrave_url'] = line[7:]
           linenumber += 1
           line = linecache.getline(file_path, linenumber)
        elif line[0:12] in ('2 PAGE Year:','3 PAGE Year:') and 'Census' in line:
           census_list.append(line[13:17] + ' ')
           linenumber += 1
           line = linecache.getline(file_path, linenumber)
        elif line[0:6] == '2 SOUR':
           source_split = line.split('@')
           if len(source_split) >= 2:
              source_id = source_split[1].rstrip()
              select_query = "SELECT * FROM SourceMaster WHERE CustomerID = %s AND SourceId = %s"
              cursor = conn.cursor()
              data = [Customer_Id, source_id]
              cursor.execute(select_query, data)
              row = cursor.fetchone()
              if row:
                 if 'United States Federal Census' in row[2]:
                    census_list.append(row[2][0:4] + ' ')
           linenumber += 1
           line = linecache.getline(file_path, linenumber)
        elif ('3 PAGE United' in line) and ('Bureau of the Census' in line) and ('1950' in line):
           census_list.append('1950' + ' ')
           linenumber += 1
           line = linecache.getline(file_path, linenumber)
        elif line[0:5] == '4 WWW' and 'findagrave.com' in line.lower():
           individual_dict['findagrave_url'] = line[6:]
           linenumber += 1
           line = linecache.getline(file_path, linenumber)
        else:
           linenumber += 1
           line = linecache.getline(file_path, linenumber)

    individual_dict['census_array'] = ''.join(sorted(set(census_list)))

# load IndividualMaster
    insert_query = "INSERT INTO IndividualMaster (CustomerId, IndividualId, IndividualName, IndividualSurname, " + \
                   "IndividualGivenname, IndividualSuffix, Gender, BirthDate, DeathDate, ObitURL, FindAGraveURL, CensusFlags, TagIds) VALUES " + \
                   "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor = conn.cursor()
    data = [Customer_Id, 
            individual_dict['individual_id'], 
            individual_dict['individual_name'], 
            individual_dict['individual_surname'],
            individual_dict['individual_givenname'],
            individual_dict['individual_suffix'],
            individual_dict['gender'],
            individual_dict['birthdate'],
            individual_dict['deathdate'],
            individual_dict['obit_url'],
            individual_dict['findagrave_url'],
            individual_dict['census_array'],
            individual_dict['tag_array']]

    cursor.execute(insert_query, data)
    conn.commit()
    cursor.close()

    return linenumber
