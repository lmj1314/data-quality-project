from check_data import orders, users

def clean_data(orders,users):
    # 1. 修复空值：把 user_id 为空的订单，暂时填充为 0（或者直接删掉）
    # 这里演示填充为 0
    orders_cleaned = orders.copy()# 复制一份，避免改坏原数据
    orders_cleaned['data_status'] = '正常'

    orders_cleaned.loc[orders_cleaned['user_id'].isnull(),'data_status'] = '异常,用户id缺失'
    orders_cleaned['user_id'] = orders_cleaned['user_id'].fillna(-1) #fillna 遇到 NaN 就替换成你给的 -1。


    # 2. 修复负数：把金额小于 0 的，取绝对值（假设原本是操作失误）
    orders_cleaned['amount'] = orders_cleaned['amount'].abs()

    # 3. 删除重复项：保留第一条重复的数据
    orders_cleaned = orders_cleaned.drop_duplicates(subset=['order_id'], keep='first')

    #4.不合法的数据，标记异常
    valid_userid= users['user_id'].astype(float).tolist()
    orphan_cond = (~orders_cleaned['user_id'].isin(valid_userid)) & (orders_cleaned['user_id']!= -1)  #孤儿条件
    print("孤儿条件的订单：", orders_cleaned[orphan_cond])
    orders_cleaned.loc[orphan_cond,'data_status'] = '异常,用户id不存在'
    orders_cleaned.loc[orphan_cond,'user_id'] = -1


    return orders_cleaned

if __name__ == '__main__':
    final_data = clean_data(orders,users)
    print("--- 最终清洗结果 ---")
    print(final_data)
    #存成excel
    final_data.to_excel('./data-quality-day2/最终清理结果.xlsx', index=False)
