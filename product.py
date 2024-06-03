from tkinter import  *
from PIL import Image,ImageTk
from tkinter import ttk, messagebox,END
import sqlite3

class productClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed by Aaryan")
        self.root.config(bg="White")
        self.root.focus_force()
        
        self.var_pid = StringVar()
        self.var_category = StringVar()
        self.var_supplier = StringVar()

        self.cat_list = []
        self.sup_list = []

        self.fetch_category_supplier()
        
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()


        product_frame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_frame.place(x=10,y=10,width=450,height=480)

        title = Label(product_frame, text="Manage Product Details", font=("times new roman",18),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)

        #Row1
        lbl_category = Label(product_frame, text="Category", font=("times new roman",15),bg="white").place(x=50,y=50)
        cmb_category = ttk.Combobox(product_frame,textvariable=self.var_category,values=self.cat_list,state='readonly',justify=CENTER,font=("times new roman",12,"bold"))
        cmb_category.place(x=175,y=50,width=180)
        cmb_category.current(0)

        #Row2
        lbl_supplier = Label(product_frame, text="Supplier", font=("times new roman",15),bg="white").place(x=50,y=100)
        cmb_supplier = ttk.Combobox(product_frame,textvariable=self.var_supplier,values=self.sup_list,state='readonly',justify=CENTER,font=("times new roman",12,"bold"))
        cmb_supplier.place(x=175,y=100,width=180)
        cmb_supplier.current(0)

        #Row3
        lbl_name = Label(self.root, text="Name", font=("times new roman",15),bg="white").place(x=65,y=165)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("times new roman",15),bg="white").place(x=185,y=165,width=180)

        #Row4
        lbl_price = Label(self.root, text="Price", font=("times new roman",15),bg="white").place(x=65,y=220)
        txt_price = Entry(self.root, textvariable=self.var_price, font=("times new roman",15),bg="white").place(x=185,y=220,width=180)

        #Row5
        lbl_qty = Label(self.root, text="QTY", font=("times new roman",15),bg="white").place(x=65,y=275)
        txt_qty = Entry(self.root, textvariable=self.var_qty, font=("times new roman",15),bg="white").place(x=185,y=275,width=180)

        #Row6
        lbl_status = Label(product_frame, text="Status", font=("times new roman",15),bg="white").place(x=50,y=320)
        cmb_status = ttk.Combobox(product_frame,textvariable=self.var_status,values=("Search","Active","Inactive"),state='readonly',justify=CENTER,font=("times new roman",12,"bold"))
        cmb_status.place(x=175,y=320,width=180)
        cmb_status.current(0)

        #Row7
        btn_save = Button(product_frame,text="Save",command=self.add,font=("times new roman",15,"bold"),bg="red",fg="black",cursor="hand2").place(x=50,y=375,width=110,height=28)
        btn_delete = Button(product_frame,text="Delete",command=self.delete,font=("times new roman",15,"bold"),bg="red",fg="black",cursor="hand2").place(x=250,y=375,width=110,height=28)
        btn_update = Button(product_frame,text="Update",command=self.update,font=("times new roman",15,"bold"),bg="red",fg="black",cursor="hand2").place(x=50,y=425,width=110,height=28)
        btn_clear = Button(product_frame,text="Clear",command=self.clear,font=("times new roman",15,"bold"),bg="red",fg="black",cursor="hand2").place(x=250,y=425,width=110,height=28)


        #Search Frame
        SearchFrame = LabelFrame(self.root, text="Search Supplier", bg="white",font=("times new roman",12,"bold"),bd=2,relief=RIDGE)
        SearchFrame.place(x=480,y=10,width=600,height=80)

        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Search","Category","Supplier","Name"),state='readonly',justify=CENTER,font=("times new roman",12,"bold"))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame,textvariable=self.var_searchtxt,font=("times new roman",15,"bold"),bg="lightyellow").place(x=200,y=10)
        btn_search = Button(SearchFrame,text="Search",command=self.search,font=("times new roman",15,"bold"),bg="red",fg="black",cursor="hand2").place(x=410,y=10,width=150,height=30)

        #Product Detail

        p_frame = Frame(self.root, bd=3,relief=RIDGE)
        p_frame.place(x=480,y=100,width=600,height=390)
        scrolly = Scrollbar(p_frame, orient=VERTICAL)
        scrollx = Scrollbar(p_frame, orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(p_frame,columns=("pid","Category","Supplier","Name","Price","QTY","Status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)

        self.ProductTable.heading("pid", text="Product ID")
        self.ProductTable.heading("Category", text="Category")
        self.ProductTable.heading("Supplier", text="Supplier")
        self.ProductTable.heading("Name", text="Name")
        self.ProductTable.heading("Price", text="Price")
        self.ProductTable.heading("QTY", text="QTY")
        self.ProductTable.heading("Status", text="Status")

        
        self.ProductTable["show"] = "headings"

        self.ProductTable.column("pid", width=90)
        self.ProductTable.column("Category", width=90)
        self.ProductTable.column("Supplier", width=90)
        self.ProductTable.column("Name", width=150)
        self.ProductTable.column("Price", width=90)
        self.ProductTable.column("QTY", width=90)
        self.ProductTable.column("Status", width=90)
        self.ProductTable.pack(fill=BOTH, expand=1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()
        


    def fetch_category_supplier(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            cur.execute("select name from CAT")
            cat = cur.fetchall()
            if len(cat) > 0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])

            cur.execute("select name from SUP")
            sup = cur.fetchall()
            if len(sup) > 0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent= self.root)


        
    #Adding Add function     

    def add(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_category.get()=="Select" or self.var_category.get()=="Empty" or self.var_supplier.get()=="Select" or self.var_name.get()=="":
                messagebox.showerror("Error", f"All fields are required", parent=self.root)
            else:
                cur.execute("select * from PRO where Name=?",(self.var_name.get(),))
                row = cur.fetchone() 
                if row != None:
                    messagebox.showerror("Error","Product already present, try different", parent=self.root)
                else:
                    cur.execute("Insert into PRO (Category,Supplier,Name,Price,QTY,Status) VALUES(?,?,?,?,?,?)",(
                        self.var_category.get(),
                        self.var_supplier.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get()
                    ))    
                    con.commit()
                    messagebox.showinfo("Success","Product added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent= self.root)

    #Showing the stored Records 

    def show(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            cur.execute("select * from PRO")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
        except Exception as ex:    
            messagebox.showerror("Error",f"Error due to: {str(ex)}", self.root)


    #Getting the stored data directly into each respective cells

    def get_data(self,ev):
        f = self.ProductTable.focus()
        content = (self.ProductTable.item(f))
        row = content['values']
        #print(row)
        self.var_pid.set(row[0]),
        self.var_category.set(row[1]),
        self.var_supplier.set(row[2]),
        self.var_name.set(row[3]),
        self.var_price.set(row[4]),
        self.var_qty.set(row[5]),
        self.var_status.set(row[6])
        
    #Adding Update function

    def update(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error", f"Please select product from list", parent=self.root)
            else:
                cur.execute("select * from PRO where pid=?",(self.var_pid.get(),))
                row = cur.fetchone() 
                if row == None:
                    messagebox.showerror("Error","Invalid Product ID", parent=self.root)
                else:
                    cur.execute("Update PRO set Category=?,Supplier=?,Name=?,Price=?,QTY=?,Status=? where pid = ?",(
                        self.var_pid.get(),
                        self.var_category.get(),
                        self.var_supplier.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get()
                    ))    
                    con.commit()
                    messagebox.showinfo("Success","Product Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent= self.root)

    #Adding Delete function

    def delete(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error", f"Select Product from list", parent=self.root)
            else:
                cur.execute("select * from PRO where pid=?",(self.var_pid.get(),))
                row = cur.fetchone() 
                if row == None:
                    messagebox.showerror("Error","Invalid Product", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm","Do you really want to delete it.", parent=self.root)
                    if op == True:
                        cur.execute("delete from PRO where pid = ?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Product Deleted Successfully", parent=self.root)
                        self.show()
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent= self.root)

    
    #Adding Clear function

    def clear(self):
        self.var_pid.set(""),
        self.var_category.set("Select"),
        self.var_supplier.set("Select"),
        self.var_name.set(""),
        self.var_price.set(""),
        self.var_qty.set(""),
        self.var_status.set("Active"),
        self.var_searchtxt.set(""),
        self.var_searchby.set("Select")
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
                cur.execute("select * from PRO where "+self.var_searchby.get()+ " LIKE '%"+self.var_searchtxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No records found!!",parent=self.root)        

        except Exception as ex:    
            messagebox.showerror("Error",f"Error due to: {str(ex)}", self.root)


    

if __name__=="__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()        