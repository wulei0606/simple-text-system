import redis


class myRedis:
    def __init__(self):
        self.client=redis.StrictRedis(
            host='localhost',port=6379,db=1,password=19970606
        )
    def findName(self,name):
        hget=self.client.hget("yonghu",name)
        if hget:
            return hget.decode("utf-8")
        else:
            return None

    def addName(self,name,pwd):
        pipe=self.client.pipeline(transaction=True)
        pipe.hset("yonghu",name,pwd)
        pipe.execute()
        # print("提交成功")

    def addexamName(self,name,pwd):
        pipe=self.client.pipeline(transaction=True)
        pipe.hset("exam",name,pwd)
        pipe.execute()
        # print("提交成功")

    def findAllExam(self):
        exam=self.client.hgetall("exam")
        # print(exam)
        klist=[]
        vlist=[]
        # print(exam)
        if exam=={}:
            return None,None
        else:
            for k,v in exam.items():
                klist.append(k.decode("utf-8"))
                vlist.append(v.decode("utf-8"))
            return klist,vlist
            # print(klist)

if __name__ == '__main__':
    a=myRedis()
    # print(a.findName("123"))
    # a.addName("占昌达","1001")

    # klist,vlist=a.findAllExam()
    # print(klist)
    # print(vlist)

