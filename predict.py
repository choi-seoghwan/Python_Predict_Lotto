# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 17:02:01 2020

@author: choi
"""

import sqlite3
import time
import itertools

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

# 앞뒤4 ( 세로 앞4라인에서 6수, 세로 뒤4라인에서 6수 제거 )
def removeFrontBack4Nums(possible_nums):
    possible_nums = set(possible_nums)
    front4 = {1,8,15,22,29,36,43,2,9,16,23,30,37,44,3,10,17,24,31,38,45,4,11,18,25,32,39}
    back4 = {4,11,18,25,32,39,5,12,19,26,33,40,6,13,20,27,34,41,7,14,21,27,35,42}
    
    front4_list = set(itertools.combinations(front4, 6))    # 세로 앞 4줄에서만 나온 수
    back4_list  = set(itertools.combinations(back4, 6))     # 세로 뒤 4줄에서만 나온 수

    return list((possible_nums - front4_list) - back4_list)

# 색깔 ( 1~10,11~20,...,41~45 : 3 ~ 4 )
def addColorNums(possible_nums):
    color_1 = {1,2,3,4,5,6,7,8,9,10}
    color_2 = {11,12,13,14,15,16,17,18,19,20}
    color_3 = {21,22,23,24,25,26,27,28,29,30}
    color_4 = {31,32,33,34,35,36,37,38,39,40}
    color_5 = {41,42,43,44,45}
    
    add_color_nums = []
    for i in possible_nums:
        color_count = 0
        if len(set(i).intersection(color_1)) > 0 :
            color_count += 1
        if len(set(i).intersection(color_2)) > 0 :
            color_count += 1
        if len(set(i).intersection(color_3)) > 0 :
            color_count += 1
        if len(set(i).intersection(color_4)) > 0 :
            color_count += 1
        if len(set(i).intersection(color_5)) > 0 :
            color_count += 1
        
        if 2 < color_count < 5:
                add_color_nums.append(i)
    
    return add_color_nums

# 가로 3줄 연속에서만 나온 수 제거
def removeRow3Nums(possible_nums):
    c1 = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21}
    c2 = {8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28}
    c3 = {15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35}
    c4 = {22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42}
    c5 = {29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45}

    remove_row_3_nums = [i for i in possible_nums \
    if len(set(i).intersection(c1)) != 6 and len(set(i).intersection(c2)) != 6 and len(set(i).intersection(c3)) != 6 and len(set(i).intersection(c4)) != 6 and len(set(i).intersection(c5)) != 6]
    return remove_row_3_nums

# 세로 3줄 연속에서만 나온 수 제거
def removeCol3Nums(possible_nums):
    c1 = {1,8,15,22,29,36,43,2,9,16,23,30,37,44,3,10,17,24,31,38,45}
    c2 = {2,9,16,23,30,37,44,3,10,17,24,31,38,45,4,11,18,25,32,39}
    c3 = {3,10,17,24,31,38,45,4,11,18,25,32,39,5,12,19,26,33,40}
    c4 = {4,11,18,25,32,39,5,12,19,26,33,40,6,13,20,27,34,41}
    c5 = {5,12,19,26,33,40,13,20,27,34,41,7,14,21,27,35,42}
    
    remove_col_3_nums = [i for i in possible_nums \
    if len(set(i).intersection(c1)) != 6 and len(set(i).intersection(c2)) != 6 and len(set(i).intersection(c3)) != 6 and len(set(i).intersection(c4)) != 6 and len(set(i).intersection(c5)) != 6]
    return remove_col_3_nums

# 세로 좌우 2줄에서만 나온 수 제거
def removeLeftRight2Nums(possible_nums):
    left_right_2_nums = {1,8,15,22,29,36,43,2,9,16,23,30,37,44,6,13,20,27,34,41,7,14,21,27,35,42}
    remove_left_right_2_nums = [i for i in possible_nums if len(set(i).intersection(left_right_2_nums)) != 6]
    return remove_left_right_2_nums

# 3수 연속으로 나온 수 제거
def removeContibuousNums(possible_nums):
    conti_num = {(i,i+1,i+2) for i in range(1,44)}
    not_conti_nums = [i for i in possible_nums if len(set(itertools.combinations(i, 3)).intersection(conti_num)) == 0]
    return not_conti_nums

# 가로연속 6줄
def removeRow16Nums(possible_nums):
    c1 = {1,2,3,4,5,6,7}
    c2 = {8,9,10,11,12,13,14}
    c3 = {15,16,17,18,19,20,21}
    c4 = {22,23,24,25,26,27,28}
    c5 = {29,30,31,32,33,34,35}
    c6 = {36,37,38,39,40,41,42}
    c7 = {43,44,45}

    pre_num = [i for i in possible_nums \
    if not (len(set(i).intersection(c1)) == 1 and \
        len(set(i).intersection(c2)) == 1 and \
            len(set(i).intersection(c3)) == 1 and \
                len(set(i).intersection(c4)) == 1 and \
                    len(set(i).intersection(c5)) == 1 and \
                        len(set(i).intersection(c6)) == 1)]
    pre_num2 = [i for i in pre_num \
    if not(len(set(i).intersection(c2)) == 1 and \
        len(set(i).intersection(c3)) == 1 and \
            len(set(i).intersection(c4)) == 1 and \
                len(set(i).intersection(c5)) == 1 and \
                    len(set(i).intersection(c6)) == 1 and \
                        len(set(i).intersection(c7)) == 1)]
    return pre_num2

# 퐁당퐁당
def removePongNums(possible_nums):
    c1 = {1,8,15,22,29,36,43,2,9,16,23,30,37,44,4,11,18,25,32,39,5,12,19,26,33,40}
    c2 = {2,9,16,23,30,37,44,3,10,17,24,31,38,45,5,12,19,26,33,40,6,13,20,27,34,41}
    c3 = {3,10,17,24,31,38,45,4,11,18,25,32,39,6,13,20,27,34,41,7,14,21,27,35,42}
    
    possible_nums = set(possible_nums)
    
    pong1_list = set(itertools.combinations(c1, 6))
    pong2_list = set(itertools.combinations(c2, 6))
    pong3_list = set(itertools.combinations(c3, 6))
    return list(((possible_nums - pong1_list) - pong2_list)-pong3_list)

# 연속번호가 2가지 이상인 것 제거
def removeContibuous2(possible_nums):
    conti_num = {(i,i+1) for i in range(1,45)}
    notContiNum = [i for i in possible_nums if len(set(itertools.combinations(i, 2)).intersection(conti_num)) < 2]
    return notContiNum

# 끝합 ( 10 ~ 35 )
def removeEndSumNums(possible_nums):
    remove_end_sums = [i for i in possible_nums if 9 < sum([i[0]%10,i[1]%10,i[2]%10,i[3]%10,i[4]%10,i[5]%10]) < 36]
    return remove_end_sums

# 동끝수 (끝수가 동일한 것 1,2개)
def removeEndNums(possible_nums):
    remove_end_nums = [i for i in possible_nums if len(set([i[0]%10,i[1]%10,i[2]%10,i[3]%10,i[4]%10,i[5]%10])) > 3]
    return remove_end_nums

# 이전회차 같은번호 4개 이하
def removeBeforeWinningNums(possible_nums):
    db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
    cursor = db_conn.cursor()
    cursor.execute("SELECT FIRST,SECOND,THIRD,FOURTH,FIVETH,SIXTH FROM CURRENT")
    current = cursor.fetchall()
    db_conn.close()

    for i in possible_nums:
        for j in current:
            if len(set(i).intersection(set(j))) > 4:
                    if i in possible_nums:
                        possible_nums.remove(i)

    return possible_nums

#삼각패턴
def removeTriNums(possible_nums):
    left_top = {1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,18,19,22,23,24,25,29,3,31,36,37,43}
    left_bottom = {1,8,9,15,16,17,22,23,24,25,29,3,31,32,33,36,37,38,39,40,41,43,44,45}
    right_top = {1,2,3,4,5,6,7,9,10,11,12,13,14,17,18,19,20,21,25,26,27,28,33,34,35,41,42}
    right_bottom = {7,13,14,19,20,21,25,26,27,28,31,32,33,34,35,37,38,39,40,41,42,43,44,45} 
    remove_tri_nums = [i for i in possible_nums if len(set(i).intersection(left_top)) != 6 and \
                   len(set(i).intersection(left_bottom)) != 6 and\
                       len(set(i).intersection(right_top)) != 6 and\
                           len(set(i).intersection(right_bottom)) != 6]
    return remove_tri_nums

# 시작
start = time.time()
# DB연결 및 현재(938)까지 나온 번호
until_now_nums = untilNowNums()

# 나올 수 있는 번호 조합
possible_nums = totalPossibleNums(until_now_nums)
print("나올 수 있는 번호        조합 수 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeFirstNum(possible_nums)
print("첫 수가 15초과           제거 수 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeFinalNum(possible_nums)
print("마지막 수가 30미만        제거 수 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeSumNums(possible_nums)
print("합계 95미만, 176초과     제거 수 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeEndNums(possible_nums)
print("끝수가 동일한 것 1~2개    출현 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeOddNums(possible_nums)
print("홀짝 6:0                 제거 수 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = addEdgeNums(possible_nums)
print("모서리 수가 1~4개        포함 수 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeFrontBack4Nums(possible_nums)
print("세로 앞뒤 4줄에서만..    제거 수 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeEndSumNums(possible_nums)
print("끝수 합이 10~35아닌 수    제거 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeRow16Nums(possible_nums)
print("가로 연속 6줄 나온 수      제거 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeContibuousNums(possible_nums)
print("3연속 수                   제거 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeTriNums(possible_nums)
print("삼각패턴                 제거 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = addColorNums(possible_nums)
print("공 색깔 3~4개           출현 수 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeRow3Nums(possible_nums)
print("가로 연속 3줄에서만 나온 수 제거 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeCol3Nums(possible_nums)
print("세로 연속 3줄에서만 나온 수 제거 :", len(possible_nums),"걸린시간 : ", time.time() - start)

possible_nums = removeContibuous2(possible_nums)
print("연속 번호가 2가지 이상     제거 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removePongNums(possible_nums)
print("퐁당퐁당 나온 수           제거 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeLeftRight2Nums(possible_nums)
print("세로 좌우 2줄에서만 나온 수 제거 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeContibuousNums(possible_nums)
print("3연속 수                   제거 :", len(possible_nums),"걸린시간 : ", time.time() - start)
possible_nums = removeBeforeWinningNums(possible_nums)
print("이때까지 나온 수 동일 4개 이하 :", len(possible_nums),"걸린시간 : ", time.time() - start)

print(" -------------------------------------------------------------------------------------- ")
print(" 총 수 :", len(possible_nums),"걸린시간 : ", time.time() - start)