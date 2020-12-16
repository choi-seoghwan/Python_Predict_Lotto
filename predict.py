# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 17:02:01 2020

@author: choi
"""

import sqlite3
import time
import itertools
import collections
from multiprocessing import Pool

# DB연결 현재깢지 나온 수(~939)
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
    until_nums = [(i1,i2,i3,i4,i5,i6) for i1 in cfirst for i2 in csecond if i1<i2 \
                      for i3 in cthird if i2<i3 for i4 in cfourth if i3<i4 \
                              for i5 in cfive if i4<i5 for i6 in csix if i5<i6]
    return until_nums
       
# 1. 첫 수 ( 15 이하 )
def removeFirstNum(possible_nums):
    remove_first_nums = [i for i in possible_nums if i[0] < 16]
    return remove_first_nums

# 2. 마지막 수 ( 35 이상 )
def removeFinalNum(possible_nums):
    remove_final_nums = [i for i in possible_nums if i[5] > 34]
    return remove_final_nums

# 3. 합계 ( 95 ~ 175 )
def removeSumNums(possible_nums):
    remove_sum_nums = [i for i in possible_nums if 94 < sum(i) < 176]
    return remove_sum_nums

# 4. 끝수 ( 동일한 끝수 3개까지 )
def removeEndNums(possible_nums):
    # 1 -> 6, 2 -> 5, 3 -> 4 
    remove_end_nums = [i for i in possible_nums if len(set([i[0]%10,i[1]%10,i[2]%10,i[3]%10,i[4]%10,i[5]%10])) > 3]
    return remove_end_nums

# 5. 홀짝 ( 1:5, 2:4, 3:3, 4:2, 5:1 )
def removeOddNums(possible_nums):
    remove_odd_nums = [i for i in possible_nums if 0 < i[0]%2+i[1]%2+i[2]%2+i[3]%2+i[4]%2+i[5]%2 < 6]
    return remove_odd_nums

# 6. 모서리수 ( 모서리에서 1~4개 )
def addEdgeNums(possible_nums):
    edge_num = {1,2,8,9, 5,6,13,14, 39,30,36,37, 34,35,41,42, 43,44,45}
    add_edge_nums = [i for i in possible_nums if 0 < len(set(i).intersection(edge_num)) < 5]
    return add_edge_nums

# 7. 앞뒤3 ( 세로 앞3라인에서 6수, 세로 뒤3라인에서 6수 제거 )
def removeFrontBack3Nums(possible_nums):
    front3 = {1,8,15,22,29,36,43,2,9,16,23,30,37,44,3,10,17,24,31,38,45}
    back3 = {5,12,19,26,33,40,6,13,20,27,34,41,7,14,21,27,35,42}
    possible_nums = [i for i in possible_nums if len(set(i).intersection(front3)) < 6] # 세로 앞 4줄에서만 나온 수
    possible_nums = [i for i in possible_nums if len(set(i).intersection(back3)) < 6] # 세로 뒤 4줄에서만 나온 수
    return possible_nums

# 8. 끝합 ( 10 ~ 35 )
def removeEndSumNums(possible_nums):
    remove_end_sums = [i for i in possible_nums if 9 < sum([i[0]%10,i[1]%10,i[2]%10,i[3]%10,i[4]%10,i[5]%10]) < 36]
    return remove_end_sums

# 9. 가로연속 6줄
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

# 10. 3수 연속
def removeContibuousNums(possible_nums):
    conti_num = {(i,i+1,i+2) for i in range(1,44)}
    not_conti_nums = [i for i in possible_nums if len(set(itertools.combinations(i, 3)).intersection(conti_num)) == 0]
    return not_conti_nums

# 11. 삼각패턴
def removeTriNums(possible_nums):
    left_bottom = {1,8,9,15,16,17,22,23,24,25,29,3,31,32,33,36,37,38,39,40,41,43,44,45}
    right_top = {1,2,3,4,5,6,7,9,10,11,12,13,14,17,18,19,20,21,25,26,27,28,33,34,35,41,42}
    right_bottom = {7,13,14,19,20,21,25,26,27,28,31,32,33,34,35,37,38,39,40,41,42,43,44,45} 

    remove_tri_nums = [i for i in possible_nums if len(set(i).intersection(left_bottom)) != 6 and
                       len(set(i).intersection(right_bottom)) != 6 and len(set(i).intersection(right_top)) != 6]
    return remove_tri_nums

# 12. 가로 3줄 연속
def removeRow3Nums(possible_nums):
    c1 = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21}
    c2 = {8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28}
    c3 = {15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35}
    c4 = {22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42}
    c5 = {29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45}

    remove_row_3_nums = [i for i in possible_nums \
    if len(set(i).intersection(c1)) != 6 and len(set(i).intersection(c2)) != 6 and len(set(i).intersection(c3)) != 6 and len(set(i).intersection(c4)) != 6 and len(set(i).intersection(c5)) != 6]
    return remove_row_3_nums

# 13. 세로 3줄 연속
def removeCol3Nums(possible_nums):
    c1 = {1,8,15,22,29,36,43,2,9,16,23,30,37,44,3,10,17,24,31,38,45}
    c2 = {2,9,16,23,30,37,44,3,10,17,24,31,38,45,4,11,18,25,32,39}
    c3 = {3,10,17,24,31,38,45,4,11,18,25,32,39,5,12,19,26,33,40}
    c4 = {4,11,18,25,32,39,5,12,19,26,33,40,6,13,20,27,34,41}
    c5 = {5,12,19,26,33,40,13,20,27,34,41,7,14,21,27,35,42}
    
    remove_col_3_nums = [i for i in possible_nums \
    if len(set(i).intersection(c1)) != 6 and len(set(i).intersection(c2)) != 6 and len(set(i).intersection(c3)) != 6 and len(set(i).intersection(c4)) != 6 and len(set(i).intersection(c5)) != 6]
    return remove_col_3_nums

# 14. 색깔 ( 1~10,11~20,...,41~45 : 3 ~ 4 )
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
        
        if 2 < color_count < 6:
                add_color_nums.append(i)
    
    return add_color_nums

# 15. 연속번호가 2
def removeContibuous2(possible_nums):
    conti_num = {(i,i+1) for i in range(1,45)}
    notContiNum = [i for i in possible_nums if len(set(itertools.combinations(i, 2)).intersection(conti_num)) < 2]
    return notContiNum

# 16. 퐁당퐁당
def removePongNums(possible_nums):
    c1 = {1,8,15,22,29,36,43,2,9,16,23,30,37,44,4,11,18,25,32,39,5,12,19,26,33,40}
    c2 = {2,9,16,23,30,37,44,3,10,17,24,31,38,45,5,12,19,26,33,40,6,13,20,27,34,41}
    c3 = {3,10,17,24,31,38,45,4,11,18,25,32,39,6,13,20,27,34,41,7,14,21,27,35,42}

    pong1_list = [i for i in possible_nums if len(set(i).intersection(c1)) < 6]
    pong2_list = [i for i in pong1_list if len(set(i).intersection(c2)) < 6]
    pong3_list = [i for i in pong2_list if len(set(i).intersection(c3)) < 6]
    return pong3_list

# 17. 세로 좌우 2줄
def removeLeftRight2Nums(possible_nums):
    left_right_2_nums = {1,8,15,22,29,36,43,2,9,16,23,30,37,44,6,13,20,27,34,41,7,14,21,27,35,42}
    remove_left_right_2_nums = [i for i in possible_nums if len(set(i).intersection(left_right_2_nums)) != 6]
    return remove_left_right_2_nums

# 18. GRA
def countGRA(possible_nums, predict_round, count):
    gra = setGRA(predict_round,count)
    gra_count = recentty(predict_round, count)

    green_add_nums = [i for i in possible_nums if len(set(i).intersection(set(gra[0]))) in gra_count[0]]
    remove_red_nums = [i for i in green_add_nums if len(set(i).intersection(set(gra[1]))) in gra_count[1]]
    remove_average_nums = [i for i in remove_red_nums if len(set(i).intersection(set(gra[2]))) in gra_count[2]]
    
    return remove_average_nums
def setGRA(predict_round, count):
    # DB 연결
    db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
    cursor = db_conn.cursor()
    cursor.execute("SELECT FIRST,SECOND,THIRD,FOURTH,FIVETH,SIXTH FROM CURRENT WHERE ROUND >= {0} AND ROUND < {1}".format(predict_round-count, predict_round))
    current = cursor.fetchall()
    db_conn.close()  
    
    current_count = []
    green = []
    red = []
    average = []
    
    for i in current:
        for j in range(0,len(i)):
            current_count.append(i[j])
    
    current_count_count = []
    for qqq in range(1,46):
        current_count_count.append(current_count.count(qqq))
    avg = int(sum(current_count_count)/len(current_count_count))
    for rotto in range(1,46):
        if current_count.count(rotto) < avg:
            green.append(rotto)
        elif current_count.count(rotto) > avg:
            red.append(rotto)
        else:
            average.append(rotto)
    
    return [green, red, average]
def recentty(predict_round, count):
    
        # DB 연결
    db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
    cursor = db_conn.cursor()
    cursor.execute("SELECT ROUND,FIRST,SECOND,THIRD,FOURTH,FIVETH,SIXTH FROM CURRENT WHERE ROUND >= {0} AND ROUND < {1}".format(predict_round-20, predict_round))
    last_tens = cursor.fetchall()
    db_conn.close()  
    
    green_count = []
    red_count = []
    avg_count = []
    
    for last_ten in last_tens:
        gra = setGRA(last_ten[0], count)
        green_count.append(len(set(last_ten).intersection(set(gra[0]))))
        red_count.append(len(set(last_ten).intersection(set(gra[1]))))
        avg_count.append(len(set(last_ten).intersection(set(gra[2]))))
        

    return [green_count, red_count, avg_count]

# 19. 최근
def recent10Notnum(possible_nums,predict_round):
    db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
    cursor = db_conn.cursor()
    cursor.execute("SELECT ROUND,FIRST,SECOND,THIRD,FOURTH,FIVETH,SIXTH FROM CURRENT WHERE ROUND >= {0} AND ROUND < {1}".format(predict_round-10, predict_round))
    current = cursor.fetchall()
    db_conn.close()

    recent_nums = []
    for i in current:
        for j in range(0,len(i)):
            recent_nums.append(i[j])
    
    all_nums = []
    for ii in range(1,46):
        all_nums.append(ii)
    
    recent_nums = set(recent_nums)
    all_nums = set(all_nums)
    
    recent_not_nums = all_nums - recent_nums
    possible_nums = [i for i in possible_nums if len(set(i).intersection(recent_not_nums)) < 4]
    
    return possible_nums
def recent5Notnum(possible_nums,predict_round):
    db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
    cursor = db_conn.cursor()
    cursor.execute("SELECT ROUND,FIRST,SECOND,THIRD,FOURTH,FIVETH,SIXTH FROM CURRENT WHERE ROUND >= {0} AND ROUND < {1}".format(predict_round-5, predict_round))
    current = cursor.fetchall()
    db_conn.close()

    recent_nums = []
    for i in current:
        for j in range(0,len(i)):
            recent_nums.append(i[j])
    
    all_nums = []
    for ii in range(1,46):
        all_nums.append(ii)
    
    recent_nums = set(recent_nums)
    all_nums = set(all_nums)
    
    recent_not_nums = all_nums - recent_nums
    possible_nums = [i for i in possible_nums if 1 < len(set(i).intersection(recent_not_nums)) < 6]
    
    return possible_nums
def recent3Notnum(possible_nums,predict_round):
    db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
    cursor = db_conn.cursor()
    cursor.execute("SELECT ROUND,FIRST,SECOND,THIRD,FOURTH,FIVETH,SIXTH FROM CURRENT WHERE ROUND >= {0} AND ROUND < {1}".format(predict_round-4, predict_round))
    current = cursor.fetchall()
    db_conn.close()

    recent_nums = []
    for i in current:
        for j in range(0,len(i)):
            recent_nums.append(i[j])
    
    all_nums = []
    for ii in range(1,46):
        all_nums.append(ii)
    
    recent_nums = set(recent_nums)
    all_nums = set(all_nums)
    
    recent_not_nums = all_nums - recent_nums
    possible_nums = [i for i in possible_nums if 2 < len(set(i).intersection(recent_not_nums))]
    
    return possible_nums

# 20. ROUND
def removeRoundNum(possible_nums, predict_round):
      
    db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
    cursor = db_conn.cursor()
    cursor.execute("SELECT FIRST,SECOND,THIRD,FOURTH,FIVETH,SIXTH,BONUS FROM CURRENT WHERE ROUND = {0}".format(predict_round-1))
    current = cursor.fetchall()
    db_conn.close()
    #4구 +1
    print("제외 수 : ",current[0][3]+1)
    possible_nums = [i for i in possible_nums if current[0][3]+1 not in i]
    
    # #지난회차 같은번호 2개 이하
    remove_before_winning_num = set(current[0])
    possible_nums = [i for i in possible_nums if len(set(i).intersection(remove_before_winning_num)) < 3]
    
    return possible_nums

# 21. COUNT
def finalNum(possible_nums):
    all_list = []
    for i in possible_nums:
        for j in range(0,len(i)):
            all_list.append(i[j])
    count_list = collections.Counter(all_list)
    
    count_list1 = collections.Counter(all_list).most_common(21)
    counter = []
    
    for i in count_list1:
        counter.append(i[0])
        
    counter = set(counter)
    possible_nums = [i for i in possible_nums if len(set(i).intersection(counter)) > 3]
    
    counter2 = []
    counter3 = []
    count_list2 = collections.Counter(all_list).most_common(44)
    for i in count_list2:
        counter2.append(i[0])
    count_list3 = collections.Counter(all_list).most_common(42)
    for i in count_list3:
        counter3.append(i[0])
    counter4 = set(set(counter2)-set(counter3))
    print("제외 수 : ",counter4)
    possible_nums = [i for i in possible_nums if len(set(i).intersection(counter4)) == 0]
    return possible_nums
def finalNum2(possible_nums):
    
    all_list = []
    for i in possible_nums:
        for j in range(0,len(i)):
            all_list.append(i[j])
    count_list1 = collections.Counter(all_list).most_common(22)
    counter = []
    
    for i in count_list1:
        counter.append(i[0])
        
    counter = set(counter)
    possible_nums = [i for i in possible_nums if len(set(i).intersection(counter)) > 3]
        
    counter2 = []
    counter3 = []
    count_list2 = collections.Counter(all_list).most_common(42)
    for i in count_list2:
        counter2.append(i[0])
    count_list3 = collections.Counter(all_list).most_common(39)
    for i in count_list3:
        counter3.append(i[0])
    counter4 = set(set(counter2)-set(counter3))
    print("제외 수 : ",counter4)
    possible_nums = [i for i in possible_nums if len(set(i).intersection(counter4)) == 0]
    return possible_nums
def finalNum3(possible_nums):
    
    all_list = []
    for i in possible_nums:
        for j in range(0,len(i)):
            all_list.append(i[j])
    count_list1 = collections.Counter(all_list).most_common(21)
    counter = []
    
    for i in count_list1:
        counter.append(i[0])
        
    counter = set(counter)
    possible_nums = [i for i in possible_nums if len(set(i).intersection(counter)) > 3]

    return possible_nums

# 22. 4WEEK
def fourWeek2(possible_nums,predict_round):
    db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
    cursor = db_conn.cursor()
    cursor.execute("SELECT FIRST,SECOND,THIRD,FOURTH,FIVETH,SIXTH FROM CURRENT WHERE ROUND >= {0} AND ROUND < {1}".format(predict_round-4, predict_round))
    current = cursor.fetchall()
    db_conn.close()

    recent_nums = []
    for i in current:
        for j in range(0,len(i)):
            recent_nums.append(i[j])
            
    container = collections.Counter(recent_nums)

    remove_nums = []
    for k,v in container.items():
        if(v >= 2):
            remove_nums.append(k)
    
    remove_nums = set(remove_nums)
    possible_nums = [i for i in possible_nums if len(set(i).intersection(remove_nums)) < 2]
    
    return possible_nums

# 23. 지난회차
def lastNull(possible_nums,predict_round):
    
    db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
    cursor = db_conn.cursor()
    cursor.execute("SELECT FIRST,SECOND,THIRD,FOURTH,FIVETH,SIXTH FROM CURRENT WHERE ROUND >= {0} AND ROUND < {1}".format(predict_round-1, predict_round))
    before = cursor.fetchall()
    db_conn.close()
    
    last1 = {1,2,3,4,5,6,7,8,9,10,11,12}
    last2 = {13,14,15,16,17,18,19,20,21,22,23,24}
    last3 = {25,26,27,28,29,30,31,32,33,34,35,36}
    last4 = {37,38,39,40,41,42,43,44,45}

    # print(predict_round, before[0])
    round_num = 0
    if len(set(before[0]).intersection(last1)) == 0:
        possible_nums = [i for i in possible_nums if len(set(i).intersection(last1)) > round_num]
    if len(set(before[0]).intersection(last2)) == 0:
        possible_nums = [i for i in possible_nums if len(set(i).intersection(last2)) > round_num]    
    if len(set(before[0]).intersection(last3)) == 0:
        possible_nums = [i for i in possible_nums if len(set(i).intersection(last3)) > round_num]
    if len(set(before[0]).intersection(last4)) == 0:
        possible_nums = [i for i in possible_nums if len(set(i).intersection(last4)) > round_num]
        
    return possible_nums
def lastNull2(possible_nums,predict_round):
    
    db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
    cursor = db_conn.cursor()
    cursor.execute("SELECT FIRST,SECOND,THIRD,FOURTH,FIVETH,SIXTH FROM CURRENT WHERE ROUND >= {0} AND ROUND < {1}".format(predict_round-2, predict_round))
    before = cursor.fetchall()
    db_conn.close()
    recent_nums = []
    for i in before:
        for j in range(0,len(i)):
            recent_nums.append(i[j])
    
    last1 = {1,2,3,4,5,6,7,8}
    last2 = {9,10,11,12,13,14,15,16}
    last3 = {17,18,19,20,21,22,23,24}
    last4 = {25,26,27,28,29,30,31,32}
    last5 = {33,34,35,36,37,38,39,40}

    round_num = 0
    if len(set(recent_nums).intersection(last1)) == 0:
        possible_nums = [i for i in possible_nums if len(set(i).intersection(last1)) > round_num]
    if len(set(recent_nums).intersection(last2)) == 0:
        possible_nums = [i for i in possible_nums if len(set(i).intersection(last2)) > round_num]    
    if len(set(recent_nums).intersection(last3)) == 0:
        possible_nums = [i for i in possible_nums if len(set(i).intersection(last3)) > round_num]
    if len(set(recent_nums).intersection(last4)) == 0:
        possible_nums = [i for i in possible_nums if len(set(i).intersection(last4)) > round_num]
    if len(set(recent_nums).intersection(last5)) == 0:
        possible_nums = [i for i in possible_nums if len(set(i).intersection(last5)) > round_num]
        
    return possible_nums

# 24. 평균
def averageNums(possible_nums):
    
    possible_nums = [i for i in possible_nums if 17 < sum(i)/len(i) < 33 ]
        
    return possible_nums

# 25. 이전회차 같은번호 4개 이하
def removeBeforeWinningNums(possible_nums, predict_round):
    db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
    cursor = db_conn.cursor()
    cursor.execute("SELECT FIRST,SECOND,THIRD,FOURTH,FIVETH,SIXTH FROM CURRENT WHERE ROUND < {0}".format(predict_round))
    current = cursor.fetchall()
    db_conn.close()
    
    for i in possible_nums:
        for j in current:
            if len(set(i).intersection(set(j))) > 4:
                if i in possible_nums:
                    possible_nums.remove(i)
                    
    return possible_nums

# 26. 회기
def regressionCount(regression_round):
    db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
    cursor1 = db_conn.cursor()
    cursor2 = db_conn.cursor()
    
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
    db_conn.close()
    return regression_count

# 26. 회기1
def regression1(possible_nums, predict_round):
    
    before_regression_count = regressionCount(predict_round-1)
    before_over_regression = []
    
    for i in range(0,len(before_regression_count)):
        if(before_regression_count[i] >= 3):
            before_over_regression.append(i+1)
    
    db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
    cursor = db_conn.cursor()
      
    current_regression = []
    
    for i in before_over_regression:
        cursor.execute("SELECT FIRST,SECOND,THIRD,FOURTH,FIVETH,SIXTH FROM CURRENT WHERE ROUND == {0}".format(predict_round-i))
        regression = cursor.fetchone()
        current_regression.append(regression)     
    db_conn.close()
    
    not_possible_nums = {i for i in possible_nums for j in current_regression if len(set(i).intersection(j)) > 2}
    possible_nums = set(possible_nums) - not_possible_nums    
    possible_nums = list(possible_nums)
   
    # for j in current_regression:
    #     possible_nums = [i for i in possible_nums if len(set(i).intersection(j)) < 3]
    
    return possible_nums

# 26. 회기2
def regression2(possible_nums, predict_round):
    db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
    cursor = db_conn.cursor()
    
    round_num = 1
    current_regression = []
    
    while(True):

        if round_num > 150:
            break
        
        cursor.execute("SELECT FIRST,SECOND,THIRD,FOURTH,FIVETH,SIXTH FROM CURRENT WHERE ROUND == {0}".format(predict_round-round_num))
        current = cursor.fetchone()
        current_regression.append(current)        
        round_num = round_num + 1
    db_conn.close()
    
    # for j in current_regression:
    #     possible_nums = [i for i in possible_nums if len(set(i).intersection(j)) < 4]
        
    not_possible_nums = {i for i in possible_nums for j in current_regression if len(set(i).intersection(j)) > 3}
    possible_nums = set(possible_nums) - not_possible_nums    
    possible_nums = list(possible_nums)
    
    return possible_nums

# 26. 회기3
def regression3(possible_nums, predict_round):
    db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
    cursor = db_conn.cursor()
    
    round_num = 1
    current_regression = []
    
    while(True):

        if predict_round - round_num == 0:
            break
        
        cursor.execute("SELECT FIRST,SECOND,THIRD,FOURTH,FIVETH,SIXTH FROM CURRENT WHERE ROUND == {0}".format(predict_round-round_num))
        current = cursor.fetchone()
        current_regression.append(current)        
        round_num = round_num + 1
    db_conn.close()
    
 
    not_possible_nums = {i for i in possible_nums for j in current_regression if len(set(i).intersection(j)) > 4}
    possible_nums = set(possible_nums) - not_possible_nums    
    possible_nums = list(possible_nums)
    return possible_nums

# 26. 회기4
def regression4(possible_nums, predict_round, regression_round, max_sum, min_sum):
    
    db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
    cursor = db_conn.cursor()   
    cursor.execute("SELECT FIRST,SECOND,THIRD,FOURTH,FIVETH,SIXTH FROM CURRENT WHERE ROUND < {0} AND ROUND > {1}".format(predict_round,predict_round-regression_round-1))
    current = cursor.fetchall()
    db_conn.close()
    
    sum_iter = []
    
    for i in possible_nums:
        sum_iter = [len(set(i).intersection(set(j))) for j in current]
        if not min_sum < sum(sum_iter) < max_sum:
            possible_nums.remove(i)
    
    return possible_nums

def start(predict_round):    
    # predict_round = ss[0]
    
    # 시작s
    start = time.time()
    # DB연결
    until_now_nums = untilNowNums()

    possible_nums = totalPossibleNums(until_now_nums)
    print("나올 수 있는 번호 조합 수			:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeFirstNum(possible_nums)
    print("1. 첫 수 < 15					:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeFinalNum(possible_nums)
    print("2. 마지막 수 > 35				:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeSumNums(possible_nums)
    print("3. 95 < 합계 < 175				:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeEndNums(possible_nums)
    print("4. 끝수							:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeOddNums(possible_nums)
    print("5. 홀짝							:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = addEdgeNums(possible_nums)
    print("6. 모서리 수						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeFrontBack3Nums(possible_nums)
    print("7. 세로 앞뒤 3줄					:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeEndSumNums(possible_nums)
    print("8. 10 < 끝합 < 35				:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeRow16Nums(possible_nums)
    print("9. 가로 연속 6줄					:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeContibuousNums(possible_nums)
    print("10. 3연속	수					:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeTriNums(possible_nums)
    print("11. 삼각패턴						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeRow3Nums(possible_nums)
    print("12. 가로 연속 3줄				:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeCol3Nums(possible_nums)
    print("13. 세로 연속 3줄				:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = addColorNums(possible_nums)
    print("14. 공 색깔						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeContibuous2(possible_nums)
    print("15. 연속 번호가 2				:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removePongNums(possible_nums)
    print("16. 퐁당퐁당						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeLeftRight2Nums(possible_nums)
    print("17. 세로 좌우 2줄				:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, predict_round, 40)
    print("18. GRA 40회						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, predict_round, 60)
    print("18. GRA 60회						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, predict_round, 70)
    print("18. GRA 70회						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, predict_round, 90)
    print("18. GRA 90회						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, predict_round, 100)
    print("18. GRA 100회					:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, predict_round, 130)
    print("18. GRA 130회					:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, predict_round, 140)
    print("18. GRA 140회					:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, predict_round, 190)
    print("18. GRA 190회					:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, predict_round, 200)
    print("18. GRA 200회					:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, predict_round, 210)
    print("18. GRA 210회					:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = recent10Notnum(possible_nums, predict_round)
    print("19. 최근 10회 	 				:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = recent5Notnum(possible_nums, predict_round)
    print("19. 최근 5회 	 				:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = recent3Notnum(possible_nums, predict_round)
    print("19. 최근 3회 	 				:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeRoundNum(possible_nums, predict_round)
    print("20. ROUND						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = finalNum(possible_nums)
    print("21. counter 					:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = finalNum2(possible_nums)
    print("21. counter2					:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = finalNum3(possible_nums)
    print("21. counter3					:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = fourWeek2(possible_nums, predict_round)
    print("22. 4주차						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = lastNull(possible_nums, predict_round)
    print("23. 지난회차						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = lastNull2(possible_nums, predict_round)
    print("23. 지난회차						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = averageNums(possible_nums)
    print("24. 평균							:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = regression1(possible_nums, predict_round)
    print("26. 회기1						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = regression2(possible_nums, predict_round)
    print("26. 회기2						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = regression3(possible_nums, predict_round)
    print("26. 회기3						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = regression4(possible_nums, predict_round,10,14,2)
    print("26. 회기4						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = regression4(possible_nums, predict_round,20,22,7)
    print("26. 회기4						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = regression4(possible_nums, predict_round,30,29,16)
    print("26. 회기4						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = regression4(possible_nums, predict_round,40,42,27)
    print("26. 회기4						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = regression4(possible_nums, predict_round,50,47,32)
    print("26. 회기4						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    
    print(" -------------------------------------------------------------------------------- ")
    print(" 총 수 							:", len(possible_nums),"걸린시간 : ", time.time() - start)
    
    last_nums = []
    for i in possible_nums:
        for j in range(0,len(i)):
            last_nums.append(i[j])
            
    container = collections.Counter(last_nums)
    print(container)
    
    # possible_winning = [i for i in possible_nums if len(set(i).intersection(set(ss[1:7]))) >= 5]
    
    # if len(possible_winning) > 0:
    #     return ("성공 : ", len(possible_nums), ss)
    # else:
    #     return ("실패 : ", len(possible_nums), ss)
    
# db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
# cursor = db_conn.cursor()
# cursor.execute("SELECT * FROM CURRENT WHERE 910 < ROUND")
# winning = cursor.fetchall()
# db_conn.close()
# if __name__ == '__main__':
#     pool = Pool(processes=4)
#     print(pool.map(start, winning))

start(942)
# regression1([11],942)