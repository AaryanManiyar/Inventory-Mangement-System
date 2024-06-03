from tkinter import * 
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib
import time

class Login_system:
    def __init__(self,root):
        self.root = root
        self.root.title("Login System | Developed by Aaryan")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")

        self.otp = ''

        self.phone_image = ImageTk.PhotoImage(file="images/phone.png")
        self.lbl_phone_image = Label(self.root, image=self.phone_image,bd=0)
        self.lbl_phone_image.place(x=200,y=50)

        login_frame = Frame(self.root,bd=2,relief=RIDGE,bg="White")
        login_frame.place(x=650,y=90,width=350,height=560)

        login_title = Label(login_frame, text="Login System", font=("times new roman",33,"bold"),bg="white")
        login_title.place(x=0,y=50,relwidth=1)

        lbl_user = Label(login_frame, text="Employee ID", font=("times new roman",20),bg="white",fg="#767171")
        lbl_user.place(x=30,y=150)
        self.emp_id = StringVar()
        txt_user = Entry(login_frame,textvariable=self.emp_id,font=("times new roman",17),bg="lightyellow")
        txt_user.place(x=30,y=190,width=270)

        lbl_password = Label(login_frame, text="Password", font=("times new roman",20),bg="white",fg="#767171")
        lbl_password.place(x=30,y=240)
        self.password = StringVar()
        txt_password = Entry(login_frame,textvariable=self.password,show="*",font=("times new roman",17),bg="lightyellow")
        txt_password.place(x=30,y=280,width=270)
        
        btn_login = Button(login_frame, text="Log In",command=self.login,font=("times new roman",15,"bold"),bg="#00B0F0",cursor="hand2",activebackground="#00B0F0",fg="white",activeforeground="white")
        btn_login.place(x=30,y=350,width=270)

        lbl_or = Label(login_frame, text="-----------------OR-----------------", font=("times new roman",15),bg="white",fg="#767171")
        lbl_or.place(x=30,y=450)

        btn_forget_pass = Button(login_frame, text="Forget Password ?", command=self.forget_window,font=("times new roman",15),bg="white",fg="#00759E",bd=0,activebackground="white")
        btn_forget_pass.place(x=90,y=500)

        self.im1 = ImageTk.PhotoImage(file="images/im1.png")
        self.im2 = ImageTk.PhotoImage(file="images/im2.png")
        self.im3 = ImageTk.PhotoImage(file="images/im3.png")

        self.lbl_change_image = Label(self.root,bg="green")
        self.lbl_change_image.place(x=367,y=150,width=240,height=430)
        self.animate()
        #self.send_email('xyz')

    def animate(self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000,self.animate)


    def login(self):
        con = sqlite3.connect(database = r'IMS.db')
        cur = con.cursor()
        try:
            if self.emp_id.get() == "" or self.password.get() == "":
                messagebox.showerror('Error',"All fields are required", parent=self.root)
            else:
                cur.execute("select utype from EMP where emp_id = ? AND password = ?",(self.emp_id.get(),self.password.get()))
                user = cur.fetchone() 
                if user == None:
                    messagebox.showerror('Error',"Invalid Employee ID and Password",parent=self.root)
                else:
                    if user[0] == "Admin":
                        self.root.destroy()
                        os.system("python main.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}", parent=self.root)

    def forget_window(self):
        con = sqlite3.connect(database=r'IMS.db')
        cur = con.cursor()
        try:
            if self.emp_id.get() == "":
                messagebox.showerror('Error',"Employee ID must be required", parent=self.root)
            else:
                cur.execute("select email from EMP where emp_id = ?",(self.emp_id.get(),))
                email = cur.fetchone() 
                if email == None:
                    messagebox.showerror('Error',"Invalid Employee ID, Try Again!!",parent=self.root)
                else:
                    self.var_OTP = StringVar()
                    self.var_new_pass = StringVar()
                    self.var_confirm_new_pass = StringVar()
                    chk = self.send_email(email[0])
                    if chk != 's':
                        messagebox.showerror('Error',"Connection Error, Try Again", parent=self.root)
                    else:
                        self.forget_win = Toplevel(self)
                        self.forget_win.title('RESET PASSWORD')
                        self.forget_win.geometry('400x350+500+100')
                        self.forget_win.focus_force()

                        title = Label(self.forget_win, text="Reset Password",font=("times new roman",15,"bold"),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)

                        lbl_reset = Label(self.forget_win, text="Enter OTP sent on Registered Email", font=("times new roman",15)).place(x=20,y=60)
                        txt_reset = Entry(self.forget_win,textvariable=self.var_OTP,font=("times new roman",15),bg="lightyellow").place(x=20,y=100,width=250,height=30)
                    
                        self.btn_reset = Button(self.forget_win, text="Sumit",command=self.validate_otp,font=("times new roman",15),bg="lightblue")
                        self.btn_reset.place(x=280,y=100,width=100,height=30)

                        lbl_new_pass = Label(self.forget_win, text="Enter New Password", font=("times new roman",15)).place(x=20,y=160)
                        txt_new_pass = Entry(self.forget_win,textvariable=self.var_new_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=190,width=250,height=30)
                            
                        lbl_confirm_pass = Label(self.forget_win, text="Enter Confirm Password", font=("times new roman",15)).place(x=20,y=225)
                        txt_confirm_pass = Entry(self.forget_win,textvariable=self.var_confirm_new_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=255,width=250,height=30)
        
                        self.btn_update = Button(self.forget_win,command=self.update_password,text="Update",state=DISABLED,font=("times new roman",15),bg="lightblue")
                        self.btn_update.place(x=150,y=300,width=100,height=30)

        except Exception as ex:
            messagebox.showerror('Error',f"Error due to: {str(ex)}", parent=self.root)    


    def update_password(self):
        if  self.var_new_pass.get() == "" or self.var_confirm_new_pass.get() == "":
            messagebox.showerror("Error","Password is required", parent=self.forget_win)
        elif (self.var_new_pass.get()) != (self.var_confirm_new_pass.get()):
            messagebox.showerror("Error","New Password & Confirm Password must be Same", parent=self.forget_win)
        else:
            con = sqlite3.connect(database=r'IMS.db')
            cur = con.cursor()
            try:
                cur.execute('update EMP SET password=? where emp_id=?',(self.var_new_pass.get(),self.emp_id.get()))                          
                con.commit()
                messagebox.showinfo("Success","Password Updated Successfully!!",parent=self.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror('Error',f"Error due to: {str(ex)}", parent=self.root)    
     
    
    def validate_otp(self):
        if int(self.otp) == int(self.validate_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error","Invalid OTP, Try Again",parent=self.forget_win)  
    
    
    def send_email(self,to_):
        s = smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_ = email_pass.email_
        pass_ = email_pass.pass_

        s.login(email_,pass_)

        self.otp = int(str(time.strftime("%H%S%M")))+int(str(time.strftime("%S")))

        subj = 'IMS - Reset Password OTP'

        mgs = f'Respected Sir/Madam, \n\nYour Reset OTP is {str(self.otp)}. \n\n With Regeards,\nIMS Team'

        mgs = "Subject:{}\n\n{}".format(subj,mgs)
        s.sendmail(email_,to_,mgs)

        chk = s.ehlo()
        if chk[0] == 250:
            messagebox.showinfo('Success','OTP Sent Successfully')
        else:
            messagebox.showerror('Error','OTP Not Sent')



root = Tk()
obj = Login_system(root)
root.mainloop()