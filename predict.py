# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 17:02:01 2020

@author: choi
"""

import sqlite3
import time
import itertools
import collections
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
    # front4 = {1,8,15,22,29,36,43,2,9,16,23,30,37,44,3,10,17,24,31,38,45,4,11,18,25,32,39}
    # back4 = {4,11,18,25,32,39,5,12,19,26,33,40,6,13,20,27,34,41,7,14,21,27,35,42}
    # possible_nums = [i for i in possible_nums if len(set(i).intersection(front4)) < 6] # 세로 앞 4줄에서만 나온 수
    # possible_nums = [i for i in possible_nums if len(set(i).intersection(back4)) < 6] # 세로 뒤 4줄에서만 나온 수
    front3 = {1,8,15,22,29,36,43,2,9,16,23,30,37,44,3,10,17,24,31,38,45}
    back3 = {5,12,19,26,33,40,6,13,20,27,34,41,7,14,21,27,35,42}
    possible_nums = [i for i in possible_nums if len(set(i).intersection(front3)) < 6] # 세로 앞 4줄에서만 나온 수
    possible_nums = [i for i in possible_nums if len(set(i).intersection(back3)) < 6] # 세로 뒤 4줄에서만 나온 수
    return possible_nums

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
        
        if 2 < color_count < 6:
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

    pong1_list = [i for i in possible_nums if len(set(i).intersection(c1)) < 6]
    pong2_list = [i for i in pong1_list if len(set(i).intersection(c2)) < 6]
    pong3_list = [i for i in pong2_list if len(set(i).intersection(c3)) < 6]
    return pong3_list

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
    remove_end_nums = [i for i in possible_nums if len(set([i[0]%10,i[1]%10,i[2]%10,i[3]%10,i[4]%10,i[5]%10])) > 3]#4,1,8,9,2,5
    return remove_end_nums

#삼각패턴
def removeTriNums(possible_nums):
    # left_top = {1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,18,19,22,23,24,25,29,3,31,36,37,43}
    left_bottom = {1,8,9,15,16,17,22,23,24,25,29,3,31,32,33,36,37,38,39,40,41,43,44,45}
    right_top = {1,2,3,4,5,6,7,9,10,11,12,13,14,17,18,19,20,21,25,26,27,28,33,34,35,41,42}
    right_bottom = {7,13,14,19,20,21,25,26,27,28,31,32,33,34,35,37,38,39,40,41,42,43,44,45} 

    remove_tri_nums = [i for i in possible_nums if len(set(i).intersection(left_bottom)) != 6 and
                       len(set(i).intersection(right_bottom)) != 6 and len(set(i).intersection(right_top)) != 6]
    return remove_tri_nums

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
    
def countGRA(possible_nums, predict_round, count):
    gra = setGRA(predict_round,count)
    gra_count = recentty(predict_round, count)

    green_add_nums = [i for i in possible_nums if len(set(i).intersection(set(gra[0]))) in gra_count[0]]
    remove_red_nums = [i for i in green_add_nums if len(set(i).intersection(set(gra[1]))) in gra_count[1]]
    remove_average_nums = [i for i in remove_red_nums if len(set(i).intersection(set(gra[2]))) in gra_count[2]]
    
    return remove_average_nums

# 이번회차 939 예측회차 940
def removeRoundNum(possible_nums):
    #라운드 13
    possible_nums = [i for i in possible_nums if 13 not in i]
    #2주연속 같은번호
    possible_nums = [i for i in possible_nums if 4 not in i]
    #보너스번호 제외
    possible_nums = [i for i in possible_nums if 6 not in i]
    #4구 +1
    possible_nums = [i for i in possible_nums if 40 not in i]
    #2구 +1
    possible_nums = [i for i in possible_nums if 12 not in i]
    #보너스볼 -6구
    possible_nums = [i for i in possible_nums if 39 not in i]
    # 합계에서 앞에 두자리
    possible_nums = [i for i in possible_nums if 16 not in i]
    # 쌍둥이 수 연속
    possible_nums = [i for i in possible_nums if 11 not in i]
    
    #지난회차 같은번호 2개 이하
    remove_before_winning_num = {4,11,28,39,42,45}
    possible_nums = [i for i in possible_nums if len(set(i).intersection(remove_before_winning_num)) < 3]
    
    return possible_nums

def removeYoutubeNum(possible_nums):
    ##초개미
    #전회차 플러스
    possible_nums = [i for i in possible_nums if 7 not in i]
    #한템포느린
    late = {8,10,11,19,20,24,25,33,34}
    possible_nums = [i for i in possible_nums if 0 < len(set(i).intersection(late)) < 3]
    #마방진
    ma = {42,44,4,43,3,12,2,11,20}
    possible_nums = [i for i in possible_nums if len(set(i).intersection(ma)) < 3]
    #마방진 가로구간
    row_num5 = {13,15,24,33,42,44,4}
    possible_nums = [i for i in possible_nums if 0 < len(set(i).intersection(row_num5)) < 4]
    #일본로또 제외수 05#실패939
    possible_nums = [i for i in possible_nums if 5 not in i]
    #이스라엘 제외수 20#실패940
    # possible_nums = [i for i in possible_nums if 20 not in i]
    #뉴질랜드 제외수 37
    possible_nums = [i for i in possible_nums if 37 not in i]
    
    #밀크님 제외수 27
    possible_nums = [i for i in possible_nums if 27 not in i]
    #로또박 제외수 43
    possible_nums = [i for i in possible_nums if 43 not in i]
    #꿀꿀이 제외수 14
    possible_nums = [i for i in possible_nums if 14 not in i]
    #행운의 신 제외수 30
    possible_nums = [i for i in possible_nums if 30 not in i]
    
    ##로또9단
    park_nums = {28,39,42,31,22,40,7,17,18,20,32,38,44,1,3,33,23,27,15,37,14,25,35,43,21,12,19,41,24,26}
    possible_nums = [i for i in possible_nums if len(set(i).intersection(park_nums)) > 3]
    
    ##행운의 신
    # 타사이트 고정 수 빈도패턴 ( 2~3개 ) ##주의(이전꺼 아님)
    luck_num = {24,4,17,5,6,8,14,15,23,25}
    possible_nums = [i for i in possible_nums if 1 < len(set(i).intersection(luck_num)) < 4]
    # 타사이트 제외 수 빈도패턴( 2~3개 )
    luck_num2 = {1,5,8,9,13,20,23,24,25,32,34,35,36,43,45}
    possible_nums = [i for i in possible_nums if 1 < len(set(i).intersection(luck_num2)) < 4]
    #최종 30수 ( 4 이상 )
    luck_num_total = {1,4,5,6,7,9,10,12,13,14,15,17,18,20,21,22,23,24,25,27,28,32,33,34,35,38,4,41,43,44}
    possible_nums = [i for i in possible_nums if 3 < len(set(i).intersection(luck_num_total)) < 6]
    
    ##짜장짬뽕
    week_no_show_num = {19,24,34,41}
    possible_nums = [i for i in possible_nums if len(set(i).intersection(week_no_show_num)) >= 1]
    possible_nums = [i for i in possible_nums if 17 not in i] #(당첨날짜 : 전회차에 나왔기때문에...) 2
    possible_nums = [i for i in possible_nums if 5 not in i] #(당첨날짜 : 전회차에 나왔기때문에...)  3
    
    ##CH소비월드
    ch_num = {3,5,11,12,13,14,15,16,17,21,22,23,26,28,32,36,38,43}
    possible_nums = [i for i in possible_nums if 1 < len(set(i).intersection(ch_num)) < 5]
    ch_num2 = {12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27} # 안나온 간격이 15개 이상일때, 2개~5개
    possible_nums = [i for i in possible_nums if 1 < len(set(i).intersection(ch_num2)) < 6]
    ch_num3 = {16,22,23,29,30,17,18,24,25,31,12,19,20,26,27} 
    possible_nums = [i for i in possible_nums if 0 < len(set(i).intersection(ch_num3))]
    possible_nums = [i for i in possible_nums if 35 not in i]
    possible_nums = [i for i in possible_nums if 32 not in i]
    possible_nums = [i for i in possible_nums if 28 not in i]
    possible_nums = [i for i in possible_nums if 18 not in i]  
    
    return possible_nums

# 이전회차 같은번호 4개 이하
def removeBeforeWinningNums(possible_nums):
    db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
    cursor = db_conn.cursor()
    cursor.execute("SELECT FIRST,SECOND,THIRD,FOURTH,FIVETH,SIXTH FROM CURRENT")
    current = cursor.fetchall()
    db_conn.close()
  
    for i in possible_nums:
        for j in current:
            if len(set(i).intersection(set(j))) > 3:
                    if i in possible_nums:
                        possible_nums.remove(i)
                    
    return possible_nums

def finalNum(possible_nums):
    all_list = []
    for i in possible_nums:
        for j in range(0,len(i)):
            all_list.append(i[j])
    count_list = collections.Counter(all_list)
    print(count_list)
    
    counter = []
    remove_counter = []
    
    for k,v in count_list.items():
        if v > 400:
            counter.append(k)#counter = {15,24}
        if v < 65:
            remove_counter.append(k) #conter_remove = {29,33,10}

    counter = set(counter)
    remove_counter = set(remove_counter)
    print("가장 많이 나온 수: ",counter)
    print("가장 적게 나온 수: ",remove_counter)
    possible_nums = [i for i in possible_nums if len(set(i).intersection(counter)) == 2]
    possible_nums = [i for i in possible_nums if len(set(i).intersection(remove_counter)) == 0]

    return possible_nums

def start():

    # 시작
    start = time.time()
    # DB연결 및 현재(939)까지 나온 번호
    until_now_nums = untilNowNums()

    possible_nums = totalPossibleNums(until_now_nums)
    print("나올 수 있는 번호 조합 수 			:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeFirstNum(possible_nums)
    print("1.첫 수가 15초과 제거 수 				:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeFinalNum(possible_nums)
    print("2.마지막 수가 30미만 제거 수 			:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeSumNums(possible_nums)
    print("3.합계 95미만, 176초과 제거 수 		:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeEndNums(possible_nums)
    print("4.끝수가 동일한 것 1~2개 출현 		:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeOddNums(possible_nums)
    print("5.홀짝 6:0 제거 수 					:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = addEdgeNums(possible_nums)
    print("6.모서리 수가 1~4개 포함 수 			:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeFrontBack4Nums(possible_nums)
    print("7.세로 앞뒤 4줄에서만 제거 수 		:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeEndSumNums(possible_nums)
    print("8.끝수 합이 10~35아닌 수 제거 		:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeRow16Nums(possible_nums)
    print("9.가로 연속 6줄 나온 수 제거 			:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeContibuousNums(possible_nums)
    print("10.3연속 수 제거 					:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeTriNums(possible_nums)
    print("11.삼각패턴 제거 					:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeRow3Nums(possible_nums)
    print("12.가로 연속 3줄에서만 나온 수 제거 	:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeCol3Nums(possible_nums)
    print("13.세로 연속 3줄에서만 나온 수 제거 	:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = addColorNums(possible_nums)
    print("14.공 색깔 3~5개 출현 수 			:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeContibuous2(possible_nums)
    print("15.연속 번호가 2가지 이상 제거 		:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removePongNums(possible_nums)
    print("16.퐁당퐁당 나온 수 제거 				:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeLeftRight2Nums(possible_nums)
    print("17.세로 좌우 2줄에서만 나온 수 제거 	:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, 940,40)
    print("18.최근 40회 						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, 940,60)
    print("18.최근 60회 						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, 940,70)
    print("18.최근 70회 						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, 940,90)
    print("18.최근 90회 						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, 940,100)
    print("18.최근 100회 						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, 940,130)
    print("18.최근 130회 						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, 940,140)
    print("18.최근 140회 						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, 940,190)
    print("18.최근 190회 						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, 940,200)
    print("18.최근 200회 						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = countGRA(possible_nums, 940,210)
    print("18.최근 210회 						:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeRoundNum(possible_nums)
    print("19.940회 							:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeYoutubeNum(possible_nums)
    print("20.Youtube 							:", len(possible_nums),"걸린시간 : ", time.time() - start)
    possible_nums = removeBeforeWinningNums(possible_nums)
    print("21.이때까지 나온 수 동일 4개 이하 	:", len(possible_nums),"걸린시간 : ", time.time() - start)
    print(" -------------------------------------------------------------------------------- ")
    print(" 총 수 								:", len(possible_nums),"걸린시간 : ", time.time() - start)

    possible_nums = finalNum(possible_nums)
    print("counter 							:", len(possible_nums),"걸린시간 : ", time.time() - start)
    
# start()