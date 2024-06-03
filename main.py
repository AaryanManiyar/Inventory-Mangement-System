from tkinter import  *
from PIL import Image,ImageTk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
import sqlite3
from tkinter import ttk, messagebox
import os
import time

class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Developed by Aaryan")
        self.root.config(bg="White")

        self.icon_title = PhotoImage(file="images/logo1.png")
        title = Label(self.root, text="Inventory Management System",image=self.icon_title,compound="left",font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        btn_logout = Button(self.root, text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="yellow").place(x=1100,y=10,height=50,width=150)

        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management System \t\t Date: DD-MM-YYYY \t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        self.MenuLogo = Image.open("images/menu_im.png")
        self.MenuLogo = self.MenuLogo.resize((200,200))
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        leftmenu = Frame(self.root, bd=2, relief=RIDGE)
        leftmenu.place(x=0,y=102,width=200,height=590)

        lbl_menuLogo = Label(leftmenu, image=self.MenuLogo)
        lbl_menuLogo.pack(side = TOP, fill=X)

        self.icon_side = PhotoImage(file="images/side.png")
        lbl_menu = Label(leftmenu, text="Menu",font=("times new roman",20),bg="#009688").pack(side=TOP, fill=X)
        btn_employee = Button(leftmenu, text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,padx=20,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP, fill=X)
        btn_supplier = Button(leftmenu, text="Supplier",command=self.supplier,image=self.icon_side,compound=LEFT,padx=20,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP, fill=X)
        btn_category = Button(leftmenu, text="Category",command=self.category,image=self.icon_side,compound=LEFT,padx=20,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP, fill=X)
        btn_products = Button(leftmenu, text="Products",command=self.products,image=self.icon_side,compound=LEFT,padx=20,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP, fill=X)
        btn_sales = Button(leftmenu, text="Sales",command=self.sales,image=self.icon_side,compound=LEFT,padx=20,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP, fill=X)
        btn_exit = Button(leftmenu, text="Exit",image=self.icon_side,compound=LEFT,padx=20,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP, fill=X)


        self.lbl_employee = Label(self.root, text="Total Employee\n [0]",bd=5, relief=RIDGE,bg="#33bbf9", fg="white",font=("times new roman",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)

        self.lbl_supplier = Label(self.root, text="Total Supplier\n [0]",bd=5, relief=RIDGE,bg="#33bbf9", fg="white",font=("times new roman",20,"bold"))
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)

        self.lbl_category = Label(self.root, text="Total Category\n [0]",bd=5, relief=RIDGE,bg="#33bbf9", fg="white",font=("times new roman",20,"bold"))
        self.lbl_category.place(x=1000,y=120,height=150,width=300)

        self.lbl_products = Label(self.root, text="Total Products\n [0]",bd=5, relief=RIDGE,bg="#33bbf9", fg="white",font=("times new roman",20,"bold"))
        self.lbl_products.place(x=300,y=300,height=150,width=300)

        self.lbl_sales = Label(self.root, text="Total Sales\n [0]",bd=5, relief=RIDGE,bg="#33bbf9", fg="white",font=("times new roman",20,"bold"))
        self.lbl_sales.place(x=650,y=300,height=150,width=300)


        lbl_footer = Label(self.root, text="IMS - Inventory Management System | Developed by Aaryan\n For any Techincal Issue Contact : 7447499360",font=("times new roman",12),bg="#4d636d",fg="white")
        lbl_footer.pack(side=BOTTOM, fill=X)

        self.update_content()
        self.update_date_time()
#=======================================================================================================================================================================================================================================================
    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)
            
    def products(self):
        self.new_win=Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    def update_content(self):
        con = sqlite3.connect(database = r'IMS.db')
        cur = con.cursor()
        try:
            cur.execute("select * from PRO")
            product = cur.fetchall()
            self.lbl_products.config(text=f'Total Product \n [ {str(len(product))} ]')

            cur.execute("select * from SUP")
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f'Total Supplier \n [ {str(len(supplier))} ]')

            cur.execute("select * from CAT")
            category = cur.fetchall()
            self.lbl_category.config(text=f'Total Category \n [ {str(len(category))} ]')

            cur.execute("select * from EMP")
            employee = cur.fetchall()
            self.lbl_employee.config(text=f'Total Employee \n [ {str(len(employee))} ]') 

            bill_count = len(os.listdir('bill'))
            self.lbl_sales.config(text=f'Total Sales \n [{str(bill_count)}]')    
        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}", parent=self.root)


    def update_date_time(self):  
        time_ = time.strftime("%I:%M:%S")
        date_ = time.strftime("%d:%m:%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System \t\t Date: {str(date_)} \t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)


    def logout(self):
        self.root.destroy()  
        os.system("python login.py") 

if __name__=="__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()


