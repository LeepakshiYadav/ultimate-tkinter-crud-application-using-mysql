from tkinter import *
from tkinter import Tk,ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector as connector

#Contains all functions requiring database connection
class db:
    def __init__(self):
        self.cnx=connector.connect(host='localhost',
                port='3306',
                user='root',
                password='root',
                database='mydb') 
        self.cnx.autocommit=True
        self.cur=self.cnx.cursor(dictionary=True)
        
        # user table
        def create_usertable():
            user_table="""create table if not exists user(
                user_id varchar(20) not NULL primary key, 
                name varchar(255) not NULL,
                father_name varchar(255) not NULL,
                mother_name varchar(255) not NULL,
                address varchar(255) not NULL,
                phone varchar(12) not NULL,
                doj datetime default now(),
                cur_fee int not NULL,
                password varchar(100) default 1234
                );
                """
            self.cur.execute(user_table)

        def create_feetable():
            fee_table="""create table if not exists feedata(
                user_id varchar(20) not NULL,
                payment_date varchar(10) not NULL,
                payment_month varchar(10) not NULL,
                payment_year int not NULL,
                amount int not NULL,
                balance int,
                remarks varchar(200),
                foreign key(user_id) references user(user_id) ON UPDATE CASCADE ON DELETE CASCADE
                );
                """
            self.cur.execute(fee_table)

        def create_admintable():
            admin_table="""create table if not exists admin(
                admin_id varchar(20) not NULL primary key, 
                name varchar(255) not NULL,
                password varchar(100) not NULL
                );
                """
            self.cur.execute(admin_table)

        try:
            create_usertable()
            create_feetable()
            create_admintable()
            print("Created")
        except Exception as e:
            print(e)

    def endcon(self):
        self.cnx.close()  

    def user_login(self,u_id,u_pass,obj):
        if u_id=="" or u_pass=="":
            messagebox.showwarning("Error","Please fill both the fields")
        else:
            query="SELECT * FROM user WHERE user_id='{}' and password='{}'".format(u_id,u_pass)
            self.cur.execute(query)
            a1=self.cur.fetchone()
            if(a1==None):
                messagebox.showerror("Invalid","Invalid user-id and password")
            else:
                self.user_panel_window(obj,u_id)

    def admin_login(self,a_id,a_pass,obj):
        if a_id=="" or a_pass=="":
            messagebox.showwarning("Error","Please fill both the fields")
        else:
            query="SELECT * FROM admin WHERE admin_id='{}' and password='{}'".format(a_id,a_pass)
            self.cur.execute(query)
            a1=self.cur.fetchone()
            if(a1==None):
                messagebox.showerror("Invalid","Invalid admin-id and password")
            else:
                self.admin_panel_window(obj)

    def user_add(self,u_id1,u_n,u_fn,u_mn,u_a,u_p,u_f,obj):
        if u_id1=="" or u_a=="" or u_n=="" or u_mn=="" or u_fn=="" or u_p=="" or u_f=="":
            messagebox.showwarning("Error","Please fill all the fields")
        else:
            query="SELECT * FROM user WHERE user_id='{}'".format(u_id1)
            self.cur.execute(query)
            a1=self.cur.fetchone()
            if(a1==None):
                query="""INSERT INTO user (user_id,name,father_name,mother_name,address,phone,cur_fee)
                values('{}','{}','{}','{}','{}','{}',{})""".format(u_id1,u_n,u_fn,u_mn,u_a,u_p,u_f)
                self.cur.execute(query)
                messagebox.showinfo("Alert","Data Added")
                self.fetch_user_data(obj)
                obj.clear()
            else:
                messagebox.showerror("Error", "User Id already taken")

    def fee_add(self,u_id,u_pd,u_pm,u_py,u_a,u_b,u_r,obj):
        if u_id=="" or u_pd=="" or u_pm=="" or u_py=="" or u_a=="":
            messagebox.showwarning("Error","First 5 fields necessary")
        else:
            query="SELECT * FROM user WHERE user_id='{}'".format(u_id)
            self.cur.execute(query)
            a1=self.cur.fetchone()
            if(a1==None):
                messagebox.showerror("Error", "User Id does not exists")
            else:
                if u_b=='':
                    u_b=0
                query="""INSERT INTO feedata (user_id,payment_date,payment_month,payment_year,amount,balance,remarks) values('{}','{}','{}',{},{},{},'{}')""".format(u_id,u_pd,u_pm,u_py,u_a,u_b,u_r)
                print(query)
                self.cur.execute(query)
                messagebox.showinfo("Alert","Payment record added")
                self.fetch_fee_data(obj)
                obj.clear()

    def show_data(self,obj,id):
        query="SELECT * FROM user WHERE user_id='{}'".format(id)
        self.cur.execute(query)
        a1=self.cur.fetchone()
        obj.txtBox.insert(END,"USER ID:\t\t"+ a1['user_id']+"\n")
        obj.txtBox.insert(END,"Name::\t\t"+ a1['name']+"\n" )
        obj.txtBox.insert(END,"Father's Name:\t\t"+ a1['father_name']+"\n" )
        obj.txtBox.insert(END,"Mother's Name:\t\t"+ a1['mother_name']+"\n")
        obj.txtBox.insert(END,"Address:\t\t"+ a1['address']+"\n")
        obj.txtBox.insert(END,"Phone no:\t\t"+ a1['phone']+"\n")
        obj.txtBox.insert(END,"Current fee:\t\t"+ str(a1['cur_fee'])+"\n")
                

    def user_update(self,u_id1,u_n,u_fn,u_mn,u_a,u_p,u_f,obj):
        if u_id1=="" or u_a=="" or u_n=="" or u_mn=="" or u_fn=="" or u_p=="" or u_f=="":
            messagebox.showwarning("Error","Please fill all the fields")
        else:
            query="SELECT * FROM user WHERE user_id='{}'".format(u_id1)
            self.cur.execute(query)
            a1=self.cur.fetchone()
            if(a1==None):
                messagebox.showerror("Error", "User ID does not exists")               
            else:
                query="""UPDATE user SET name='{}',father_name='{}',mother_name='{}',address='{}',phone='{}',cur_fee={}
                WHERE user_id='{}'""".format(u_n,u_fn,u_mn,u_a,u_p,u_f,u_id1)
                self.cur.execute(query)
                messagebox.showinfo("Alert","Data Updated")
                self.fetch_user_data(obj)
                obj.clear()

    def password_update(self,id,p,p1,p2):
        if p1=="":
            messagebox.showerror("Error","Password can't be empty")
        elif p1!=p2:
            messagebox.showerror("Error","password and confirm password does not matches")
        else:
            query="SELECT * FROM user WHERE user_id='{}' and password='{}'".format(id,p)
            self.cur.execute(query)
            a1=self.cur.fetchone()
            if(a1==None):
                messagebox.showerror("Error", "Incorrect current password given")               
            else:
                query="""UPDATE user SET password='{}'
                WHERE user_id='{}'""".format(p1,id)
                self.cur.execute(query)
                messagebox.showinfo("Alert","Password updated successfully")

    def user_delete(self,u_id1,obj):
        if u_id1=="":
            messagebox.showwarning("Error","User ID requied for deletion")
        else:
            query="SELECT * FROM user WHERE user_id='{}'".format(u_id1)
            self.cur.execute(query)
            a1=self.cur.fetchone()
            if(a1==None):
                messagebox.showerror("Error", "User ID does not exists")               
            else:
                query="""DELETE from user WHERE user_id='{}'""".format(u_id1)
                print(query)
                self.cur.execute(query)
                messagebox.showinfo("Alert","Data Deleted Sucessfully")
                self.fetch_user_data(obj)
                obj.clear()

    def search_user_data(self,str1,str2,obj):
        query="""SELECT * FROM user where """+str(str1)+""" like "%"""+str(str2)+"""%" """
        self.cur.execute(query)
        rows=self.cur.fetchall()
        if len(rows)==0:
            obj.Student_table.delete(*obj.Student_table.get_children())
            messagebox.showerror("Alert","No search results found")
        else:
            obj.Student_table.delete(*obj.Student_table.get_children())
            for i in rows:
                obj.Student_table.insert("",END,values=(i['user_id'],i['name'],i['father_name'],i['mother_name'],i['address'],i['phone'],i['cur_fee']))

    def search_fee_data(self,str1,str2,obj):
        query="""SELECT * FROM feedata where """+str(str1)+""" like "%"""+str(str2)+"""%" """
        self.cur.execute(query)
        rows=self.cur.fetchall()
        if len(rows)==0:
            obj.Fee_table.delete(*obj.Fee_table.get_children())
            messagebox.showerror("Alert","No search results found")
        else:
            obj.Fee_table.delete(*obj.Fee_table.get_children())
            for i in rows:
                obj.Fee_table.insert("",END,values=(i['user_id'],i['payment_date'],i['payment_month'],i['payment_year'],i['amount'],i['balance'],i['remarks']))

    def fetch_user_data(self,obj):
        query="SELECT * FROM user"
        self.cur.execute(query)
        rows=self.cur.fetchall()
        if len(rows)==0:
            messagebox.showerror("Underflow","No data found")
        else:
            obj.Student_table.delete(*obj.Student_table.get_children())
            for i in rows:
                obj.Student_table.insert("",END,values=(i['user_id'],i['name'],i['father_name'],i['mother_name'],i['address'],i['phone'],i['cur_fee']))
    
    def search_student_fee_data(self,str1,str2,id,obj):
        query="""SELECT * FROM feedata where """+str(str1)+""" like """+str(str2)+""" and user_id='{}'""".format(id)
        self.cur.execute(query)
        rows=self.cur.fetchall()
        if len(rows)==0:
            obj.Fee_table.delete(*obj.Fee_table.get_children())
            messagebox.showerror("Alert","No search results found")
        else:
            obj.Fee_table.delete(*obj.Fee_table.get_children())
            for i in rows:
                obj.Fee_table.insert("",END,values=(i['payment_date'],i['payment_month'],i['payment_year'],i['amount'],i['balance'],i['remarks']))

    def fetch_student_fee_data(self,id,obj):
        query="SELECT * FROM feedata where user_id = '{}'".format(id)
        self.cur.execute(query)
        rows=self.cur.fetchall()
        if len(rows)==0:
            messagebox.showerror("Underflow","No record found")
        else:
            obj.Fee_table.delete(*obj.Fee_table.get_children())
            for i in rows:
                obj.Fee_table.insert("",END,values=(i['payment_date'],i['payment_month'],i['payment_year'],i['amount'],i['balance'],i['remarks']))

    def fetch_fee_data(self,obj):
        query="SELECT * FROM feedata"
        self.cur.execute(query)
        rows=self.cur.fetchall()
        if len(rows)==0:
            messagebox.showerror("Underflow","No record found")
        else:
            obj.Fee_table.delete(*obj.Fee_table.get_children())
            for i in rows:
                obj.Fee_table.insert("",END,values=(i['user_id'],i['payment_date'],i['payment_month'],i['payment_year'],i['amount'],i['balance'],i['remarks']))

    def admin_panel_window(self,obj):
        obj.close()
        p=Admin_panel()

    def user_panel_window(self,obj,id):
        obj.close()
        p=Student_panel(id)

#Constructor called to set-up initial data base connection, and create necessary tables if npt already created
db1=db()

#For user login page
class Login:
    def __init__(self):
        self.w=Tk()
        self.w.title("Login")
        self.w.geometry('1550x800+-7+0') #width,height,starting x-coordinate,starting y-coordinate
        self.bg=ImageTk.PhotoImage(file=r"D:\tkinter-project\path.jpg")
        label_bg=Label(self.w,image=self.bg)
        label_bg.place(x=0,y=0,relwidth=1,relheight=1)

        frame=Frame(self.w,bg="black")
        frame.place(x=610,y=170,width=340,height=450)

        img1=Image.open(r"D:\tkinter-project\pen.png")
        img1=img1.resize((100,100),Image.ANTIALIAS)
        self.im1=ImageTk.PhotoImage(img1)
        l_img1=Label(image=self.im1,bg="black",borderwidth=0)
        l_img1.place(x=730,y=175,width=100,height=100)

        L1=Label(frame,text="User Login",fg="white",bg="black",font=("times new roman",20,"bold"))
        L1.place(x=95,y=105)

        L2=Label(frame,text="User ID:",fg="white",bg="black",font=("times new roman",15))
        L2.place(x=40,y=160)

        self.u_id=ttk.Entry(frame,font=("times new roman",15))
        self.u_id.place(x=40,y=190,width=270)

        L3=Label(frame,text="User Password:",fg="white",bg="black",font=("times new roman",15))
        L3.place(x=40,y=230)

        self.u_pass=ttk.Entry(frame,font=("times new roman",15))
        self.u_pass.place(x=40,y=260,width=270)

        B1=Button(frame,text="Login",command=lambda:db1.user_login(self.u_id.get(),self.u_pass.get(),self),font=("times new roman",15,"bold"),bd=3,bg="purple",fg="white",relief=RIDGE)
        B1.place(x=128,y=330)

        B2=Button(frame,text="Login as admin",command=self.open_admin_window,font=("times new roman",12),borderwidth=0,bg="black",fg="white",activebackground="black",activeforeground="yellow")
        B2.place(x=40,y=380)

        self.w.mainloop()

    def open_admin_window(self):
        self.close()
        a=Admin_Login()
    
    def close(self):
        self.w.destroy()

#for admin panel (crud user, add/view fee)
class Admin_panel:
    def __init__(self):
        self.w1=Tk()
        self.w1.title("Admin Panel")
        self.w1.geometry('1550x800+-7+0') #width,height,starting x-coordinate,starting y-coordinate
        bg=ImageTk.PhotoImage(file=r"D:\tkinter-project\palm.jpg")
        label_bg=Label(image=bg)
        label_bg.place(x=0,y=0,relwidth=1,relheight=1)

        frame=Frame(self.w1,bg="black")
        frame.place(x=850,y=100,width=500,height=650)

        L1=Label(frame,text="Admin Panel",fg="yellow",bg="black",font=("times new roman",25,"underline"))
        L1.place(x=170,y=30)

        B1=Button(frame,text="CRUD User",command=lambda:self.open_student(),font=("times new roman",15,"bold"),bd=3,bg="white",fg="black",relief=RIDGE)
        B1.place(x=50,y=150)

        B2=Button(frame,text="Add/View Fee",command=lambda:self.open_fee(),font=("times new roman",15,"bold"),bd=3,bg="white",fg="black",relief=RIDGE)
        B2.place(x=50,y=220)

        B7=Button(frame,text="Exit",command=self.close,font=("times new roman",15,"bold"),bd=3,bg="white",fg="black",relief=RIDGE)
        B7.place(x=50,y=290)
        self.w1.mainloop()

    def open_student(self):
        self.close()
        a=Student()

    def open_fee(self):
        self.close()
        a=Fees()

    def close(self):
        self.w1.destroy()


#for admin login
class Admin_Login:
    def __init__(self):

        self.w3=Tk()
        self.w3.title("Admin Login")
        self.w3.geometry('1550x800+-7+0') #width,height,starting x-coordinate,starting y-coordinate
        self.bg=ImageTk.PhotoImage(file=r"D:\tkinter-project\path.jpg")
        label_bg=Label(self.w3,image=self.bg)
        label_bg.place(x=0,y=0,relwidth=1,relheight=1)

        frame=Frame(self.w3,bg="black")
        frame.place(x=610,y=170,width=340,height=450)

        img1=Image.open(r"D:\tkinter-project\pen.png")
        img1=img1.resize((100,100),Image.ANTIALIAS)
        self.im1=ImageTk.PhotoImage(img1)
        l_img1=Label(image=self.im1,bg="black",borderwidth=0)
        l_img1.place(x=730,y=175,width=100,height=100)

        L1=Label(frame,text="Admin Login",fg="white",bg="black",font=("times new roman",20,"bold"))
        L1.place(x=95,y=105)

        L2=Label(frame,text="Admin ID:",fg="white",bg="black",font=("times new roman",15))
        L2.place(x=40,y=160)

        self.a_id=ttk.Entry(frame,font=("times new roman",15))
        self.a_id.place(x=40,y=190,width=270)

        L3=Label(frame,text="Admin Password:",fg="white",bg="black",font=("times new roman",15))
        L3.place(x=40,y=230)

        self.a_pass=ttk.Entry(frame,font=("times new roman",15))
        self.a_pass.place(x=40,y=260,width=270)

        B1=Button(frame,text="Login",command=lambda:db1.admin_login(self.a_id.get(),self.a_pass.get(),self),font=("times new roman",15,"bold"),bd=3,bg="purple",fg="white",relief=RIDGE)
        B1.place(x=128,y=330)

        B2=Button(frame,text="Login as User",command=self.open_user_window,font=("times new roman",12),borderwidth=0,bg="black",fg="white",activebackground="black",activeforeground="yellow")
        B2.place(x=40,y=380)

        self.w3.mainloop()

    def open_user_window(self):
        self.close()
        a=Login()

    def close(self):
        self.w3.destroy()

#crud user (Stdent management panel)
class Student:
    def __init__ (self):
        self.w4=Tk()
        self.w4.title("Student Management Panel")
        self.w4.geometry('1550x800+-7+0') #width,height,starting x-coordinate,starting y-coordinate
        
        self.bg=ImageTk.PhotoImage(file=r"D:\tkinter-project\butterfly.jpg")
        label_bg=Label(self.w4,image=self.bg)
        label_bg.place(x=0,y=0,relwidth=1,relheight=1)

        title=Label(self.w4,text="Student Management Panel",font=("times new roman",50,"bold"),bd=9,relief=GROOVE,bg="purple",fg="white")
        title.pack(side=TOP,fill=X)

        frame1=Frame(self.w4,bg="white",bd=4,relief=RIDGE)
        frame1.place(x=20,y=150,width=430,height=700)

        L4=Label(frame1,text="Name:",fg="black",bg="white",font=("times new roman",15))
        L4.place(x=40,y=30)
        self.u_n=ttk.Entry(frame1,font=("times new roman",15))
        self.u_n.place(x=40,y=60,width=330)

        L5=Label(frame1,text="Father's Name:",fg="black",bg="white",font=("times new roman",15))
        L5.place(x=40,y=100)
        self.u_fn=ttk.Entry(frame1,font=("times new roman",15))
        self.u_fn.place(x=40,y=130,width=330)

        L6=Label(frame1,text="Mother's Name:",fg="black",bg="white",font=("times new roman",15))
        L6.place(x=40,y=170)
        self.u_mn=ttk.Entry(frame1,font=("times new roman",15))
        self.u_mn.place(x=40,y=200,width=330)

        L7=Label(frame1,text="Phone no:",fg="black",bg="white",font=("times new roman",15))
        L7.place(x=40,y=240)
        self.u_p=ttk.Entry(frame1,font=("times new roman",15))
        self.u_p.place(x=40,y=270,width=330)

        L8=Label(frame1,text="Address:",fg="black",bg="white",font=("times new roman",15))
        L8.place(x=40,y=310)
        self.u_a=ttk.Entry(frame1,font=("times new roman",15))
        self.u_a.place(x=40,y=340,width=330)

        L9=Label(frame1,text="USER ID:",fg="black",bg="white",font=("times new roman",15))
        L9.place(x=40,y=380)
        self.u_id1=ttk.Entry(frame1,font=("times new roman",15))
        self.u_id1.place(x=40,y=410,width=330)

        L10=Label(frame1,text="Student fee:",fg="black",bg="white",font=("times new roman",15))
        L10.place(x=40,y=450)
        self.u_f=ttk.Entry(frame1,font=("times new roman",15))
        self.u_f.place(x=40,y=480,width=330)

        B1=Button(frame1,text="Add",command=lambda:db1.user_add(self.u_id1.get(),self.u_n.get(),self.u_fn.get(),self.u_mn.get(),self.u_a.get(),self.u_p.get(),self.u_f.get(),self),font=("times new roman",15,"bold"),bg="purple",fg="white",relief=RIDGE)
        B1.place(x=40,y=540)

        B2=Button(frame1,text="Update",command=lambda:db1.user_update(self.u_id1.get(),self.u_n.get(),self.u_fn.get(),self.u_mn.get(),self.u_a.get(),self.u_p.get(),self.u_f.get(),self),font=("times new roman",15,"bold"),bg="purple",fg="white",relief=RIDGE)
        B2.place(x=110,y=540)

        B3=Button(frame1,text="Delete",command=lambda:db1.user_delete(self.u_id1.get(),self),font=("times new roman",15,"bold"),bg="purple",fg="white",relief=RIDGE)
        B3.place(x=205,y=540)

        B4=Button(frame1,text="Clear",command=self.clear,font=("times new roman",15,"bold"),bg="purple",fg="white",relief=RIDGE)
        B4.place(x=295,y=540)

        B8=Button(frame1,text="Add/View Fee",command=lambda:self.open_fee(),font=("times new roman",15,"bold"),bd=3,bg="white",fg="purple",relief=RIDGE)
        B8.place(x=140,y=590)


        frame2=Frame(self.w4,bg="white",bd=4,relief=RIDGE)
        frame2.place(x=500,y=150,width=1000,height=600)

        lbl_search=Label(frame2,text="Search by",font=("times new roman",20),bg="white")
        lbl_search.grid(row=0,column=0,pady=10,padx=20,sticky="w")

        self.combo=ttk.Combobox(frame2,font=("times new roman",15),state='readonly')
        self.combo['values']=("user_id","name","father_name","mother_name","address","phone","cur_fee")
        self.combo.current(0)
        self.combo.grid(row=0,column=1,padx=20,pady=10,sticky="w")

        self.search=ttk.Entry(frame2,font=("times new roman",15))
        self.search.grid(row=0,column=2,padx=20,pady=10,sticky="w")

        B5=Button(frame2,text="Search",command=lambda:db1.search_user_data(self.combo.get(),self.search.get(),self),font=("times new roman",15,"bold"),bg="purple",fg="white",relief=RIDGE)
        B5.grid(row=0,column=3,padx=20,pady=10,sticky="w")

        B6=Button(frame2,text="View All",command=lambda:db1.fetch_user_data(self),font=("times new roman",15,"bold"),bg="purple",fg="white",relief=RIDGE)
        B6.grid(row=0,column=4,padx=20,pady=10,sticky="w")


        frame3=Frame(frame2,bg="purple",bd=4,relief=RIDGE)
        frame3.place(x=50,y=70,width=900,height=500)

        scroll_x=Scrollbar(frame3,orient=HORIZONTAL)
        scroll_y=Scrollbar(frame3,orient=VERTICAL)

        self.Student_table=ttk.Treeview(frame3,columns=("user_id","name","father_name","mother_name","address","phone","cur_fee"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x.config(command=self.Student_table.xview)
        scroll_y.config(command=self.Student_table.yview)

        self.Student_table.heading("user_id",text="User ID")
        self.Student_table.heading("name",text="Name")
        self.Student_table.heading("father_name",text="Father's name")
        self.Student_table.heading("mother_name",text="Mother's name")
        self.Student_table.heading("address",text="Address")
        self.Student_table.heading("phone",text="Phone no")
        self.Student_table.heading("cur_fee",text="Fees")

        self.Student_table["show"]="headings"
        self.Student_table.pack(fill=BOTH,expand=1)

        self.Student_table.column('user_id',width=100)
        self.Student_table.column('name',width=100)
        self.Student_table.column('father_name',width=100)
        self.Student_table.column('mother_name',width=100)
        self.Student_table.column('address',width=150)
        self.Student_table.column('phone',width=100)
        self.Student_table.column('cur_fee',width=100)

        self.Student_table.bind("<ButtonRelease-1>",self.get_cursor)

        self.w4.mainloop()

    def clear(self):
        self.u_id1.delete(0,END)
        self.u_a.delete(0,END)
        self.u_f.delete(0,END)
        self.u_fn.delete(0,END)
        self.u_mn.delete(0,END)
        self.u_p.delete(0,END)
        self.u_n.delete(0,END)
        self.search.delete(0,END)

    def get_cursor(self,event=""):
        self.clear()
        cursor_row=self.Student_table.focus()
        contents=self.Student_table.item(cursor_row)
        row=contents['values']
        self.u_id1.insert(0,row[0])
        self.u_n.insert(0,row[1])
        self.u_fn.insert(0,row[2])
        self.u_mn.insert(0,row[3])
        self.u_a.insert(0,row[4])
        self.u_p.insert(0,row[5])
        self.u_f.insert(0,row[6])

    def open_fee(self):
        self.close()
        a=Fees()

    def close(self):
        self.w4.destroy()


#Fee management panel (Add/View user)
class Fees:
    def __init__ (self):
        self.w5=Tk()
        self.w5.title("Fee Management Panel")
        self.w5.geometry('1550x800+-7+0') #width,height,starting x-coordinate,starting y-coordinate
        
        self.bg=ImageTk.PhotoImage(file=r"D:\tkinter-project\butterfly.jpg")
        label_bg=Label(self.w5,image=self.bg)
        label_bg.place(x=0,y=0,relwidth=1,relheight=1)

        title=Label(self.w5,text="Fee Management Panel",font=("times new roman",50,"bold"),bd=9,relief=GROOVE,bg="purple",fg="white")
        title.pack(side=TOP,fill=X)

        frame1=Frame(self.w5,bg="white",bd=4,relief=RIDGE)
        frame1.place(x=20,y=150,width=430,height=600)

        L4=Label(frame1,text="User ID:",fg="black",bg="white",font=("times new roman",15))
        L4.place(x=40,y=30)
        self.u_id=ttk.Entry(frame1,font=("times new roman",15))
        self.u_id.place(x=40,y=60,width=330)

        L5=Label(frame1,text="Payment date:",fg="black",bg="white",font=("times new roman",15))
        L5.place(x=40,y=100)
        self.u_pd=ttk.Entry(frame1,font=("times new roman",15))
        self.u_pd.place(x=40,y=130,width=330)

        L6=Label(frame1,text="Payment month:",fg="black",bg="white",font=("times new roman",15))
        L6.place(x=40,y=170)
        self.u_pm=ttk.Entry(frame1,font=("times new roman",15))
        self.u_pm.place(x=40,y=200,width=330)

        L7=Label(frame1,text="Payment year:",fg="black",bg="white",font=("times new roman",15))
        L7.place(x=40,y=240)
        self.u_py=ttk.Entry(frame1,font=("times new roman",15))
        self.u_py.place(x=40,y=270,width=330)

        L8=Label(frame1,text="Amount:",fg="black",bg="white",font=("times new roman",15))
        L8.place(x=40,y=310)
        self.u_a=ttk.Entry(frame1,font=("times new roman",15))
        self.u_a.place(x=40,y=340,width=330)

        L9=Label(frame1,text="Balance:",fg="black",bg="white",font=("times new roman",15))
        L9.place(x=40,y=380)
        self.u_b=ttk.Entry(frame1,font=("times new roman",15))
        self.u_b.place(x=40,y=410,width=330)

        L10=Label(frame1,text="Remarks:",fg="black",bg="white",font=("times new roman",15))
        L10.place(x=40,y=450)
        self.u_r=ttk.Entry(frame1,font=("times new roman",15))
        self.u_r.place(x=40,y=480,width=330)

        B1=Button(frame1,text="Add",command=lambda:db1.fee_add(self.u_id.get(),self.u_pd.get(),self.u_pm.get(),self.u_py.get(),self.u_a.get(),self.u_b.get(),self.u_r.get(),self),font=("times new roman",15,"bold"),bg="purple",fg="white",relief=RIDGE)
        B1.place(x=90,y=540)

        B2=Button(frame1,text="Clear",command=self.clear,font=("times new roman",15,"bold"),bg="purple",fg="white",relief=RIDGE)
        B2.place(x=150,y=540)

        B3=Button(frame1,text="CRUD User",command=lambda:self.open_student(),font=("times new roman",15,"bold"),bg="white",fg="purple",relief=RIDGE)
        B3.place(x=245,y=540)


        frame2=Frame(self.w5,bg="white",bd=4,relief=RIDGE)
        frame2.place(x=500,y=150,width=1000,height=600)

        lbl_search=Label(frame2,text="Search by",font=("times new roman",20),bg="white")
        lbl_search.grid(row=0,column=0,pady=10,padx=20,sticky="w")

        self.combo=ttk.Combobox(frame2,font=("times new roman",15),state='readonly')
        self.combo['values']=("user_id","payment_date","payment_month","payment_year","amount","balance","remarks")
        self.combo.current(0)
        self.combo.grid(row=0,column=1,padx=20,pady=10,sticky="w")

        self.search=ttk.Entry(frame2,font=("times new roman",15))
        self.search.grid(row=0,column=2,padx=20,pady=10,sticky="w")

        B5=Button(frame2,text="Search",command=lambda:db1.search_fee_data(self.combo.get(),self.search.get(),self),font=("times new roman",15,"bold"),bg="purple",fg="white",relief=RIDGE)
        B5.grid(row=0,column=3,padx=20,pady=10,sticky="w")

        B6=Button(frame2,text="View All",command=lambda:db1.fetch_fee_data(self),font=("times new roman",15,"bold"),bg="purple",fg="white",relief=RIDGE)
        B6.grid(row=0,column=4,padx=20,pady=10,sticky="w")


        frame4=Frame(frame2,bg="purple",bd=4,relief=RIDGE)
        frame4.place(x=50,y=70,width=900,height=500)

        scroll_x=Scrollbar(frame4,orient=HORIZONTAL)
        scroll_y=Scrollbar(frame4,orient=VERTICAL)

        self.Fee_table=ttk.Treeview(frame4,columns=("user_id","payment_date","payment_month","payment_year","amount","balance","remarks"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x.config(command=self.Fee_table.xview)
        scroll_y.config(command=self.Fee_table.yview)

        self.Fee_table.heading("user_id",text="User ID")
        self.Fee_table.heading("payment_date",text="Payment Day")
        self.Fee_table.heading("payment_month",text="Payment Month")
        self.Fee_table.heading("payment_year",text="Payment Year")
        self.Fee_table.heading("amount",text="Amount")
        self.Fee_table.heading("balance",text="Balance")
        self.Fee_table.heading("remarks",text="Remarks")

        self.Fee_table["show"]="headings"
        self.Fee_table.pack(fill=BOTH,expand=1)

        self.Fee_table.column("user_id",width=100)
        self.Fee_table.column("payment_date",width=100)
        self.Fee_table.column("payment_month",width=100)
        self.Fee_table.column("payment_year",width=100)
        self.Fee_table.column("amount",width=150)
        self.Fee_table.column("balance",width=100)
        self.Fee_table.column("remarks",width=100)

        self.Fee_table.bind("<ButtonRelease-1>",self.get_cursor)

        self.w5.mainloop()

    def clear(self):
        self.u_id.delete(0,END)
        self.u_pd.delete(0,END)
        self.u_pm.delete(0,END)
        self.u_py.delete(0,END)
        self.u_a.delete(0,END)
        self.u_b.delete(0,END)
        self.u_r.delete(0,END)
        self.search.delete(0,END)

    def get_cursor(self,event=""):
        self.clear()
        cursor_row=self.Fee_table.focus()
        contents=self.Fee_table.item(cursor_row)
        row=contents['values']
        self.u_id.insert(0,row[0])
        self.u_pd.insert(0,row[1])
        self.u_pm.insert(0,row[2])
        self.u_py.insert(0,row[3])
        self.u_a.insert(0,row[4])
        self.u_b.insert(0,row[5])
        self.u_r.insert(0,row[6])

    def open_student(self):
        self.close()
        a=Student()

    def close(self):
        self.w5.destroy()

#for window appearing after student logs in
class Student_panel:
    def __init__ (self,id):
        self.w6=Tk()
        self.w6.title("Student Panel")
        self.w6.geometry('1550x800+-7+0') #width,height,starting x-coordinate,starting y-coordinate
        
        self.bg=ImageTk.PhotoImage(file=r"D:\tkinter-project\purple.jpg")
        label_bg=Label(self.w6,image=self.bg)
        label_bg.place(x=0,y=0,relwidth=1,relheight=1)

        title=Label(self.w6,text="Student Panel",font=("times new roman",50,"bold"),bd=9,relief=GROOVE,bg="purple",fg="white")
        title.pack(side=TOP,fill=X)

        frame1=Frame(self.w6,bg="white",bd=4,relief=RIDGE)
        frame1.place(x=20,y=150,width=430,height=300)

        L4=Label(frame1,text="Current Password:",fg="black",bg="white",font=("times new roman",15))
        L4.place(x=40,y=30)
        self.p=ttk.Entry(frame1,font=("times new roman",15))
        self.p.place(x=40,y=60,width=330)

        L5=Label(frame1,text="New Password:",fg="black",bg="white",font=("times new roman",15))
        L5.place(x=40,y=100)
        self.p1=ttk.Entry(frame1,font=("times new roman",15))
        self.p1.place(x=40,y=130,width=330)

        L6=Label(frame1,text="Confirm Password:",fg="black",bg="white",font=("times new roman",15))
        L6.place(x=40,y=170)
        self.p2=ttk.Entry(frame1,font=("times new roman",15))
        self.p2.place(x=40,y=200,width=330)

        B1=Button(frame1,text="Change password",command=lambda:db1.password_update(id,self.p.get(),self.p1.get(),self.p2.get()),font=("times new roman",15,"bold"),bg="purple",fg="white",relief=RIDGE)
        B1.place(x=70,y=240)

        B2=Button(frame1,text="Clear",command=self.clear,font=("times new roman",15,"bold"),bg="purple",fg="white",relief=RIDGE)
        B2.place(x=260,y=240)

        frame5=Frame(self.w6,bg="white",bd=4,relief=RIDGE)
        frame5.place(x=20,y=500,width=430,height=250)

        L18=Label(frame5,text="Your details",bg="white",font=("times new roman",15))
        L18.grid(row=0,column=0)

        self.txtBox=Text(frame5,font=("arial",12,"bold"),width=46,height=15,padx=2,pady=6)
        self.txtBox.grid(row=1,column=0)

        frame2=Frame(self.w6,bg="white",bd=4,relief=RIDGE)
        frame2.place(x=500,y=150,width=1000,height=600)

        lbl_search=Label(frame2,text="Search by",font=("times new roman",20),bg="white")
        lbl_search.grid(row=0,column=0,pady=10,padx=20,sticky="w")

        self.combo=ttk.Combobox(frame2,font=("times new roman",15),state='readonly')
        self.combo['values']=("payment_date","payment_month","payment_year","amount","balance","remarks")
        self.combo.current(0)
        self.combo.grid(row=0,column=1,padx=20,pady=10,sticky="w")

        self.search=ttk.Entry(frame2,font=("times new roman",15))
        self.search.grid(row=0,column=2,padx=20,pady=10,sticky="w")

        B5=Button(frame2,text="Search",command=lambda:db1.search_student_fee_data(self.combo.get(),self.search.get(),id,self),font=("times new roman",15,"bold"),bg="purple",fg="white",relief=RIDGE)
        B5.grid(row=0,column=3,padx=20,pady=10,sticky="w")

        B6=Button(frame2,text="View All Payments",command=lambda:db1.fetch_student_fee_data(id,self),font=("times new roman",15,"bold"),bg="purple",fg="white",relief=RIDGE)
        B6.grid(row=0,column=4,padx=20,pady=10,sticky="w")


        frame4=Frame(frame2,bg="purple",bd=4,relief=RIDGE)
        frame4.place(x=50,y=70,width=900,height=500)

        scroll_x=Scrollbar(frame4,orient=HORIZONTAL)
        scroll_y=Scrollbar(frame4,orient=VERTICAL)

        self.Fee_table=ttk.Treeview(frame4,columns=("payment_date","payment_month","payment_year","amount","balance","remarks"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x.config(command=self.Fee_table.xview)
        scroll_y.config(command=self.Fee_table.yview)

        self.Fee_table.heading("payment_date",text="Payment Day")
        self.Fee_table.heading("payment_month",text="Payment Month")
        self.Fee_table.heading("payment_year",text="Payment Year")
        self.Fee_table.heading("amount",text="Amount")
        self.Fee_table.heading("balance",text="Balance")
        self.Fee_table.heading("remarks",text="Remarks")

        self.Fee_table["show"]="headings"
        self.Fee_table.pack(fill=BOTH,expand=1)

        self.Fee_table.column("payment_date",width=100)
        self.Fee_table.column("payment_month",width=100)
        self.Fee_table.column("payment_year",width=100)
        self.Fee_table.column("amount",width=150)
        self.Fee_table.column("balance",width=100)
        self.Fee_table.column("remarks",width=100)

        db1.show_data(self,id)
        db1.fetch_student_fee_data(id,self)

        self.w6.mainloop()

    def clear(self):
        self.p.delete(0,END)
        self.p1.delete(0,END)
        self.p2.delete(0,END)
        self.search.delete(0,END)

    def open_student(self):
        self.close()
        a=Student()

    def close(self):
        self.w6.destroy()

if __name__=="__main__":
    a=Login()

