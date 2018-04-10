import collections


class DBSharding(object):
    def __init__(self,dbCount=4,tbCount=8):
        self.dbArray=[]
        self.dbCount=dbCount
        self.tbCount=tbCount
        for x in  xrange(self.dbCount):
            tb=[0]*tbCount
            self.dbArray.append(tb)

    def showDBArray(self):
        for x in xrange(self.dbCount):
            tb=self.dbArray[x]
            zero=tb.count(0)/float(self.tbCount)
            print "->x:",x ,zero
            print tb

    def setRecord(self,dbIndex,tbIndex):
        tb = self.dbArray[dbIndex]
        tb[tbIndex] += 1
        pass

    def hash1(self,userid):
        dbIndex = userid%self.dbCount
        tbIndex = userid%self.tbCount
        return dbIndex,tbIndex

    def hash2(self,userid):
        userid = userid%(self.dbCount*self.tbCount)
        dbIndex = userid/self.tbCount
        #tbIndex = userid - dbIndex*self.tbCount
        tbIndex = userid%self.tbCount
        return dbIndex,tbIndex

    def hash3(self,userid):
        dbIndex = userid%self.dbCount
        tbIndex = userid/self.dbCount%self.tbCount
        return dbIndex,tbIndex


    def fillData(self):
        for i in xrange(100000):
            dbIndex,tbIndex=self.hash2(i)
            #print dbIndex,tbIndex
            self.setRecord(dbIndex,tbIndex)




def main():
    d=DBSharding()
    print d.hash2(200)
    print d.hash3(200)
    d.fillData()
    d.showDBArray()

main()