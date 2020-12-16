# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 21:59:35 2020

@author: choi

최근 30회 90% 이상

"""

import predict as predict
import sqlite3

db_conn = sqlite3.connect("LOTTO.db", isolation_level=None)
cursor = db_conn.cursor()
cursor.execute("SELECT * FROM CURRENT WHERE 919 < ROUND")
winning = cursor.fetchall()
db_conn.close()  

# winning = [(941,3,15,20,22,24,41)]

first_nums = []         #1
final_nums = []         #2
sum_nums = []           #3
# end_nums = []           #4
# odd_nums = []           #5
# edge_nums = []          #6
# frontback4_nums = []    #7
# endsum_nums = []        #8
# row16_nums = []         #9
# conti_nums = []         #10
# tri_nums = []           #11
# row3_nums = []          #12
# col3_nums = []          #13
# color_nums = []         #14
# conti2_nums = []        #15
# pingpong_nums = []      #16
# leftright_nums = []     #17
# green_red_nums_40 = []  #18
# green_red_nums_60 = []  #18
# green_red_nums_70 = []  #18
# green_red_nums_90 = []  #18
# green_red_nums_100=[]   #18
# green_red_nums_130=[]   #18
# green_red_nums_140=[]   #18
# green_red_nums_190=[]   #18
# green_red_nums_200=[]   #18
# green_red_nums_210=[]   #18
# recent_not10_nums = []  #19
# recent_not5_nums = []   #19
# recent_not3_nums = []   #19
# round_nums = []         #20
# four_week_nums = [] #22
# last_null_nums = []
# last_null_nums2 = []
# before_last_num = []
# youtube_nums = []       #21
# beforewinning_nums = [] #22

regression1 = [] #26-1
regression2 = [] #26-2
regression3 = [] #26-3
regression4 = [] #26-4

# total_nums = []

# 나올 수 있는 번호 조합
for i in winning:
    # if i[1:7] in predict.removeFirstNum([i[1:7]]):
    #     first_nums.append(i[0])        
    # if i[1:7] in predict.removeFinalNum([i[1:7]]):   
    #     final_nums.append(i[0])                               
    # if i[1:7] in predict.removeSumNums([i[1:7]]):   
    #     sum_nums.append(i[0])  
    # if i[1:7] in predict.removeEndNums([i[1:7]]):   
    #     end_nums.append(i[0])   
    # if i[1:7] in predict.removeOddNums([i[1:7]]):     
    #     odd_nums.append(i[0])   
    # if i[1:7] in predict.addEdgeNums([i[1:7]]):       
    #     edge_nums.append(i[0])   
    # if i[1:7] in predict.removeFrontBack4Nums([i[1:7]]):  
    #     frontback4_nums.append(i[0])
    # if i[1:7] in predict.removeEndSumNums([i[1:7]]):   
    #     endsum_nums.append(i[0])
    # if i[1:7] in predict.removeRow16Nums([i[1:7]]):    
    #     row16_nums.append(i[0]) 
    # if i[1:7] in predict.removeContibuousNums([i[1:7]]): 
    #     conti_nums.append(i[0])
    # if i[1:7] in predict.removeTriNums([i[1:7]]): 
    #     tri_nums.append(i[0])
    # if i[1:7] in predict.removeRow3Nums([i[1:7]]): 
    #     row3_nums.append(i[0])      
    # if i[1:7] in predict.removeCol3Nums([i[1:7]]): 
    #     col3_nums.append(i[0])      
    # if i[1:7] in predict.addColorNums([i[1:7]]):  
    #     color_nums.append(i[0])
    # if i[1:7] in predict.removeContibuous2([i[1:7]]):
    #     conti2_nums.append(i[0])     
    # if i[1:7] in predict.removePongNums([i[1:7]]):
    #     pingpong_nums.append(i[0])       
    # if i[1:7] in predict.removeLeftRight2Nums([i[1:7]]):
    #     leftright_nums.append(i[0])
    # if i[1:7] in predict.countGRA([i[1:7]],i[0],40):
    #     green_red_nums_40.append(i[0])
    # if i[1:7] in predict.countGRA([i[1:7]],i[0],60):
    #     green_red_nums_60.append(i[0])
    # if i[1:7] in predict.countGRA([i[1:7]],i[0],70):
    #     green_red_nums_70.append(i[0])
    # if i[1:7] in predict.countGRA([i[1:7]],i[0],90):
    #     green_red_nums_90.append(i[0])
    # if i[1:7] in predict.countGRA([i[1:7]],i[0],100):
    #     green_red_nums_100.append(i[0])
    # if i[1:7] in predict.countGRA([i[1:7]],i[0],130):
    #     green_red_nums_130.append(i[0])
    # if i[1:7] in predict.countGRA([i[1:7]],i[0],140):
    #     green_red_nums_140.append(i[0])
    # if i[1:7] in predict.countGRA([i[1:7]],i[0],190):
    #     green_red_nums_190.append(i[0])
    # if i[1:7] in predict.countGRA([i[1:7]],i[0],200):
    #     green_red_nums_200.append(i[0])
    # if i[1:7] in predict.countGRA([i[1:7]],i[0],210):
    #     green_red_nums_210.append(i[0])
    # if i[1:7] in predict.recent10Notnum([i[1:7]],i[0]):
    #     recent_not10_nums.append(i[0])
    # if i[1:7] in predict.recent5Notnum([i[1:7]],i[0]):
    #     recent_not5_nums.append(i[0])
    # if i[1:7] in predict.recent3Notnum([i[1:7]],i[0]):
    #     recent_not3_nums.append(i[0])
    # if i[1:7] in predict.removeRoundNum([i[1:7]],i[0]):
    #     round_nums.append(i[0])
    # if i[1:7] in predict.fourWeek2([i[1:7]],i[0]):
    #     four_week_nums.append(i[0])
    # if i[1:7] in predict.lastNull([i[1:7]],i[0]):
    #     last_null_nums.append(i[0])
    # if i[1:7] in predict.lastNull2([i[1:7]],i[0]):
    #     last_null_nums2.append(i[0])
    # if i[1:7] in predict.averageNums([i[1:7]]):
    #     before_last_num.append(i[0])
    # if i[1:7] in predict.removeYoutubeNum([i[1:7]]):
    #     youtube_nums.append(i[0])
    # if i[1:7] in predict.removeBeforeWinningNums([i[1:7]],i[0]):
    #     beforewinning_nums.append(i[0])
    if i[1:7] in predict.regression1([i[1:7]],i[0]):
        regression1.append(i[0])
    if i[1:7] in predict.regression2([i[1:7]],i[0]):
        regression2.append(i[0])
    if i[1:7] in predict.regression3([i[1:7]],i[0]):
        regression3.append(i[0])
    if i[1:7] in predict.regression4([i[1:7]],i[0]):
        regression4.append(i[0])
   
# print("- 1. 첫 수 15 이하 확률					:", "%.2f%%" % (100 * len(first_nums)/len(winning)))
# print("- 2. 마지막 수 35 이상 확률 				:", "%.2f%%" % (100 * len(final_nums)/len(winning)))
# print("- 3. 합계 95~175 확률 			 		:", "%.2f%%" % (100 * len(sum_nums)/len(winning)))
# print("- 4.끝수 3개 이상 동일 				:", "%.2f%%" % (100 * len(end_nums)/len(winning)))
# print("- 5.홀짝 6:0 		 				:", "%.2f%%" % (100 * len(odd_nums)/len(winning)))
# print("- 6.모서리 수 0,5,6개	 			:", "%.2f%%" % (100 * len(edge_nums)/len(winning)))
# print("- 7.세로 앞뒤 3줄에서만		 		:", "%.2f%%" % (100 * len(frontback4_nums)/len(winning)))
# print("- 8.끝수 합 10~35아님				:", "%.2f%%" % (100 * len(endsum_nums)/len(winning)))
# print("- 9.가로 연속 6줄 					:", "%.2f%%" % (100 * len(row16_nums)/len(winning)))
# print("- 10.3연속	 						:", "%.2f%%" % (100 * len(conti_nums)/len(winning)))
# print("- 11.삼각패턴 						:", "%.2f%%" % (100 * len(tri_nums)/len(winning)))
# print("- 12.가로 연속 3줄 					:", "%.2f%%" % (100 * len(row3_nums)/len(winning)))
# print("- 13.세로 연속 3줄 					:", "%.2f%%" % (100 * len(col3_nums)/len(winning)))
# print("- 14.공 색깔 1,2,5,6개 				:", "%.2f%%" % (100 * len(color_nums)/len(winning)))
# print("- 15.연속 번호가 2번 				:", "%.2f%%" % (100 * len(conti2_nums)/len(winning)))
# print("- 16.퐁당퐁당 나온 수 				:", "%.2f%%" % (100 * len(pingpong_nums)/len(winning)))
# print("- 17.세로 좌우 2줄					:", "%.2f%%" % (100 * len(leftright_nums)/len(winning)))
# print("- 18.GREEN,RED,평균40				:", "%.2f%%" % (100 * len(green_red_nums_40)/len(winning)))
# print("- 18.GREEN,RED,평균60				:", "%.2f%%" % (100 * len(green_red_nums_60)/len(winning)))
# print("- 18.GREEN,RED,평균70				:", "%.2f%%" % (100 * len(green_red_nums_70)/len(winning)))
# print("- 18.GREEN,RED,평균90				:", "%.2f%%" % (100 * len(green_red_nums_90)/len(winning)))
# print("- 18.GREEN,RED,평균100				:", "%.2f%%" % (100 * len(green_red_nums_100)/len(winning)))
# print("- 18.GREEN,RED,평균130				:", "%.2f%%" % (100 * len(green_red_nums_130)/len(winning)))
# print("- 18.GREEN,RED,평균140				:", "%.2f%%" % (100 * len(green_red_nums_140)/len(winning)))
# print("- 18.GREEN,RED,평균190				:", "%.2f%%" % (100 * len(green_red_nums_190)/len(winning)))
# print("- 18.GREEN,RED,평균200				:", "%.2f%%" % (100 * len(green_red_nums_200)/len(winning)))
# print("- 18.GREEN,RED,평균210				:", "%.2f%%" % (100 * len(green_red_nums_210)/len(winning)))
# print("- 19.최근 안나온 번호10				:", "%.2f%%" % (100 * len(recent_not10_nums)/len(winning)))
# print("- 19.최근 안나온 번호5				:", "%.2f%%" % (100 * len(recent_not5_nums)/len(winning)))
# print("- 19.최근 안나온 번호3				:", "%.2f%%" % (100 * len(recent_not3_nums)/len(winning)))
# print("- 19.4주차 2							:", "%.2f%%" % (100 * len(four_week_nums)/len(winning)))
# print("- 19. 이전번호5						:", "%.2f%%" % (100 * len(last_null_nums)/len(winning)))
# print("- 19. 이전번호52						:", "%.2f%%" % (100 * len(last_null_nums2)/len(winning)))
# print("- 19. 이전번호미자막					:", "%.2f%%" % (100 * len(before_last_num)/len(winning)))
# print("- 20.Round							:", "%.2f%%" % (100 * len(round_nums)/len(winning)))
# print("- 21.Youtube						:", "%.2f%%" % (100 * len(youtube_nums)/len(winning)))
# print("- 22.이때까지 나온번호				:", "%.2f%%" % (100 * len(beforewinning_nums)/len(winning)))
print("- 26.회기1							:", "%.2f%%" % (100 * len(regression1)/len(winning)))
print("- 26.회기2							:", "%.2f%%" % (100 * len(regression2)/len(winning)))
print("- 26.회기3							:", "%.2f%%" % (100 * len(regression3)/len(winning)))
print("- 26.회기4							:", "%.2f%%" % (100 * len(regression4)/len(winning)))
# print("- total								:", "%.2f%%" % (100 * len(total_nums)/len(winning)))
