import sys
import linecache

def load_tagmaster(Customer_Id, conn, file_path, linenumber):

    line = linecache.getline(file_path, linenumber)

    tag_split = line.split('@')
    tag_id = tag_split[1].rstrip()
    linenumber += 1
    line = linecache.getline(file_path, linenumber)
    line = line.strip() 
    tag_desc = line[6:]
    linenumber += 1
    line = linecache.getline(file_path, linenumber)
    
# load tags to TagMaster
    insert_query = "INSERT INTO TagMaster (CustomerId, TagId, TagDesc) VALUES (%s, %s, %s)"
    cursor = conn.cursor()
    data = (Customer_Id, tag_id, tag_desc)
    cursor.execute(insert_query, data)
    conn.commit()
    cursor.close()

    return linenumber
