# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 21:59:35 2020

@author: choi
"""

import predict as predict

# 현재까지 당첨번호
until_now_nums = predict.untilNowNums()
# 938회 당첨번호
winning = [(938,4,8,10,16,31,36)]
# winning = until_now_nums
first_nums = []
final_nums = []
sum_nums = []
end_nums = []
odd_nums = []
edge_nums = []
frontback4_nums = []
endsum_nums = []
row16_nums = []
conti_nums = []
tri_nums = []
row3_nums = []
col3_nums = []
color_nums = []
conti2_nums = []
pingpong_nums = []
leftright_nums = []
beforewinning_nums = []
    
# 나올 수 있는 번호 조합
for i in winning:
    if i[1:7] not in predict.removeFirstNum([i[1:7]]):
        first_nums.append(i[0])        
    if i[1:7] not in predict.removeFinalNum([i[1:7]]):   
        final_nums.append(i[0])                               
    if i[1:7] not in predict.removeSumNums([i[1:7]]):   
        sum_nums.append(i[0])  
    if i[1:7] not in predict.removeEndNums([i[1:7]]):   
        end_nums.append(i[0])   
    if i[1:7] not in predict.removeOddNums([i[1:7]]):     
        odd_nums.append(i[0])   
    if i[1:7] not in predict.addEdgeNums([i[1:7]]):       
        edge_nums.append(i[0])   
    if i[1:7] not in predict.removeFrontBack4Nums([i[1:7]]):  
        frontback4_nums.append(i[0])
    if i[1:7] not in predict.removeEndSumNums([i[1:7]]):   
        endsum_nums.append(i[0])
    if i[1:7] not in predict.removeRow16Nums([i[1:7]]):    
        row16_nums.append(i[0]) 
    if i[1:7] not in predict.removeContibuousNums([i[1:7]]): 
        conti_nums.append(i[0])
    if i[1:7] not in predict.removeTriNums([i[1:7]]): 
        tri_nums.append(i[0])
    if i[1:7] not in predict.removeRow3Nums([i[1:7]]): 
        row3_nums.append(i[0])      
    if i[1:7] not in predict.removeCol3Nums([i[1:7]]): 
        col3_nums.append(i[0])      
    if i[1:7] not in predict.addColorNums([i[1:7]]):  
        color_nums.append(i[0])
    if i[1:7] not in predict.removeContibuous2([i[1:7]]):
        conti2_nums.append(i[0])     
    if i[1:7] not in predict.removePongNums([i[1:7]]):
        pingpong_nums.append(i[0])       
    if i[1:7] not in predict.removeLeftRight2Nums([i[1:7]]):
        leftright_nums.append(i[0]) 

# print("- 첫 수 15 초과					:", "%.2f%%" % (100 * len(first_nums)/len(until_now_nums))," : ",first_nums)
# print("- 마지막 수 30미만 	 			:", "%.2f%%" % (100 * len(final_nums)/len(until_now_nums))," : ",final_nums)
# print("- 합계 95미만, 176초과 	 		:", "%.2f%%" % (100 * len(sum_nums)/len(until_now_nums))," : ",sum_nums)
# print("- 끝수 3개 이상 동일 				:", "%.2f%%" % (100 * len(end_nums)/len(until_now_nums))," : ",end_nums)
# print("- 홀짝 6:0 		 				:", "%.2f%%" % (100 * len(odd_nums)/len(until_now_nums))," : ",odd_nums)
# print("- 모서리 수 0,5,6개	 			:", "%.2f%%" % (100 * len(edge_nums)/len(until_now_nums))," : ",edge_nums)
# print("- 세로 앞뒤 4줄에서만		 		:", "%.2f%%" % (100 * len(frontback4_nums)/len(until_now_nums))," : ",frontback4_nums)
# print("- 끝수 합 10~35아님				:", "%.2f%%" % (100 * len(endsum_nums)/len(until_now_nums))," : ",endsum_nums)
# print("- 가로 연속 6줄 					:", "%.2f%%" % (100 * len(row16_nums)/len(until_now_nums))," : ",row16_nums)
# print("- 3연속	 						:", "%.2f%%" % (100 * len(conti_nums)/len(until_now_nums))," : ",conti_nums)
# print("- 삼각패턴 						:", "%.2f%%" % (100 * len(tri_nums)/len(until_now_nums))," : ",tri_nums)
# print("- 가로 연속 3줄 					:", "%.2f%%" % (100 * len(row3_nums)/len(until_now_nums))," : ",row3_nums)
# print("- 세로 연속 3줄 					:", "%.2f%%" % (100 * len(col3_nums)/len(until_now_nums))," : ",col3_nums)
# print("- 공 색깔 1,2,5,6개 				:", "%.2f%%" % (100 * len(color_nums)/len(until_now_nums))," : ",color_nums)
# print("- 연속 번호가 2번 					:", "%.2f%%" % (100 * len(conti2_nums)/len(until_now_nums))," : ",conti2_nums)
# print("- 퐁당퐁당 나온 수 				:", "%.2f%%" % (100 * len(pingpong_nums)/len(until_now_nums))," : ",pingpong_nums)
# print("- 세로 좌우 2줄					:", "%.2f%%" % (100 * len(leftright_nums)/len(until_now_nums))," : ",leftright_nums)

print("- 첫 수 15 초과					:", "%.2f%%" % (100 * len(first_nums)/len(until_now_nums)))
print("- 마지막 수 30미만 	 			:", "%.2f%%" % (100 * len(final_nums)/len(until_now_nums)))
print("- 합계 95미만, 176초과 	 		:", "%.2f%%" % (100 * len(sum_nums)/len(until_now_nums)))
print("- 끝수 3개 이상 동일 				:", "%.2f%%" % (100 * len(end_nums)/len(until_now_nums)))
print("- 홀짝 6:0 		 				:", "%.2f%%" % (100 * len(odd_nums)/len(until_now_nums)))
print("- 모서리 수 0,5,6개	 			:", "%.2f%%" % (100 * len(edge_nums)/len(until_now_nums)))
print("- 세로 앞뒤 4줄에서만		 		:", "%.2f%%" % (100 * len(frontback4_nums)/len(until_now_nums)))
print("- 끝수 합 10~35아님				:", "%.2f%%" % (100 * len(endsum_nums)/len(until_now_nums)))
print("- 가로 연속 6줄 					:", "%.2f%%" % (100 * len(row16_nums)/len(until_now_nums)))
print("- 3연속	 						:", "%.2f%%" % (100 * len(conti_nums)/len(until_now_nums)))
print("- 삼각패턴 						:", "%.2f%%" % (100 * len(tri_nums)/len(until_now_nums)))
print("- 가로 연속 3줄 					:", "%.2f%%" % (100 * len(row3_nums)/len(until_now_nums)))
print("- 세로 연속 3줄 					:", "%.2f%%" % (100 * len(col3_nums)/len(until_now_nums)))
print("- 공 색깔 1,2,5,6개 				:", "%.2f%%" % (100 * len(color_nums)/len(until_now_nums)))
print("- 연속 번호가 2번 					:", "%.2f%%" % (100 * len(conti2_nums)/len(until_now_nums)))
print("- 퐁당퐁당 나온 수 				:", "%.2f%%" % (100 * len(pingpong_nums)/len(until_now_nums)))
print("- 세로 좌우 2줄					:", "%.2f%%" % (100 * len(leftright_nums)/len(until_now_nums)))