from tkinter import *
from tkinter import messagebox
from MYSQL1.Msql import Mysql
from MYSQL1.Redis import myRedis

class Login:

    def __init__(self):
        self.m=True
        self.ms = Mysql()
        self.mr=myRedis()
        self.index=0
        #初始化答案列表
        self.answer=[]
        #从redis获取答案与题目
        self.klist=[]
        self.vlist=[]
        self.msqlRedis()
        # print(self.vlist, self.klist)
        self.win = Tk()

        self.loginFrame()



#登录界面
    def loginFrame(self):

        self.win.title("登录界面")
        self.win.geometry("400x200")
        self.fram=Frame()
        self.fram.pack()

        self.ent1Var=StringVar()
        self.label1=Label(self.fram,text="用户名")
        self.ent1=Entry(self.fram,textvariable=self.ent1Var)
        self.ent2Var = StringVar()
        self.label2=Label(self.fram,text="密码")
        self.ent2=Entry(self.fram,textvariable=self.ent2Var)

        self.but1=Button(self.fram,width=10,text="登录",command=self.login)
        self.but2=Button(self.fram,width=10,text="注册",command=self.register)

        self.label1.grid(row=1,column=1,pady=30)
        self.ent1.grid(row=1,column=2,pady=30)

        self.label2.grid(row=2,column=1,pady=5)
        self.ent2.grid(row=2,column=2,pady=5)

        self.but1.grid(row=4,column=1,pady=20)
        self.but2.grid(row=4,column=2,pady=20)
        self.win.mainloop()

#考试界面
    def textFrame(self):
        self.win.title("考试界面")
        self.win.geometry("400x400")
        self.examFrame=Frame()
        self.examFrame.pack()
        self.label3=Label(self.examFrame)


        self.ent3Var=StringVar()
        self.ent3=Entry(self.examFrame,textvariable=self.ent3Var)
        self.but5=Button(self.examFrame,text="上一题",command=self.last1,width=20)
        self.but6=Button(self.examFrame,text="下一题",command=self.next,width=20)

        self.label3.grid(row=1,column=1,pady=(30,10))
        self.ent3.grid(row=2,columnspan=3,pady=10)
        self.but5.grid(row=3,columnspan=3,pady=5,padx=5)
        self.but6.grid(row=4,columnspan=3,pady=5,padx=5)
        self.label3["text"] = self.klist[self.index]
        # self.label3["text"] = self.sklist[self.index]



#注册界面
    def RegisterFrame(self):
        self.win.title("注册界面")
        self.win.geometry("400x200")
        self.registerFrame = Frame()
        self.registerFrame.pack()

        self.ent5Var=StringVar()
        self.label5=Label(self.registerFrame,text="用户名")

        self.ent5=Entry(self.registerFrame,textvariable=self.ent5Var)

        self.ent6Var = StringVar()
        self.label6=Label(self.registerFrame,text="密码")

        self.ent6=Entry(self.registerFrame,textvariable=self.ent6Var)
        self.ent7Var = StringVar()
        self.label7 = Label(self.registerFrame, text="确认密码")
        self.ent7 = Entry(self.registerFrame, textvariable=self.ent7Var)

        self.but3=Button(self.registerFrame,width=10,text="确定",command=self.exam)
        self.but4=Button(self.registerFrame,width=10,text="返回",command=self.back)


        self.label5.grid(row=1,column=1,pady=(30,0))
        self.ent5.grid(row=1,column=2,pady=(30,0))
        self.label6.grid(row=2,column=1,pady=5)
        self.ent6.grid(row=2,column=2,pady=5)
        self.label7.grid(row=3,column=1,pady=5)
        self.ent7.grid(row=3,column=2,pady=5)
        self.but3.grid(row=4,column=1,pady=(10,30))
        self.but4.grid(row=4,column=2,pady=(10,30))

#登录按钮
    def login(self):
        name=self.ent1Var.get()
        password=self.ent2Var.get()
        #判断redis里有没有用户名
        ret1=self.mr.findName(name)
        if name==''or password=='':
            messagebox.showinfo("警告", "账号或密码不能为空")
        else:
            if ret1==None:
                #redis里没有，就在mysql里找
                ret = self.ms.checkSQL(name)
                #mysql里没有
                if ret==():
                    messagebox.showinfo("警告","账号不存在")
                else:
                    #判断密码是否相等
                    if password==ret[0][2]:
                        self.mr.addName(name,password)
                        self.fram.destroy()
                        self.textFrame()
                    else:
                        messagebox.showinfo("警告","密码错误")
            else:
                #redis里有，判断密码是否正确
                if ret1==password:
                    self.fram.destroy()
                    self.textFrame()
                else:
                    messagebox.showinfo("警告","密码错误")

    # 注册按钮
    def register(self):
        self.fram.destroy()
        self.RegisterFrame()
    #返回登录页面
    def back(self):
        self.registerFrame.destroy()
        self.loginFrame()

#注册页面确定按钮
    def exam(self):

        name = self.ent5Var.get()
        password = self.ent6Var.get()
        password2=self.ent7Var.get()
        ret1=self.mr.findName(name)
        if name==''or password=='':
            messagebox.showinfo("警告", "账号或密码不能为空")
        else:
            #判断redis里有没有账户名
            if ret1 == None:
                #查找mysql里有没有
                ret = self.ms.checkSQL(name)
                #mysql里没有
                if ret==():
                    #判断两次密码是否相同
                    if password==password2:
                        #将用户名与密码插入mysql
                        self.ms.insertSQL((name, password))
                        # 将用户名与密码插入redis
                        self.mr.addName(name,password)
                        self.registerFrame.destroy()
                        self.textFrame()
                    else:
                        messagebox.showinfo("警告","两次密码不一致")
                else:
                    messagebox.showinfo("警告","用户名已存在")
            else:
                messagebox.showinfo("警告", "用户名已存在")

    # 上一题
    def last1(self):
        self.m=False
        if self.index>0:
            self.index-=1
            self.label3["text"]=self.klist[self.index]
            self.ent3Var.set(self.answer[self.index])
            # print(self.answer)
        else:
            messagebox.showinfo("警告","没有上一个了")



#下一题


    #下一题
    def next(self):
        if self.index < len(self.klist) - 1:
            self.index += 1
            self.label3["text"] = self.klist[self.index]



            answer1 = self.ent3.get()
            self.answer.append(answer1)
            self.ent3Var.set("")
            print(self.answer)


            # if self.m==False:
            #     self.answer.pop(self.index-1)
            #     self.m=True

            # print(self.answer)
            # print(self.vlist)

        elif self.index ==len(self.klist) - 1:
            Button(self.examFrame,text="交卷",command=self.result,width=50).grid(row=5,columnspan=3,pady=5,padx=5)

#得到成绩

    #得到成绩
    def result(self):
        self.text = Label(self.examFrame, text="你的成绩是")
        self.text.grid(row=6, column=1, pady=5, padx=5)
        self.grade = Label(self.examFrame,fg="red",font="Arial, 15")
        self.grade.grid(row=6, column=2, pady=5)
        count=0
        Rset=self.mr.findAllExam()
        Sset=self.ms.findQuestion()
        if Rset==(None,None):
            if Sset==None:
                messagebox.showinfo("警告", "题目不存在")
            else:
                self.vlist=self.svlist
                #组合遍历，判断答案是否相等
                for (i,j )in zip(self.answer,self.vlist):
                    if i==j:
                        count=count+1
                ret=count*25
                self.grade["text"]=ret

        else:
            for (i, j) in zip(self.answer, self.vlist):
                if i == j:
                    count = count + 1
            ret = count * 25
            self.grade["text"] = ret


#判断查询
    def msqlRedis(self):
        #接收redis查找题目函数的返回值
        m,n=self.mr.findAllExam()
        # Sset=self.ms.findQuestion()
        #如果redis不存在题目
        if m==None:
            #把mysql里的题目与答案给两个列表
             self.klist,self.vlist= self.ms.findQuestion()
            #这里是遍历两个列表，把题目与答案插入redis
             for i,j in zip(self.klist,self.vlist):
                 self.mr.addexamName(i,j)

        else:
            #redis里存在题目，就直接把前面接收的m，n给这两个列表
             self.klist, self.vlist=m,n













Login()

