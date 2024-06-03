from tkinter import  *
from PIL import Image,ImageTk
from tkinter import ttk, messagebox
import sqlite3
import time
import os
import tempfile 


class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Developed by Aaryan")
        self.root.config(bg="White")
        self.cart_list = []
        self.chk_print = 0


        self.icon_title = PhotoImage(file="images/logo1.png")
        title = Label(self.root, text="Inventory Management System",image=self.icon_title,compound="left",font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        btn_logout = Button(self.root, text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="yellow").place(x=1100,y=10,height=50,width=150)

        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management System \t\t Date: DD-MM-YYYY \t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        
        #Product Frame=========================================================================================================================================================================================================================
        self.var_search = StringVar()
        product_frame = Frame(self.root,bd=4,relief=RIDGE,bg="white")
        product_frame.place(x=6,y=110,width=410,height=550)
        ptitle = Label(product_frame, text="All Products", font=("times new roman",20,"bold"),bg="#262626",fg="white")
        ptitle.pack(side=TOP, fill=X)

        product_frame1 = Frame(product_frame,bd=2,relief=RIDGE,bg="white")
        product_frame1.place(x=2,y=42,width=398,height=90)

        lbl_search = Label(product_frame1, text="Search Product | By Name", font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)
        lbl_name = Label(product_frame1, text="Product Name", font=("times new roman",15,"bold"),bg="white").place(x=2,y=45)
        txt_search = Entry(product_frame1, textvariable=self.var_search, font=("times new roman",15),bg="lightyellow").place(x=130,y=47,width=150,height=22)
        btn_search = Button(product_frame1, text="Search",command=self.search,font=("times new roman",15),bg="#2196f3",fg="white",cursor="hand2").place(x=285,y=47,width=100,height=22)
        btn_show_all = Button(product_frame1, text="Show All",command=self.show,font=("times new roman",15),bg="#2196f3",fg="white",cursor="hand2").place(x=285,y=10,width=100,height=22)

        productframe2 = Frame(product_frame, bd=3,relief=RIDGE)
        productframe2.place(x=2,y=140,width=398,height=385)
        scrolly = Scrollbar(productframe2, orient=VERTICAL)
        scrollx = Scrollbar(productframe2, orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(productframe2,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ProductTable.xview)

        self.ProductTable.heading("pid", text="P ID")
        self.ProductTable.heading("name", text="Name")
        self.ProductTable.heading("price", text="Price")
        self.ProductTable.heading("qty", text="QTY")
        self.ProductTable.heading("status", text="Status")
        
        self.ProductTable["show"] = "headings"

        self.ProductTable.column("pid", width=40)
        self.ProductTable.column("name", width=90)
        self.ProductTable.column("price", width=60)
        self.ProductTable.column("qty", width=40)
        self.ProductTable.column("status", width=90)
        self.ProductTable.pack(fill=BOTH, expand=1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)
        lbl_note = Label(product_frame, text="Note: Enter 0 Qty to remove product from the cart",font=("times new roman",10),bg="white",fg="red").pack(side=BOTTOM, fill=X)

        #Customer Frame ============================================================================================================================================================================================================
        self.var_cname = StringVar()
        self.var_contact = StringVar()

        customerframe = Frame(self.root, bd=4,relief=RIDGE,bg="white")
        customerframe.place(x=420,y=110,width=530,height=70)
        ctitle = Label(customerframe, text="Customer Details", font=("times new roman",15),bg="grey")
        ctitle.pack(side=TOP, fill=X)

        lbl_name1 = Label(customerframe, text="Name", font=("times new roman",15),bg="white")
        lbl_name1.place(x=5,y=35)        
        txt_name1 = Entry(customerframe, textvariable=self.var_cname, font=("times new roman",13),bg="lightyellow")
        txt_name1.place(x=80,y=35,width=140)
 
        lbl_name1 = Label(customerframe, text="Contact No.", font=("times new roman",15),bg="white")
        lbl_name1.place(x=250,y=35)        
        txt_name1 = Entry(customerframe, textvariable=self.var_contact, font=("times new roman",13),bg="lightyellow")
        txt_name1.place(x=360,y=35,width=140)

        cal_cart_frame = Frame(self.root, bd=2,relief=RIDGE,bg="white")
        cal_cart_frame.place(x=420,y=190,width=530,height=360)

        
        self.var_cal_input = StringVar()
        cal_frame = Frame(cal_cart_frame, bd=9,relief=RIDGE,bg="white")
        cal_frame.place(x=5,y=10,width=268,height=340)

        txt_cal_input = Entry(cal_frame, textvariable=self.var_cal_input,font=("times new roman",15,"bold"),width=23,bd=10,relief=GROOVE,state='readonly',justify=RIGHT)
        txt_cal_input.grid(row=0,columnspan=4)

        btn_7 = Button(cal_frame, text='7',font=("times new roman",15,"bold"),command=lambda:self.get_input(7),bd=5,width=4,pady=12,cursor="hand2").grid(row=1,column=0)
        btn_8 = Button(cal_frame, text='8',font=("times new roman",15,"bold"),command=lambda:self.get_input(8),bd=5,width=4,pady=12,cursor="hand2").grid(row=1,column=1)
        btn_9 = Button(cal_frame, text='9',font=("times new roman",15,"bold"),command=lambda:self.get_input(9),bd=5,width=4,pady=12,cursor="hand2").grid(row=1,column=2)
        btn_sum = Button(cal_frame, text='+',font=("times new roman",15,"bold"),command=lambda:self.get_input('+'),bd=5,width=4,pady=12,cursor="hand2").grid(row=1,column=3)

        btn_4 = Button(cal_frame, text='4',font=("times new roman",15,"bold"),command=lambda:self.get_input(4),bd=5,width=4,pady=12,cursor="hand2").grid(row=2,column=0)
        btn_5 = Button(cal_frame, text='5',font=("times new roman",15,"bold"),command=lambda:self.get_input(5),bd=5,width=4,pady=12,cursor="hand2").grid(row=2,column=1)
        btn_6 = Button(cal_frame, text='6',font=("times new roman",15,"bold"),command=lambda:self.get_input(6),bd=5,width=4,pady=12,cursor="hand2").grid(row=2,column=2)
        btn_diff = Button(cal_frame, text='-',font=("times new roman",15,"bold"),command=lambda:self.get_input('-'),bd=5,width=4,pady=12,cursor="hand2").grid(row=2,column=3)

        btn_1 = Button(cal_frame, text='1',font=("times new roman",15,"bold"),command=lambda:self.get_input(1),bd=5,width=4,pady=12,cursor="hand2").grid(row=3,column=0)
        btn_2 = Button(cal_frame, text='2',font=("times new roman",15,"bold"),command=lambda:self.get_input(2),bd=5,width=4,pady=12,cursor="hand2").grid(row=3,column=1)
        btn_3 = Button(cal_frame, text='3',font=("times new roman",15,"bold"),command=lambda:self.get_input(3),bd=5,width=4,pady=12,cursor="hand2").grid(row=3,column=2)
        btn_multiply = Button(cal_frame, text='*',font=("times new roman",15,"bold"),command=lambda:self.get_input('*'),bd=5,width=4,pady=12,cursor="hand2").grid(row=3,column=3)

        btn_0 = Button(cal_frame, text='0',font=("times new roman",15,"bold"),command=lambda:self.get_input(0),bd=5,width=4,pady=13,cursor="hand2").grid(row=4,column=0)
        btn_c = Button(cal_frame, text='C',font=("times new roman",15,"bold"),command=self.clear_cal,bd=5,width=4,pady=13,cursor="hand2").grid(row=4,column=1)
        btn_eq = Button(cal_frame, text='=',font=("times new roman",15,"bold"),command=self.perform_cal,bd=5,width=4,pady=13,cursor="hand2").grid(row=4,column=2)
        btn_div = Button(cal_frame, text='/',font=("times new roman",15,"bold"),command=lambda:self.get_input('/'),bd=5,width=4,pady=13,cursor="hand2").grid(row=4,column=3)

        cartframe = Frame(cal_cart_frame, bd=3,relief=RIDGE)
        cartframe.place(x=280,y=8,width=245,height=342)
        self.cart_title = Label(cartframe, text="Cart Total Product: [0]", font=("times new roman",15),bg="grey")
        self.cart_title.pack(side=TOP, fill=X)
        scrolly = Scrollbar(cartframe, orient=VERTICAL)
        scrollx = Scrollbar(cartframe, orient=HORIZONTAL)

        self.CartTable = ttk.Treeview(cartframe,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("pid", text="P ID")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="QTY")
        
        self.CartTable["show"] = "headings"

        self.CartTable.column("pid", width=40)
        self.CartTable.column("name", width=90)
        self.CartTable.column("price", width=90)
        self.CartTable.column("qty", width=40)
        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)
        
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()



        add_cartframe = Frame(self.root, bd=2,relief=RIDGE,bg="white")
        add_cartframe.place(x=420,y=550,width=530,height=110)

        lbl_product_name = Label(add_cartframe, text="Product Name", font=("times new roman",15),bg="white")
        lbl_product_name.place(x=5,y=5)
        txt_product_name = Entry(add_cartframe, textvariable=self.var_pname, font=("times new roman",15),bg="lightyellow",state="readonly")
        txt_product_name.place(x=5,y=35,width=190,height=22)

        lbl_product_price = Label(add_cartframe, text="Price for Qty", font=("times new roman",15),bg="white")
        lbl_product_price.place(x=230,y=5)
        txt_product_price = Entry(add_cartframe, textvariable=self.var_price, font=("times new roman",15),bg="lightyellow",state="readonly")
        txt_product_price.place(x=230,y=35,width=150,height=22)

        lbl_product_qty = Label(add_cartframe, text="Quantity", font=("times new roman",15),bg="white")
        lbl_product_qty.place(x=390,y=5)
        txt_product_qty = Entry(add_cartframe, textvariable=self.var_qty, font=("times new roman",15),bg="lightyellow")
        txt_product_qty.place(x=390,y=35,width=110,height=22)

        self.lbl_instock = Label(add_cartframe, text="In Stock", font=("times new roman",15),bg="white")
        self.lbl_instock.place(x=5,y=70)

        btn_add = Button(add_cartframe, text="Add or Update",command=self.add_update_cart,font=("times new roman",15),bg="#2196f3",fg="white",cursor="hand2")
        btn_add.place(x=180,y=70,width=150,height=30)
        btn_clear = Button(add_cartframe, text="Clear",command=self.clear_cart,font=("times new roman",15),bg="#2196f3",fg="white",cursor="hand2")
        btn_clear.place(x=340,y=70,width=150,height=30)
        

        customer_billing_frame = Frame(self.root, bd=4,relief=RIDGE,bg="white")
        customer_billing_frame.place(x=950,y=110,width=400,height=430)
        billing_title = Label(customer_billing_frame, text="Customer Billing Area", font=("times new roman",15),bg="grey")
        billing_title.pack(side=TOP, fill=X)
        scrollx = Scrollbar(customer_billing_frame, orient=HORIZONTAL)
        scrolly.pack(side=BOTTOM,fill=X)
        scrolly = Scrollbar(customer_billing_frame, orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        self.txt_bill_area = Text(customer_billing_frame, font=("times new roman",20,"bold"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrollx.config(command=self.txt_bill_area.xview)
        scrolly.config(command=self.txt_bill_area.yview)

        widget_frame = Frame(self.root, bd=4,relief=RIDGE,bg="white")
        widget_frame.place(x=950,y=540,width=400,height=120)
        
        self.lbl_bill_amount = Label(widget_frame, text="Bill Amt \n [0]",font=("times new roman",15,"bold"),bg="#3232ff",cursor="hand2",fg="white")
        self.lbl_bill_amount.place(x=7,y=10,width=120,height=45)

        self.lbl_discount = Label(widget_frame, text="Discount \n 5%",font=("times new roman",15,"bold"),bg="#007f00",cursor="hand2",fg="white")
        self.lbl_discount.place(x=140,y=10,width=120,height=45)

        self.lbl_net_pay = Label(widget_frame, text="Net Pay \n [0]",font=("times new roman",14,"bold"),bg="#555555",cursor="hand2",fg="white")
        self.lbl_net_pay.place(x=270,y=10,width=120,height=45)

        btn_print = Button(widget_frame, text="Print",command=self.print_bill,font=("times new roman",15,"bold"),bg="#00cc00",cursor="hand2",fg="white")
        btn_print.place(x=7,y=60,width=120,height=45)

        btn_clear_all = Button(widget_frame, text="Clear All",command=self.clear_all,font=("times new roman",15,"bold"),bg="#555555",cursor="hand2",fg="white")
        btn_clear_all.place(x=140,y=60,width=120,height=45)

        btn_generate_bill = Button(widget_frame, text="Generate \n Save Bill",command=self.generate_bill,font=("times new roman",15,"bold"),bg="#005249",cursor="hand2",fg="white")
        btn_generate_bill.place(x=270,y=60,width=120,height=45)

        lbl_footer = Label(self.root, text="IMS - Inventory Management System | Developed by Aaryan\n For any Techincal Issue Contact : 7447499360",font=("times new roman",12),bg="#4d636d",fg="white")
        lbl_footer.pack(side=BOTTOM, fill=X)

        self.show()
        self.update_date_time()

    def get_input(self,num):
        xnum = self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)


    def clear_cal(self):
        self.var_cal_input.set('')


    def perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))        


    def show(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from PRO where status = 'Active'")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
        except Exception as ex:    
            messagebox.showerror("Error",f"Error due to: {str(ex)}", self.root)


    def search(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error","Search input should be required", parent=self.root)
            else:    
                cur.execute("select pid,name,price,qty,status from PRO where name LIKE '%"+self.var_search.get()+"%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No records found!!",parent=self.root)        

        except Exception as ex:    
            messagebox.showerror("Error",f"Error due to: {str(ex)}", parent=self.root)
        
    def get_data(self,ev):
        f = self.ProductTable.focus()
        content = (self.ProductTable.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')


    def get_data_cart(self,ev):
        f = self.CartTable.focus()
        content = (self.CartTable.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])
    


    def add_update_cart(self):
        if self.var_pid.get() == '':
            messagebox.showerror('Error',"Please select product from the list", parent=self.root)
        elif self.var_qty.get() == '':
            messagebox.showerror('Error',"Quantity is required", parent=self.root)
        elif int(self.var_qty.get())> int(self.var_stock.get()):
            messagebox.showerror('Error',"Invalid Quantity", parent=self.root)
        else:
            price_cal = self.var_price.get()
            cart_data = [self.var_pid.get(), self.var_pname.get(),price_cal, self.var_qty.get(),self.var_stock.get()]

            present = 'no'
            index_ = 0
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = 'yes'
                    break
                index_ += 1        
            if present == 'yes':
                op = messagebox.askyesno('Confirm',"Product already present \n Do you want to Update | Remove from the Cart List", parent=self.root)
                if op == True:
                    if self.var_qty.get() == "0":
                        self.cart_list.pop(index_)                
                    else:
                        #self.cart_list[index_][2] = price_cal
                        self.cart_list[index_][3] = self.var_qty.get()
            else:
                self.cart_list.append(cart_data)
        self.show_cart()
        self.bill_updates()

    
    def bill_updates(self):
        self.bill_amount = 0
        self.net_pay = 0
        self.discount = 0
        for row in self.cart_list:
            self.bill_amount = self.bill_amount+((float(row[2]))*int(row[3]))
        
        self.discount = float((self.bill_amount * 5)*100)
        self.net_pay = float(self.bill_amount - self.discount)
        self.lbl_bill_amount.config(f'Bill Amt (Rs.)\n {str(self.bill_amount)}')
        self.lbl_net_pay.config(f'Net Pay (Rs.)\n {str(self.net_pay)}')    
        self.cart_title.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")


    def show_cart(self):
        try:
            self.CartTable.delete(*self.ProductTable.get_children())
            for row in self.cart_list:
                self.self.CartTable.insert('',END,values=row)
        except Exception as ex:    
            messagebox.showerror("Error",f"Error due to: {str(ex)}", parent=self.root)


    def generate_bill(self):
        if self.var_cname.get() == '' or self.var_contact.get() == '':
            messagebox.showerror("Error", "Customer Details are required", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror("Error", "Please add some product to the cart", parent=self.root)
        else:
            self.bill_top()  
            self.bill_middle()  
            self.bill_bottom()

            fp = open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved',"Bill has been Generated and Saved in Backend", parent=self.root)
            self.chk_print = 1


    def print_bill(self):
        if self.chk_print == 1:
            messagebox.showinfo('Print',"PLease wait while printing",parent=self.root)
            new_file = tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror('Print',"Please Generate Bill First",parent=self.root)
            
    
    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_temp = f'''
\t\t XYZ - Inventory 
\t Phone Number 98725*****, Delhi-125001
{str("="*47)}
 Customer Name: {self.var_cname.get()}
 Phone No. {str(self.invoice)} \t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
 Product Name\t\t\tQTY\tPrice
{str("="*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)


    def bill_middle(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            for row in self.cart_list:
                pid = row[0]
                Name = row[1]
                QTY = int(row[4]) - int(row[3])
                if int(row[3]) == int(row[4]):
                    status = 'Inactive'
                if int(row[3]) != int(row[4]):
                    status = 'Active'

                Price = float(row[2])*int(row[3])
                Price = str(Price)
                self.txt_bill_area.insert(END,"\n "+Name+"\t\t\t"+row[3]+"\tRs."+Price)

                cur.execute('update PRO set qty=?,status=? where pid=?',(
                    QTY,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:    
            messagebox.showerror("Error",f"Error due to: {str(ex)}", self.root)

    
    def bill_bottom(self):
        bill_bottom_temp = f'''
{str("="*47)}
 Bill Amount\t\t\t\tRs.{self.bill_amount}
 CGST\t\t\t\tRs.{self.cgst}
 SGST\t\t\t\tRs.{self.sgst}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*47)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)  


    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_instock.config(text=f"In Stock")
        self.var_stock.set('')     


    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact
        self.txt_bill_area.delete('1.0',END)
        self.chk_print = 0
        self.cart_title.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()    
        self.show_cart()


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
    obj = BillClass(root)
    root.mainloop()   