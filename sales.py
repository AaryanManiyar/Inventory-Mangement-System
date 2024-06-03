from tkinter import  *
from PIL import Image,ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os

class salesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed by Aaryan")
        self.root.config(bg="White")
        self.root.focus_force()

        self.bill_list = []
        self.var_invoice = StringVar()

        title = Label(self.root, text="Customer Bill Reports", font=("times new roman",25),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X,padx=10,pady=20)

        lbl_voice = Label(self.root, text="Invoice No.", font=("times new roman",15),bg="white").place(x=50,y=100)
        txt_voice = Entry(self.root, textvariable=self.var_invoice, font=("times new roman",15),bg="lightyellow").place(x=185,y=100,width=180)

        btn_search = Button(self.root,text="Search",command=self.search,font=("times new roman",15,"bold"),bg="red",fg="black",cursor="hand2").place(x=400,y=100,width=110,height=28)
        btn_clear = Button(self.root,text="Clear",command=self.clear,font=("times new roman",15,"bold"),bg="red",fg="black",cursor="hand2").place(x=550,y=100,width=110,height=28)

        self.im1 = Image.open("images/cat2.jpg")
        self.im1 = self.im1.resize((350,350))
        self.im1 = ImageTk.PhotoImage(self.im1)
        self.lbl_im1 = Label(self.root, image = self.im1)
        self.lbl_im1.place(x=700,y=100)
    
        
        sales_frame = Frame(self.root,bd=3,relief=RIDGE)
        sales_frame.place(x=50,y=140,width=200,height=330)
        scrolly = Scrollbar(sales_frame, orient=VERTICAL)
        self.sales_list = Listbox(sales_frame,font=("times new roman",15),bg="white", yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.sales_list.yview)
        self.sales_list.pack(fill=BOTH, expand=1)
        self.sales_list.bind("<ButtonRelease-1>", self.get_data)

        bill_frame = Frame(self.root,bd=3,relief=RIDGE)
        bill_frame.place(x=280,y=140,width=375,height=330)
        title2 = Label(bill_frame, text="Customer Bill Area", font=("times new roman",20),bg="orange").pack(side=TOP,fill=X)
        scrolly = Scrollbar(bill_frame, orient=VERTICAL)
        self.bill_area = Text(bill_frame,font=("times new roman",15),bg="lightyellow", yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.sales_list.yview)
        self.bill_area.pack(fill=BOTH, expand=1)

        self.show()

    def show(self):
        del self.bill_list[:]
        self.sales_list.delete(0,END)
        for i in os.listdir('bill'):
            if i.split('.')[-1]=='txt':
                self.sales_list.insert(END,i)
                self.bill_list.append(i.split('.')[0])


    def get_data(self,ev):
        index_ = self.sales_list.curselection()
        file_name = self.sales_list.get(index_)
        print(file_name)
        self.bill_area.delete('1.0',END)
        fp = open(f'bill/{file_name}','r')
        for i in fp:
            self.bill_area.insert(END, i)
        fp.close()     


    def search(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Invoice number is required", parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                fp = open(f'bill/{self.var_invoice.get()}.txt','r')
                self.bill_area.delete('1.0',END)
                for i in fp:
                    self.bill_area.insert(END, i)
                fp.close()
            else:
                messagebox.showerror("Error","Invalid Invoice No.", parent=self.root)


    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)




if __name__=="__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()           