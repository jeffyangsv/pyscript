#coding=utf-8

import time
import os
import pymssql
import re
import difflib



class SelectMySQL(object):
    def select_data(self,host,user,password,database,searchsql):
        result = []
        try:
            conn = pymssql.connect(host=host,
                                 user=user,
                                 password=password,
                                 database=database)
            cur = conn.cursor()
            cur.execute(searchsql)
            alldata = cur.fetchall()
            # print(alldata)
            for rec in alldata:
                result.append(rec) 
        except Exception as e:
            print('Error msg: ' + e)
        finally:
            cur.close()
            conn.close()
  
        return result

    def get_result(self, host, user, password, database, searchsql, filename):
        #print(searchsql)
        results = self.select_data(host, user, password, database, searchsql)
        print('The amount of datas: %d' % (len(results)))
        with open(filename, 'w') as f:
            for result in results:
                f.write(str(result) + '\n')
        print('%s Data write is over!' %host)
        return results

def select_card():
    searchsql = '''select stb.smart_card_id,stb.subscriber_id,COUNT(distinct package_id) package_num \
                 from lsms_entitlement e \
                 left join lsms_subscriber s on e.subscriber_id = s.subscriber_id \
                 left join lsms_stb stb on e.subscriber_id=stb.subscriber_id \
                 group by stb.smart_card_id,stb.subscriber_id \
                 order by stb.smart_card_id'''
                 
    
    select = SelectMySQL()
    for edge_id in sorted(edict.keys()):
        #password='cdn_'+edict[ip]+'_LSM'
        print('%s begin search!!!' %edict[edge_id])
        filename = workdir+'\\'+edict[edge_id]+'.txt'
        #result1 = select.get_result('172.16.'+edict[ip]+'.181','lsms',password,'lsms',searchsql,filename)
        result1 = select.get_result('172.16.'+edict[edge_id]+'.184','lsms','lsms','lsms',searchsql,filename)
    #print(result1)
        print('CBO_%s begin search!!!' %edge_id)
        cbo_select_card= "select stb.smart_card_id,stb.subscriber_id,COUNT(distinct package_id) package_num \
                          from lsms_entitlement e \
                          left join lsms_subscriber s on e.subscriber_id = s.subscriber_id \
                          left join lsms_stb stb on e.subscriber_id=stb.subscriber_id \
                          where s.edge_id ='"+ edge_id +"' \
                          group by stb.smart_card_id,stb.subscriber_id \
                          order by stb.smart_card_id"
        filename2 = 'D:\\'+search_time+'\\CBO_'+edict[edge_id]+'.txt'
        result2 = select.get_result('172.16.89.181','lsms','lsms','lsms',cbo_select_card,filename2)

def compare_data():
    filelist = os.listdir(workdir)
    diffdir = workdir+'\\diff'
    os.makedirs(diffdir)
    dict={}
    for edge_id in sorted(edict.keys()):
        re1 = re.compile(edict[edge_id])
        dict[edge_id]=list()
        for file in filelist:
            if re1.search(file):
                dict[edge_id].append(file)

    for i in dict.keys():
        if dict[i] != []:
            a = open(workdir+'\\'+dict[i][0],'U').readlines()
            b = open(workdir+'\\'+dict[i][1],'U').readlines()
            #
            diffs = difflib.ndiff(a,b)
            with open(diffdir+'\\'+edict[i]+'.txt','w') as fp:
                for diff in diffs:
                    fp.write(diff)
                    
            '''
            ##########   1    ############
            diffs = difflib.ndiff(a,b)
            with open(diffdir+'\\'+edict[i]+'.txt','w') as fp:
                for diff in diffs:
                    fp.write(diff)
            ##########   2    ############
            
                                            
            '''        
                
if __name__ == '__main__':
    search_time = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
    workdir = 'D:\\'+search_time
    os.makedirs(workdir)    
    #edict={'10':'72','20':'73','30':'74','40':'75','50':'76','60':'77','70':'78','80':'84'}
    edict={'70':'77',}
    select_card()
    compare_data()


        