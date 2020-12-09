# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 21:59:35 2020

@author: choi
"""

import predict as predict

winning = [(940,3,15,20,22,24,41),(939,4,11,28,39,42,45),(938,14,8,10,16,31,36),(937,2,10,13,22,29,40),(936,7,11,13,17,18,29),(935,4,10,20,32,38,44),(934,1,3,30,33,36,39),(933,23,27,29,31,36,45),(932,1,6,15,36,37,38),(931,14,15,23,25,35,43),(930,8,21,25,38,39,44)]
# winning = [(940,3,15,20,22,24,41)]
# winning = [(939,4,11,28,39,42,45)]
# winning = [(938,14,8,10,16,31,36)]
# winning = [(937,2,10,13,22,29,40)]
# winning = [(936,7,11,13,17,18,29)]		#Error : 끝수 30 미만..
# winning = [(935,4,10,20,32,38,44)]		#Error : 모두 짝수임..
# winning = [(934,1,3,30,33,36,39)]
# winning = [(933,23,27,29,31,36,45)]		#Error : 1.23부터시작, 합계 176초과
# winning = [(932,1,6,15,36,37,38)]			#Error : 36,37,38(3연속수)
# winning = [(931,14,15,23,25,35,43)]       #Error : 15,25,35(5끝자리 3개)
# winning = [(930,8,21,25,38,39,44)]

first_nums = []         #1
final_nums = []         #2
sum_nums = []           #3
end_nums = []           #4
odd_nums = []           #5
edge_nums = []          #6
frontback4_nums = []    #7
endsum_nums = []        #8
row16_nums = []         #9
conti_nums = []         #10
tri_nums = []           #11
row3_nums = []          #12
col3_nums = []          #13
color_nums = []         #14
conti2_nums = []        #15
pingpong_nums = []      #16
leftright_nums = []     #17
green_red_nums_40 = []  #18
green_red_nums_60 = []  #18
green_red_nums_70 = []  #18
green_red_nums_90 = []  #18
green_red_nums_100=[]   #18
green_red_nums_130=[]   #18
green_red_nums_140=[]   #18
green_red_nums_190=[]   #18
green_red_nums_200=[]   #18
green_red_nums_210=[]   #18
round_nums = []         #19
youtube_nums = []       #20
beforewinning_nums = [] #21

# 나올 수 있는 번호 조합
for i in winning:
    if i[1:7] in predict.removeFirstNum([i[1:7]]):
        first_nums.append(i[0])        
    if i[1:7] in predict.removeFinalNum([i[1:7]]):   
        final_nums.append(i[0])                               
    if i[1:7] in predict.removeSumNums([i[1:7]]):   
        sum_nums.append(i[0])  
    if i[1:7] in predict.removeEndNums([i[1:7]]):   
        end_nums.append(i[0])   
    if i[1:7] in predict.removeOddNums([i[1:7]]):     
        odd_nums.append(i[0])   
    if i[1:7] in predict.addEdgeNums([i[1:7]]):       
        edge_nums.append(i[0])   
    if i[1:7] in predict.removeFrontBack4Nums([i[1:7]]):  
        frontback4_nums.append(i[0])
    if i[1:7] in predict.removeEndSumNums([i[1:7]]):   
        endsum_nums.append(i[0])
    if i[1:7] in predict.removeRow16Nums([i[1:7]]):    
        row16_nums.append(i[0]) 
    if i[1:7] in predict.removeContibuousNums([i[1:7]]): 
        conti_nums.append(i[0])
    if i[1:7] in predict.removeTriNums([i[1:7]]): 
        tri_nums.append(i[0])
    if i[1:7] in predict.removeRow3Nums([i[1:7]]): 
        row3_nums.append(i[0])      
    if i[1:7] in predict.removeCol3Nums([i[1:7]]): 
        col3_nums.append(i[0])      
    if i[1:7] in predict.addColorNums([i[1:7]]):  
        color_nums.append(i[0])
    if i[1:7] in predict.removeContibuous2([i[1:7]]):
        conti2_nums.append(i[0])     
    if i[1:7] in predict.removePongNums([i[1:7]]):
        pingpong_nums.append(i[0])       
    if i[1:7] in predict.removeLeftRight2Nums([i[1:7]]):
        leftright_nums.append(i[0])
    if i[1:7] in predict.countGRA([i[1:7]],i[0],40):
        green_red_nums_40.append(i[0])
    if i[1:7] in predict.countGRA([i[1:7]],i[0],60):
        green_red_nums_60.append(i[0])
    if i[1:7] in predict.countGRA([i[1:7]],i[0],70):
        green_red_nums_70.append(i[0])
    if i[1:7] in predict.countGRA([i[1:7]],i[0],90):
        green_red_nums_90.append(i[0])
    if i[1:7] in predict.countGRA([i[1:7]],i[0],100):
        green_red_nums_100.append(i[0])
    if i[1:7] in predict.countGRA([i[1:7]],i[0],130):
        green_red_nums_130.append(i[0])
    if i[1:7] in predict.countGRA([i[1:7]],i[0],140):
        green_red_nums_140.append(i[0])
    if i[1:7] in predict.countGRA([i[1:7]],i[0],190):
        green_red_nums_190.append(i[0])
    if i[1:7] in predict.countGRA([i[1:7]],i[0],200):
        green_red_nums_200.append(i[0])
    if i[1:7] in predict.countGRA([i[1:7]],i[0],210):
        green_red_nums_210.append(i[0])
    # if i[1:7] in predict.removeRoundNum([i[1:7]]):
    #     round_nums.append(i[0])
    # if i[1:7] in predict.removeYoutubeNum([i[1:7]]):
    #     youtube_nums.append(i[0])
    # if i[1:7] in predict.removeBeforeWinningNums([i[1:7]]):
    #     beforewinning_nums.append(i[0])

print("- 1.첫 수 15 초과					:", "%.2f%%" % (100 * len(first_nums)/len(winning)))
print("- 2.마지막 수 30미만 	 			:", "%.2f%%" % (100 * len(final_nums)/len(winning)))
print("- 3.합계 95미만, 176초과 	 		:", "%.2f%%" % (100 * len(sum_nums)/len(winning)))
print("- 4.끝수 3개 이상 동일 				:", "%.2f%%" % (100 * len(end_nums)/len(winning)))
print("- 5.홀짝 6:0 		 				:", "%.2f%%" % (100 * len(odd_nums)/len(winning)))
print("- 6.모서리 수 0,5,6개	 			:", "%.2f%%" % (100 * len(edge_nums)/len(winning)))
print("- 7.세로 앞뒤 3줄에서만		 		:", "%.2f%%" % (100 * len(frontback4_nums)/len(winning)))
print("- 8.끝수 합 10~35아님				:", "%.2f%%" % (100 * len(endsum_nums)/len(winning)))
print("- 9.가로 연속 6줄 					:", "%.2f%%" % (100 * len(row16_nums)/len(winning)))
print("- 10.3연속	 						:", "%.2f%%" % (100 * len(conti_nums)/len(winning)))
print("- 11.삼각패턴 						:", "%.2f%%" % (100 * len(tri_nums)/len(winning)))
print("- 12.가로 연속 3줄 					:", "%.2f%%" % (100 * len(row3_nums)/len(winning)))
print("- 13.세로 연속 3줄 					:", "%.2f%%" % (100 * len(col3_nums)/len(winning)))
print("- 14.공 색깔 1,2,5,6개 				:", "%.2f%%" % (100 * len(color_nums)/len(winning)))
print("- 15.연속 번호가 2번 				:", "%.2f%%" % (100 * len(conti2_nums)/len(winning)))
print("- 16.퐁당퐁당 나온 수 				:", "%.2f%%" % (100 * len(pingpong_nums)/len(winning)))
print("- 17.세로 좌우 2줄					:", "%.2f%%" % (100 * len(leftright_nums)/len(winning)))
print("- 18.GREEN,RED,평균40				:", "%.2f%%" % (100 * len(green_red_nums_40)/len(winning)))
print("- 18.GREEN,RED,평균60				:", "%.2f%%" % (100 * len(green_red_nums_60)/len(winning)))
print("- 18.GREEN,RED,평균70				:", "%.2f%%" % (100 * len(green_red_nums_70)/len(winning)))
print("- 18.GREEN,RED,평균90				:", "%.2f%%" % (100 * len(green_red_nums_90)/len(winning)))
print("- 18.GREEN,RED,평균100				:", "%.2f%%" % (100 * len(green_red_nums_100)/len(winning)))
print("- 18.GREEN,RED,평균130				:", "%.2f%%" % (100 * len(green_red_nums_130)/len(winning)))
print("- 18.GREEN,RED,평균140				:", "%.2f%%" % (100 * len(green_red_nums_140)/len(winning)))
print("- 18.GREEN,RED,평균190				:", "%.2f%%" % (100 * len(green_red_nums_190)/len(winning)))
print("- 18.GREEN,RED,평균200				:", "%.2f%%" % (100 * len(green_red_nums_200)/len(winning)))
print("- 18.GREEN,RED,평균210				:", "%.2f%%" % (100 * len(green_red_nums_210)/len(winning)))
# print("- 19.Round							:", "%.2f%%" % (100 * len(round_nums)/len(winning)))
# print("- 20.Youtube						:", "%.2f%%" % (100 * len(youtube_nums)/len(winning)))
# print("- 21.이때까지 나온번호				:", "%.2f%%" % (100 * len(beforewinning_nums)/len(winning)))
