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

# 짝홀 제거 ( 1:5, 2:4, 3:3, 4:2, 5:1 )
def removeOddNums(possible_nums):
    remove_odd_nums = [i for i in possible_nums if 0 < i[0]%2+i[1]%2+i[2]%2+i[3]%2+i[4]%2+i[5]%2 < 6]
    return remove_odd_nums

# 첫수 ( 16 미만 )
def removeFirstNum(possible_nums):
    remove_first_nums = [i for i in possible_nums if i[0] < 16]
    return remove_first_nums

# 마지막수 ( 30 초과 )
def removeFinalNum(possible_nums):
    remove_final_nums = [i for i in possible_nums if i[5] > 30]
    return remove_final_nums

# 모서리수 (모서리에서 1~4개 나옴)
def addEdgeNums(possible_nums):
    edge_num = {1,2,8,9, 5,6,13,14, 39,30,36,37, 34,35,41,42, 43,44,45}
    add_edge_nums = [i for i in possible_nums if 0 < len(set(i).intersection(edge_num)) < 5]
    return add_edge_nums

# 시작
start = time.time()
# DB연결 및 현재(938)까지 나온 번호
until_now_nums = untilNowNums()

# 나올 수 있는 번호 조합
possible_nums = totalPossibleNums(until_now_nums)
print("나올 수 있는 번호 조합 수 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeSumNums(possible_nums)
print("합계 95미만, 176초과 제거 수 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeOddNums(possible_nums)
print("홀짝 6:0 제거 수 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeFirstNum(possible_nums)
print("첫 수가 15초과 제거 수:", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeFinalNum(possible_nums)
print("마지막 수가 30미만 제거 수 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = addEdgeNums(possible_nums)
print("모서리 수가 1~4개 포함된 수 :", len(possible_nums),"걸린시간 : ", time.time() - start)