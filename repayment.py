import os
import sys
import re
import time
import math
import numpy_financial

float_orginal_nominal_rate_total = 0.04
float_penalty_rate = 0.03
num_repay_count = 24
float_nominal_principal = 1200.0
float_save_rate = 0.0

# 计算提前还款是否划算的工具

try: 
    while (True):
        str_repay_count = input("请输入分期期数，每月1期，接受1~60期，默认24：")
        if int(str_repay_count) < 1 or int(str_repay_count) > 60 :
            print ("超过范围！")
        else :
            num_repay_count = int(str_repay_count)
            break
except:
    num_repay_count = 24
    print ("输入不是有效值，因此范围设置为默认24")

try: 
    while (True):
        str_orginal_nominal_rate_total = input("请输入名义总手续费率，接受0到0.5，0.01表示1%，默认0.04：")
        if float(str_orginal_nominal_rate_total) < 0.0 or float(str_orginal_nominal_rate_total) > 0.5:
            print ("超过范围！")
        else:
            float_orginal_nominal_rate_total = float(str_orginal_nominal_rate_total)
            break
except:
    float_orginal_nominal_rate_total = 0.04
    print ("输入不是有效值，因此范围设置为默认0.04")


try: 
    while (True):
        str_penalty_rate = input("请输入提前还款违约金率（针对未还本金的违约金比例），接受0到0.1，0.01表示1%，默认0.03：")
        if float(str_penalty_rate) < 0.0 or float(str_penalty_rate) > 0.1:
            print ("超过范围！")
        else:
            float_penalty_rate = float(str_penalty_rate)
            break
except:
    float_penalty_rate = 0.03
    print ("输入不是有效值，因此范围设置为默认0.03")

print("提前还款后，实际还款利率和提前还款相当于理财利率的情况如下：0.0100代表年化利率1.00%，1.0000则代表年化利率100.00%\n")
for i in range(1, num_repay_count):
    # 初始化已发生的现金流
    arr_actual_float_cash_flow = [-float_nominal_principal]
    for ap in range (0, num_repay_count - i):
        # 已经还款的每期金额
        arr_actual_float_cash_flow.append(float_nominal_principal / num_repay_count * (1.0 + float_orginal_nominal_rate_total))
    # 末期还款含违约金
    arr_actual_float_cash_flow.append(float_nominal_principal / num_repay_count * i * (1.0 + float_penalty_rate))
    float_actual_rate = (numpy_financial.irr(arr_actual_float_cash_flow) + 1) ** 12 - 1
    # 初始化虚拟现金流为提前偿还金额
    arr_simulate_float_cash_flow = [-float_nominal_principal / num_repay_count * i * (1.0 + float_penalty_rate)]
    for p in range(0, i):
        # 每期节省还款金额
        arr_simulate_float_cash_flow.append(float_nominal_principal / num_repay_count * (1.0 + float_orginal_nominal_rate_total))
    # 计算提前还款IRR
    float_save_rate = (numpy_financial.irr(arr_simulate_float_cash_flow) + 1) ** 12 - 1
    
    print("当提前%d期还款时" % i + "实际还款利率是%0.4f" % float_actual_rate + "，提前还款相当于年化利率%0.4f 的理财。" % float_save_rate)
print("提前还款折算利率显示完毕。再次提示：0.0100代表年化利率1.00%，1.0000则代表年化利率100.00%\n")