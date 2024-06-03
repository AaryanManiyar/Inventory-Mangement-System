from tkinter import  *
from PIL import Image,ImageTk
from tkinter import ttk, messagebox
import sqlite3

class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed by Aaryan")
        self.root.config(bg="White")
        self.root.focus_force()

        self.var_cid = StringVar()
        self.var_name = StringVar()

        lbl_title = Label(self.root, text="Manage Product Category", font=("times new roman",30),bg="#184a45",fg="white").place(x=50,y=10,width=1000,height=60)

        lbl_name = Label(self.root, text="Enter Category Name", font=("times new roman",20),bg="white").place(x=50,y=100)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("times new roman",20),bg="lightyellow").place(x=50,y=150,width=300)

        btn_add = Button(self.root,text="Add",command=self.add,font=("times new roman",20),bg="red",fg="black",cursor="hand2").place(x=400,y=150,width=100,height=38)
        btn_delete = Button(self.root,text="Delete",command=self.delete,font=("times new roman",20),bg="red",fg="black",cursor="hand2").place(x=525,y=150,width=100,height=38)

        #Category details

        cat_frame = Frame(self.root, bd=3,relief=RIDGE)
        cat_frame.place(x=660,y=110,width=420,height=380)
        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)

        self.CategoryTable = ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CategoryTable.xview)
        scrolly.config(command=self.CategoryTable.yview)

        self.CategoryTable.heading("cid", text="Category ID")
        self.CategoryTable.heading("name", text="Name")
        
        self.CategoryTable["show"] = "headings"

        self.CategoryTable.column("cid", width=90)
        self.CategoryTable.column("name", width=90)
        self.CategoryTable.pack(fill=BOTH, expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>", self.get_data)

        self.im1 = Image.open("images/cat.jpg")
        self.im1 = self.im1.resize((500,200))
        self.im1 = ImageTk.PhotoImage(self.im1)
        self.lbl_im1 = Label(self.root, image = self.im1)
        self.lbl_im1.place(x=30,y=220)

        #self.im2 = Image.open("images/category.jpg")
        #self.im2 = self.im2.resize((500,200))
        #self.im2 = ImageTk.PhotoImage(self.im2)
        #self.lbl_im2 = Label(self.root, image = self.im2)
        #self.lbl_im2.place(x=570,y=220)
        #self.show()

    #Add Function
    def add(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error", f"Category Name should be required", parent=self.root)
            else:
                cur.execute("select * from CAT where name=?",(self.var_name.get(),))
                row = cur.fetchone() 
                if row != None:
                    messagebox.showerror("Error","This Category is already addigned, try different", parent=self.root)
                else:
                    cur.execute("Insert into CAT (name) VALUES(?)",(self.var_name.get(),))    
                    con.commit()
                    messagebox.showinfo("Success","Category added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent= self.root)

    def show(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            cur.execute("select * from CAT")
            rows = cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('',END,values=row)
        except Exception as ex:    
            messagebox.showerror("Error",f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self,ev):
        f = self.CategoryTable.focus()
        content = (self.CategoryTable.item(f))
        row = content['values']
        #print(row)
        self.var_cid.set(row[0]),
        self.var_name.set(row[1]),

    def clear(self):
        self.var_name.set("")
        self.show()

    def delete(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error", f"Category Name must be required", parent=self.root)
            else:
                cur.execute("select * from CAT where name=?",(self.var_name.get(),))
                row = cur.fetchone() 
                if row == None:
                    messagebox.showerror("Error","Invalid Category Name", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm","Do you really want to delete it.", parent=self.root)
                    if op == True:
                        cur.execute("delete from CAT where name = ?",(self.var_name.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Category Deleted Successfully", parent=self.root)
                        self.show()
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent= self.root)


if __name__=="__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()