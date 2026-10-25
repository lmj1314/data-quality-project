import pandas as pd

#展示数据
users = pd.read_excel( 'data-quality-day2/users.xlsx')
orders = pd.read_excel( 'data-quality-day2/orders.xlsx')

# print(users)
# print(orders)

# 1. 找金额为负的订单（对应 WHERE amount < 0）
bad_amount = orders[orders['amount'] < 0]
print("金额为负的订单：\n", bad_amount)

# 2. 找 user_id 为空的订单（对应 WHERE user_id IS NULL）
id_null = orders[orders['user_id'].isnull()]
print("user_id为空的订单：\n", id_null['order_id'])

#---------“孤儿记录”-----------
all_user_id = users['user_id'].tolist()
bad_order = orders[~orders['user_id'].isin(all_user_id)]
print("孤儿记录：\n", bad_order)

#------------去重记录------------------
#duplicated 是 Pandas 查重函数，keep=False 的意思是“只要有重复，把所有相关的行都给我标出来”
duplicate_orders  = orders[orders.duplicated(subset=['order_id'],keep=False)]
print("重复记录：\n", duplicate_orders)

#把上面查出来的所有“坏数据”，保存到一个新的 Excel 文件里。
# 创建一个 Excel 写入器，准备写多个 Sheet
with pd.ExcelWriter('data-quality-day2/数据质量校验报告.xlsx') as writer:
    bad_amount.to_excel(writer, sheet_name='金额为负', index=False)
    id_null.to_excel(writer, sheet_name='id为空', index=False)
    bad_order.to_excel(writer, sheet_name='孤儿订单', index=False)
    duplicate_orders.to_excel(writer, sheet_name='重复订单', index=False)

print('所有坏数据已保存到 数据质量校验报告.xlsx 文件')
