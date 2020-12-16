# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 20:16:09 2020

@author: choi
"""
import sqlite3
import collections

def regression(predict_round):
    db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
    cursor1 = db_conn.cursor()
    cursor2 = db_conn.cursor()
    
    regression_round = 920
    round_num = 1
    
    regression_count = []
    
    while(True):

        if(regression_round - round_num == 0):
            break
        
        cursor1.execute("SELECT FIRST,SECOND,THIRD,FOURTH,FIVETH,SIXTH FROM CURRENT WHERE ROUND == {0}".format(regression_round))
        cursor2.execute("SELECT FIRST,SECOND,THIRD,FOURTH,FIVETH,SIXTH FROM CURRENT WHERE ROUND == {0}".format(regression_round-round_num))
        current = set(cursor1.fetchone())
        current1 = set(cursor2.fetchone())
        regression_count.append(len(set(current).intersection(current1)))        
        round_num = round_num + 1
               
    print(regression_count)
    db_conn.close()

regression(942)