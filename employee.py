from tkinter import  *
from PIL import Image,ImageTk
from tkinter import ttk, messagebox
import sqlite3

class employeeClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed by Aaryan")
        self.root.config(bg="White")
        self.root.focus_force()

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_emp_id = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_password = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()

        #Search Bar for Searchby Option

        SearchFrame = LabelFrame(self.root, text="Search Employee", bg="white",font=("times new roman",12,"bold"),bd=2,relief=RIDGE)
        SearchFrame.place(x=250,y=20,width=600,height=70)

        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Search","Email_ID","Name","Contact","Gender"),state='readonly',justify=CENTER,font=("times new roman",12,"bold"))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame,textvariable=self.var_searchtxt,font=("times new roman",15,"bold"),bg="lightyellow").place(x=200,y=10)
        btn_search = Button(SearchFrame,text="Search",command=self.search,font=("times new roman",15,"bold"),bg="red",fg="black",cursor="hand2").place(x=410,y=10,width=150,height=30)

        #Title

        title = Label(self.root, text="Employee Details", font=("times new roman",15),bg="#0f4d7d",fg="white").place(x=50,y=100,width=1000)

        #Row1

        lbl_empid = Label(self.root, text="Emp ID", font=("times new roman",15),bg="white").place(x=50,y=150)
        lbl_gender = Label(self.root, text="Gender", font=("times new roman",15),bg="white").place(x=400,y=150)
        lbl_contact = Label(self.root, text="Contact No.", font=("times new roman",15),bg="white").place(x=750,y=150)
        
        txt_empid = Entry(self.root, textvariable=self.var_emp_id, font=("times new roman",15),bg="white").place(x=150,y=150,width=180)
        cmb_gender=ttk.Combobox(self.root,textvariable=self.var_gender,values=("Search","Male","Female","Other"),state='readonly',justify=CENTER,font=("times new roman",12,"bold"))
        cmb_gender.place(x=500,y=150,width=180)
        cmb_gender.current(0)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("times new roman",15),bg="white").place(x=850,y=150,width=180)

        #Row2

        lbl_name = Label(self.root, text="Name", font=("times new roman",15),bg="white").place(x=50,y=190)
        lbl_dob = Label(self.root, text="D.O.B", font=("times new roman",15),bg="white").place(x=400,y=190)
        lbl_doj = Label(self.root, text="D.O.J", font=("times new roman",15),bg="white").place(x=750,y=190)
        
        txt_name = Entry(self.root, textvariable=self.var_name, font=("times new roman",15),bg="white").place(x=150,y=190,width=180)
        txt_dob = Entry(self.root, textvariable=self.var_dob, font=("times new roman",15),bg="white").place(x=500,y=190,width=180)
        txt_doj = Entry(self.root, textvariable=self.var_doj, font=("times new roman",15),bg="white").place(x=850,y=190,width=180)

        #Row3

        lbl_email = Label(self.root, text="Email ID", font=("times new roman",15),bg="white").place(x=50,y=230)
        lbl_password = Label(self.root, text="Password", font=("times new roman",15),bg="white").place(x=400,y=230)
        lbl_utype = Label(self.root, text="User Type", font=("times new roman",15),bg="white").place(x=750,y=230)
        
        txt_email = Entry(self.root, textvariable=self.var_email, font=("times new roman",15),bg="white").place(x=150,y=230,width=180)
        txt_password = Entry(self.root, textvariable=self.var_password, font=("times new roman",15),bg="white").place(x=500,y=230,width=180)
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype,values=("Search","Admin","Employee"),state='readonly',justify=CENTER,font=("times new roman",12,"bold"))
        cmb_utype.place(x=850,y=230,width=180)
        cmb_utype.current(0) 

        #Row4

        lbl_address = Label(self.root, text="Address", font=("times new roman",15),bg="white").place(x=50,y=270)
        lbl_salary = Label(self.root, text="Salary", font=("times new roman",15),bg="white").place(x=500,y=270)
        
        self.txt_address = Text(self.root, font=("times new roman",15),bg="white")
        self.txt_address.place(x=150,y=270,width=300,height=60)
        txt_salary = Entry(self.root, textvariable=self.var_salary, font=("times new roman",15),bg="white").place(x=600,y=270,width=180)

        btn_save = Button(self.root,text="Save",command=self.add,font=("times new roman",15,"bold"),bg="red",fg="black",cursor="hand2").place(x=500,y=305,width=110,height=28)
        btn_delete = Button(self.root,text="Delete",command=self.delete,font=("times new roman",15,"bold"),bg="red",fg="black",cursor="hand2").place(x=620,y=305,width=110,height=28)
        btn_update = Button(self.root,text="Update",command=self.update,font=("times new roman",15,"bold"),bg="red",fg="black",cursor="hand2").place(x=740,y=305,width=110,height=28)
        btn_clear = Button(self.root,text="Clear",command=self.clear,font=("times new roman",15,"bold"),bg="red",fg="black",cursor="hand2").place(x=860,y=305,width=110,height=28)

        #Employee Details

        emp_frame = Frame(self.root, bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=350,relwidth=1,height=150)
        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.EmployeeTable = ttk.Treeview(emp_frame,columns=("emp_id","name","email","gender","contact","dob","doj","password","utype","address","salary"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("emp_id", text="Emp No")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("name", text="Name")
        self.EmployeeTable.heading("dob", text="D.O.B")
        self.EmployeeTable.heading("doj", text="D.O.J")
        self.EmployeeTable.heading("email", text="Email ID")
        self.EmployeeTable.heading("password", text="Password")
        self.EmployeeTable.heading("utype", text="User Type")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salary", text="Salary")
        
        self.EmployeeTable["show"] = "headings"

        self.EmployeeTable.column("emp_id", width=90)
        self.EmployeeTable.column("gender", width=90)
        self.EmployeeTable.column("contact", width=90)
        self.EmployeeTable.column("name", width=90)
        self.EmployeeTable.column("dob", width=90)
        self.EmployeeTable.column("doj", width=90)
        self.EmployeeTable.column("email", width=90)
        self.EmployeeTable.column("password", width=90)
        self.EmployeeTable.column("utype", width=90)
        self.EmployeeTable.column("address", width=90)
        self.EmployeeTable.column("salary", width=90)
        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    #Adding Add function     

    def add(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error", f"Employee ID must be required", parent=self.root)
            else:
                cur.execute("select * from EMP where emp_id=?",(self.var_emp_id.get(),))
                row = cur.fetchone() 
                if row != None:
                    messagebox.showerror("Error","This Employee ID already addigned, try different", parent=self.root)
                else:
                    cur.execute("Insert into EMP (emp_id,name,email,gender,contact,dob,doj,password,utype,address,salary) VALUES(?,?,?,?,?,?,?,?,?,?,?)",(
                        self.var_emp_id.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_password.get(),
                        self.var_utype.get(),
                        self.txt_address.get('1.0',END),
                        self.var_salary.get()
                    ))    
                    con.commit()
                    messagebox.showinfo("Success","Employee added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent= self.root)

    #Showing the stored Records 

    def show(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            cur.execute("select * from EMP")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)
        except Exception as ex:    
            messagebox.showerror("Error",f"Error due to: {str(ex)}", self.root)


    #Getting the stored data directly into each respective cells

    def get_data(self,ev):
        f = self.EmployeeTable.focus()
        content = (self.EmployeeTable.item(f))
        row = content['values']
        #print(row)
        self.var_emp_id.set(row[0]),self.var_name.set(row[1]),
        self.var_email.set(row[2]),self.var_gender.set(row[3]),
        self.var_contact.set(row[4]),self.var_dob.set(row[5]),
        self.var_doj.set(row[6]),self.var_password.set(row[7]),
        self.var_utype.set(row[8]),self.txt_address.delete('1.0',END),self.txt_address.insert(END, row[9]),
        self.var_salary.set(row[10])

    
    #Adding Update function

    def update(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error", f"Employee ID must be required", parent=self.root)
            else:
                cur.execute("select * from EMP where emp_id=?",(self.var_emp_id.get(),))
                row = cur.fetchone() 
                if row == None:
                    messagebox.showerror("Error","Invalid Employee ID", parent=self.root)
                else:
                    cur.execute("Update EMP set name=?,email=?,gender=?,contact=?,dob=?,doj=?,password=?,utype=?,address=?,salary=? where emp_id = ?",(
                        self.var_name.get(),
                        self.var_email.get(),self.var_gender.get(),
                        self.var_contact.get(),self.var_dob.get(),
                        self.var_doj.get(),self.var_password.get(),
                        self.var_utype.get(),self.txt_address.get('1.0',END),
                        self.var_salary.get(),self.var_emp_id.get()
                    ))    
                    con.commit()
                    messagebox.showinfo("Success","Employee Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent= self.root)

    #Adding Delete function

    def delete(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error", f"Employee ID must be required", parent=self.root)
            else:
                cur.execute("select * from EMP where emp_id=?",(self.var_emp_id.get(),))
                row = cur.fetchone() 
                if row == None:
                    messagebox.showerror("Error","Invalid Employee ID", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm","Do you really want to delete it.", parent=self.root)
                    if op == True:
                        cur.execute("delete from EMP where emp_id = ?",(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Employee Deleted Successfully", parent=self.root)
                        self.show()
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent= self.root)

    
    #Adding Clear function

    def clear(self):
        self.var_emp_id.set(""),self.var_name.set(""),
        self.var_email.set(""),self.var_gender.set("Select"),
        self.var_contact.set(""),self.var_dob.set(""),
        self.var_doj.set(""),self.var_password.set(""),
        self.var_utype.set("Select"),self.txt_address.delete('1.0',END),
        self.var_salary.set(""),self.var_searchtxt.set(""),self.var_searchby.set("Select")
        self.show()


    #Search function

    def search(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error","Select search by Option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error","Search input should be required", parent=self.root)
            else:    
                cur.execute("select * from EMP where "+self.var_searchby.get()+ " LIKE '%"+self.var_searchtxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No records found!!",parent=self.root)        

        except Exception as ex:    
            messagebox.showerror("Error",f"Error due to: {str(ex)}", self.root)



if __name__=="__main__":
    root = Tk()
    obj = employeeClass(root)
    root.mainloop()

