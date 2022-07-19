import sqlite3


def readFlatFile(fileName):
    with open(fileName, 'r') as f:
        print(f.read())
        f.seek(0)
        records = []
        for line in f.readlines()[1:]:
            roll_no = line[0:11].strip()
            name = line[10:61].strip()
            c_marks = eval(line[60:71].strip())
            cpp_marks = eval(line[70:81].strip())
            py_marks = eval(line[80:91].strip())
            records.append([roll_no, name, c_marks, cpp_marks, py_marks])
        print(records)
        return records


def insertToDB(records):
    con = sqlite3.connect('DataBase.db')
    print('Connected To Database Successfully')
    cur = con.cursor()

    query = '''
     DROP TABLE IF EXISTS MARKS;
    CREATE TABLE MARKS (
                ID         TEXT PRIMARY KEY,
                NAME       TEXT   NOT NULL,
                C_MARKS    REAL   NOT NULL,
                CPP_MARKS  REAL   NOT NULL,
                PY_MARKS   REAL   NOT NULL
                );
    '''
    cur.executescript(query)
    print('Table created successfully')

    query = '''INSERT INTO MARKS VALUES ('{}','{}',{},{},{})'''
    try:
        for record in records:
            cur.execute(query.format(*record))
        print('Values inserted successfully')
    except Exception as e:
        print(e)

    con.commit()
    con.close()


'''
Some Basic Queries: 
select * from marks where C_MARKS = (select max(c_marks) from marks);
select * from marks where CPP_MARKS = (select max(cpp_marks) from marks);
select * from marks where PY_MARKS = (select max(PY_marks) from marks);

select avg(C_MARKS) from marks;
select avg(CPP_MARKS) from marks;
select avg(PY_MARKS) from marks;
'''


if __name__ == '__main__':
    data = readFlatFile('FlatFile.txt')
    insertToDB(data)
