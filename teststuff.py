__author__ = 'Afzal Syed'

#def insertIntoTable(table,**kwargs):
#    print "table is", table
    # INSERT INTO standings (player_id, matches, wins, losses, netscore ) VALUES  (%s, %s, %s, %s, %s)", (winner, l_matches, l_wins, l_loses, l_netscore))
    # "INSERT INTO table (key1, key2) VALUES (%s, %s)", (value1, value2,))
 #   string = "insert into table "
    #cursor.execute("INSERT INTO players (name) VALUES  (%s)", (name,))
    #DB.commit()
    #DB.close()


def runQuery(sql, commit=None, rtype=None):
    print sql, commit, rtype
    if commit:
        print "going to commit"
    else:
        print "not going to commit"



runQuery("test cmd", None, "int")