from tkinter import  *
from PIL import Image,ImageTk
from tkinter import ttk, messagebox, END
import sqlite3

class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed by Aaryan")
        self.root.config(bg="White")
        self.root.focus_force()

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()
        self.var_desc = StringVar()

        #Search Bar for Searchby Option

        lbl_search = LabelFrame(self.root, text="Search Supplier", bg="white",font=("times new roman",12,"bold"),bd=2,relief=RIDGE)
        lbl_search.place(x=660,y=60,width=420,height=70)

        lbl_search=ttk.Label(self.root,text="Invoice No.",font=("times new roman",12,"bold"))
        lbl_search.place(x=670,y=90)

        txt_search = Entry(self.root,textvariable=self.var_searchtxt,font=("times new roman",15,"bold"),bg="lightyellow").place(x=760,y=90)
        btn_search = Button(self.root,text="Search",command=self.search,font=("times new roman",15,"bold"),bg="red",fg="black",cursor="hand2").place(x=975,y=90,width=90,height=30)

        #Title

        title = Label(self.root, text="Suppliers Details", font=("times new roman",20),bg="#0f4d7d",fg="white").place(x=50,y=10,width=1000,height=40)

        #Row1

        lbl_invoice = Label(self.root, text="Serial No.", font=("times new roman",15),bg="white").place(x=50,y=80)
        txt_invoice = Entry(self.root, textvariable=self.var_invoice, font=("times new roman",15),bg="white").place(x=180,y=80,width=180)
        
        #Row2

        lbl_name = Label(self.root, text="Name", font=("times new roman",15),bg="white").place(x=50,y=120)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("times new roman",15),bg="white").place(x=180,y=120,width=180)
    
        #Row3

        lbl_contact = Label(self.root, text="Email ID", font=("times new roman",15),bg="white").place(x=50,y=160)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("times new roman",15),bg="white").place(x=180,y=160,width=180)
        
        #Row4

        self.lbl_desc = Label(self.root, text="Description", font=("times new roman",15),bg="white").place(x=50,y=200)
        self.txt_desc = Entry(self.root, textvariable=self.var_desc, font=("times new roman",15),bg="white").place(x=180,y=200,width=350,height=120)

        btn_save = Button(self.root,text="Save",command=self.add,font=("times new roman",15,"bold"),bg="red",fg="black",cursor="hand2").place(x=180,y=350,width=110,height=28)
        btn_delete = Button(self.root,text="Delete",command=self.delete,font=("times new roman",15,"bold"),bg="red",fg="black",cursor="hand2").place(x=300,y=350,width=110,height=28)
        btn_update = Button(self.root,text="Update",command=self.update,font=("times new roman",15,"bold"),bg="red",fg="black",cursor="hand2").place(x=420,y=350,width=110,height=28)
        btn_clear = Button(self.root,text="Clear",command=self.clear,font=("times new roman",15,"bold"),bg="red",fg="black",cursor="hand2").place(x=540,y=350,width=110,height=28)

        #Employee Details

        emp_frame = Frame(self.root, bd=3,relief=RIDGE)
        emp_frame.place(x=660,y=140,width=420,height=350)
        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.SupplierTable = ttk.Treeview(emp_frame,columns=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)

        self.SupplierTable.heading("invoice", text="Sr.")
        self.SupplierTable.heading("name", text="Name")
        self.SupplierTable.heading("contact", text="Contact")
        self.SupplierTable.heading("desc", text="Description")
        
        self.SupplierTable["show"] = "headings"

        self.SupplierTable.column("invoice", width=30)
        self.SupplierTable.column("name", width=130)
        self.SupplierTable.column("contact", width=110)
        self.SupplierTable.column("desc", width=90)
        self.SupplierTable.pack(fill=BOTH, expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    #Adding Add function     

    def add(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_invoice.get()=="":
                messagebox.showerror("Error", f"Invoice No. must be required", parent=self.root)
            else:
                cur.execute("select * from SUP where invoice=?",(self.var_invoice.get(),))
                row = cur.fetchone() 
                if row != None:
                    messagebox.showerror("Error","This Invoice No. already addigned, try different", parent=self.root)
                else:
                    cur.execute("Insert into SUP (invoice,name,contact,desc) VALUES(?,?,?,?)",(
                        self.var_invoice.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.var_desc.get()
                    ))    
                    con.commit()
                    messagebox.showinfo("Success","Supplier Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent= self.root)

    #Showing the stored Records 

    def show(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            cur.execute("select * from SUP")
            rows = cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('',END,values=row)
        except Exception as ex:    
            messagebox.showerror("Error",f"Error due to: {str(ex)}", self.root)


    #Getting the stored data directly into each respective cells

    def get_data(self,ev):
        f = self.SupplierTable.focus()
        content = (self.SupplierTable.item(f))
        row = content['values']
        self.var_invoice.set(row[0]),
        self.var_name.set(row[1]),
        self.var_contact.set(row[2]),
        self.txt_desc.delete('1.0',END),
        self.txt_desc.insert(END, row[3])

    
    #Adding Update function

    def update(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_invoice.get() == "":
                messagebox.showerror("Error", f"Invoice No. must be required", parent=self.root)
            else:
                cur.execute("select * from SUP where invoice=?",(self.var_invoice.get(),))
                row = cur.fetchone() 
                if row == None:
                    messagebox.showerror("Error","Invalid Invoice No.", parent=self.root)
                else:
                    cur.execute("Update SUP set name=?,contact=?,desc=? where invoice = ?",(
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0',END),
                        self.var_invoice.get()
                    ))    
                    con.commit()
                    messagebox.showinfo("Success","Supplier Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent= self.root)

    #Adding Delete function

    def delete(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_invoice.get()=="":
                messagebox.showerror("Error", f"Invoice No. must be required", parent=self.root)
            else:
                cur.execute("select * from SUP where invoice=?",(self.var_invoice.get(),))
                row = cur.fetchone() 
                if row == None:
                    messagebox.showerror("Error","Invalid Invoice No.", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm","Do you really want to delete it.", parent=self.root)
                    if op == True:
                        cur.execute("delete from SUP where invoice = ?",(self.var_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Supplier Deleted Successfully", parent=self.root)
                        self.show()
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent= self.root)

    
    #Adding Clear function

    def clear(self):
        self.var_invoice.set(""),
        self.var_name.set(""),
        self.var_contact.set(""),
        self.txt_desc.delete('1.0',END),
        self.var_searchtxt.set(""),
        self.show()


    #Search function

    def search(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error","Invoice No. should be required", parent=self.root)
            else:    
                cur.execute("select * from SUP where invoice = ?",(self.var_searchtxt.get(),))
                row = cur.fetchone()
                if row != None:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    self.SupplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No records found!!",parent=self.root)        

        except Exception as ex:    
            messagebox.showerror("Error",f"Error due to: {str(ex)}", self.root)



if __name__=="__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()

