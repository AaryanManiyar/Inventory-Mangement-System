import sqlite3

def create_db():
    con = sqlite3.connect(database= r'IMS.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS EMP(emp_id INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,doj text,password text,utype text,address text,salary text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS SUP(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,desc text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS CAT(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS PRO(pid INTEGER PRIMARY KEY AUTOINCREMENT,Supplier text,Category text,Name text,Price text,QTY text,Status text)")
    con.commit()


create_db()     