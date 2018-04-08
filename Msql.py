import pymysql
class Mysql:
#数据库连接
    def open(self):
        # 配置和数据库链接
        self.conn = pymysql.connect(
            # 主机和端口
            host="127.0.0.1", port=3306,
            # 用户与密码
            user="root", password="19970606",

            database="text", charset="utf8"
        )
        self.cursor = self.conn.cursor()
#数据库关闭
    def close(self):
        self.cursor.close()
        self.conn.close()
#插入数据
    def insertSQL(self,shuju):
        self.open()
        self.cursor.execute("INSERT INTO student(name,password) values(%s,%s);",shuju)
        self.conn.commit()
        self.close()
#查询数据
    def checkSQL(self,name):
        self.open()
        self.cursor.execute("select * from student WHERE NAME ="'%s'";",name)
        ret=self.cursor.fetchall()
        self.conn.commit()
        self.close()
        return ret
    #查询题目

    def findQuestion(self):
        self.open()
        self.cursor.execute("select question,answer from exam ")
        ret=self.cursor.fetchall()
        # print(ret)
        self.conn.commit()
        self.close()
        listSql=list(ret)
        skList=[]
        svList=[]
        if listSql=={}:
            return None,None
        else:
            for item in listSql:
                skList.append(item[0])
                svList.append(item[1])

            return skList,svList
#改变数据
    def updateSQL(self,targetDict,queryDict):
        # queryDict：查询条件
        # targetDict：修改后的数据
        self.open()
        self.cursor.execute("update student set name = '%s' where name = '%s';" % (targetDict,queryDict) )
        self.conn.commit()
        self.close()

#删除数据
    def delectSQL(self,sql):
        self.open()
        self.cursor.execute("delete from student  where name = "'%s'";" ,sql)
        self.conn.commit()
        self.close()

if __name__ == '__main__':
    pass
    #
    # a=Mysql()
    # b=a.findQuestion()
    # print(type(b))
    # print(b)