from tstpydb import tstpydb

'''
USAGE EXAMPLES
'''

db = tstpydb.tstPyDb('_sqlite','user.db')

'''
INSERT INTO Users (Id,Name) VALUES ("5","William")
'''
#db.table('Users').insert({"Id":"5","Name":"William"})

'''
UPDATE Users SET Id = 4 WHERE Name = 'Jeremy'
'''
#db.table('Users').update({"Id":"1"}).where('Name','=','Michelle')

'''
SELECT * FROM Usera WHERE Id != 3 AND Name != 'Sonya'
'''
#c = db.table('Users').where('Id','!=','3').where('Name','!=','Sonya').get()


'''
SELECT * FROM Users
'''
c = db.table('Users').get()
for row in c:
    print('row = %r' % (row,))

print("_________________________________")

