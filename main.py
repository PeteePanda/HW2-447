from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

@app.route('/enternew')
def new_student():
   return render_template('student.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         id = request.form['id']
         scr = request.form['scr']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO students (name,ident,score) VALUES (?,?,?)",(nm,id,scr) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         con = sql.connect("database.db")
         con.row_factory = sql.Row

         cur = con.cursor()
         cur.execute("select * from students")
   
         rows = cur.fetchall()
         con.close()
         return render_template("result.html",msg = msg, rows = rows)

@app.route('/delete')
def delete():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall()
   con.close()
   return render_template('deletestudent.html',rows = rows)

@app.route('/delrec', methods = ['POST', 'GET'])
def delrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         id = request.form['id']

         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT name,ident FROM students WHERE name=? AND ident=?",(nm,id))
            if cur.fetchone():
               cur.execute("DELETE FROM students WHERE name=? AND ident=?",(nm,id))
         
               con.commit()
               msg = 'Record Successfully Deleted'
            else:
               con.rollback()
               msg = 'invalid name or id'
      except:
         con.rollback()
         msg = 'Error deletion operation'
      finally:
         con = sql.connect("database.db")
         con.row_factory = sql.Row

         cur = con.cursor()
         cur.execute("select * from students")
   
         rows = cur.fetchall()
         con.close()
         return render_template('result.html', msg = msg, rows = rows)


@app.route('/search')
def search():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall()
   con.close()
   return render_template('search.html', rows=rows)

@app.route('/searchrec', methods = ['POST', 'GET'])
def searchrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         id = request.form['id']
         scr = request.form['scr']
         
         con = sql.connect("database.db")
         con.row_factory = sql.Row

         cur = con.cursor()
         cur.execute("SELECT * FROM students WHERE name = ? OR ident = ? OR score = ?",(nm,id,scr)) 
         
         rows = cur.fetchall()
         msg = "Record successfully searched"
      except:
         con = sql.connect("database.db")
         con.row_factory = sql.Row

         cur = con.cursor()
         cur.execute("select * from students")

         rows = cur.fetchall()
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         con.close()
         return render_template("result.html",msg = msg, rows = rows)

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall(); 
   con.close()
   return render_template("list.html",rows = rows)

@app.route('/')
def home():
   return render_template('home.html')

if __name__ == '__main__':
   conn = sql.connect('database.db')
   print ("Opened database successfully")

   conn.execute('CREATE TABLE IF NOT EXISTS students (name TEXT, ident INTEGER, score INTEGER)')
   print ("Table created successfully")
   conn.close()
   app.run(debug = True)