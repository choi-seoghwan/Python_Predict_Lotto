# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 17:02:01 2020

@author: choi
"""

import sqlite3
import time

# DB연결 현재깢지 나온 수(938)
def untilNowNums():
    # DB 연결
    db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM CURRENT")
    current = cursor.fetchall()
    db_conn.close()  
    
    return current

# 가능한 조합
def totalPossibleNums(until_now_nums):
    
    size = len(until_now_nums)

    cfirst = {until_now_nums[i][1] for i in range(0, size) if until_now_nums[i][0]<550} # 550회 이후로는 같은 번호만 나옴
    csecond = {until_now_nums[i][2] for i in range(0, size)if until_now_nums[i][0]<656} # 656회 이후로는 같은 번호만 나옴
    cthird = {until_now_nums[i][3] for i in range(0, size)if until_now_nums[i][0]<857}  # 857회 이후로는 같은 번호만 나옴
    cfourth = {until_now_nums[i][4] for i in range(0, size)if until_now_nums[i][0]<707} # 707회 이후로는 같은 번호만 나옴
    cfive = {until_now_nums[i][5] for i in range(0, size)if until_now_nums[i][0]<606}   # 606회 이후로는 같은 번호만 나옴
    csix = {until_now_nums[i][6] for i in range(0, size)if until_now_nums[i][0]<201}    # 201회 이후로는 같은 번호만 나옴

    # 앞으로 나올 수 있는 번호 조합
    until_nums = [(i1,i2,i3,i4,i5,i6) \
        for i1 in cfirst for i2 \
            in csecond if i1<i2 for i3 \
                in cthird if i2<i3 for i4 \
                    in cfourth if i3<i4 for i5 \
                        in cfive if i4<i5 for i6 \
                            in csix if i5<i6]

    return until_nums
       
# 합계 제거 ( 94 ~ 176 )
def removeSumNums(possible_nums):
    remove_sum_nums = [i for i in possible_nums if 94 < sum(i) < 176]
    return remove_sum_nums

# 시작
start = time.time()
# DB연결 및 현재(938)까지 나온 번호
until_now_nums = untilNowNums()

# 나올 수 있는 번호 조합
possible_nums = totalPossibleNums(until_now_nums)
print("나올 수 있는 번호 조합 수 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeSumNums(possible_nums)
print("합계 95미만, 176초과 제거 수 :", len(possible_nums),"걸린시간 : ", time.time() - start)

