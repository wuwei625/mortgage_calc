import os
import sys
import re
import time
import math
import numpy_financial


print ("分期付款计算器 by Rufev\n")
arr_str_yes = ["Y", "y", "Yes", "yes"]

float_original_amount = 10000.0 # 本金
num_repay_count = 24 # 还款期数
bool_real_rate = False # 实际年利率模式
float_mortgage_real_rate = 0.06 # 实际年利率
float_mortgage_nominal_fee_rate = 0.0025 # 每期手续费率
float_money_rate = 0.015 # 存款利率
float_deposit = 0.0 # 假设不还款，去存款，存款的余额
float_deposit_total_interest = 0.0 # 假设不还款，去存款，累计的利息
float_each_payment = 0.0
arr_float_cash_flow = [] # 现金流表

# 输入条件

try: 
    while (True):
        str_original_amount = input("请输入本金，接受100到1000000，默认10000")
        if float(str_original_amount) < 100.0 or float(str_original_amount) > 1000000.0:
            print ("超过范围！")
        else:
            float_original_amount = float(str_original_amount)
            break
except:
    float_original_amount = 10000.0
    print ("输入不是有效值，因此范围设置为默认10000")


try: 
    while (True):
        str_repay_count = input("请输入分期期数，每月1期，接受1~60期，默认24")
        if int(str_repay_count) < 1 or int(str_repay_count) > 60 :
            print ("超过范围！")
        else :
            num_repay_count = int(str_repay_count)
            break
except:
    num_repay_count = 24
    print ("输入不是有效值，因此范围设置为默认24")

str_rate_type = input("你要用实际年利率，还是名义每期手续费率？Y、y、Yes、yes表示实际利率")
bool_real_rate =  str_rate_type in arr_str_yes

if bool_real_rate:
    try: 
        while (True):
            str_mortgage_real_rate = input("请输入实际利率，接受0到0.48，0.01表示1%，默认0.06")
            if float(str_mortgage_real_rate) < 0.0 or float(str_mortgage_real_rate) > 0.48:
                print ("超过范围！")
            else:
                float_mortgage_real_rate = float(str_mortgage_real_rate)
                break
    except:
        float_mortgage_real_rate = 0.06
        print ("输入不是有效值，因此范围设置为默认0.06")
else:
    try: 
        while (True):
            str_mortgage_nominal_fee = input("请输入名义每期手续费率，接受0到0.02，0.01表示1%，默认0.0025")
            if float(str_mortgage_nominal_fee) < 0.0 or float(str_mortgage_nominal_fee) > 0.01:
                print ("超过范围！")
            else:
                float_mortgage_nominal_fee_rate = float(str_mortgage_nominal_fee)
                break
    except:
        float_mortgage_nominal_fee_rate = 0.0025
        print ("输入不是有效值，因此范围设置为默认0.0025")

try: 
    while (True):
        str_money_rate = input("请输入预期低风险准活期投资利率，如余额宝等产品，接受0到0.05，0.01表示年利率1%，默认0.015")
        if float(str_money_rate) < 0.0 or float(str_money_rate) > 0.05:
            print ("超过范围！")
        else:
            float_money_rate = float(str_money_rate)
            break
except:
    float_money_rate = 0.015
    print ("输入不是有效值，因此范围设置为默认0.015")

# 计算还款额
if bool_real_rate:
    # 实际利率法
    float_each_payment = numpy_financial.pmt(float_mortgage_real_rate / 12.0, num_repay_count, -float_original_amount)
else:
    # 手续费模式
    float_each_payment = float_original_amount / num_repay_count + float_original_amount * float_mortgage_nominal_fee_rate

print ("共还款" + str(num_repay_count) + "期，月供是%0.2f" % float_each_payment)

float_deposit = float_original_amount # 假设本金存入活期

arr_float_cash_flow.append(-float_original_amount) # 首期现金流是负本金
for i in range(0, num_repay_count):
    arr_float_cash_flow.append(float_each_payment) # 每期现金流
    # 每期还款日的时候，如果存款有结余，先结算活期利息
    if (float_deposit > 0.0):
        float_interest = float_deposit * (float_money_rate / 12.0) # 当期利息
        float_deposit_total_interest += float_interest # 计算累积了多少利息
    float_deposit -= float_each_payment # 从存款余额中扣除当期还款额

if not bool_real_rate:
    # 计算真实利率
    float_mortgage_real_rate = (numpy_financial.irr(arr_float_cash_flow) + 1) ** 12 - 1
    print ("分期付款的实际利率是%0.4f。\n" % float_mortgage_real_rate)
    
print ("如果用分期还款，则在手的现金会产生利息%0.2f元。\n" % float_deposit_total_interest)
if (float_deposit < 0.0):
    print ("但是存款不够用，到最后反而亏了至少%0.2f元" % -float_deposit)
else :
    print ("最后居然还剩%0.2f元。" % float_deposit)

