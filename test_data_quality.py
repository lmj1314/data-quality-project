import pytest

from check_data import orders, users
from clear_data import  clean_data

@pytest.fixture
def cleaned_data():
    print('正在执行清理数据操作')
    return clean_data(orders, users)

class TestDataQuality:
    def test_num_orders(self,cleaned_data):
         # 1. 前置验证：先证明原数据确实有负数（证明脏数据存在）
        assert (orders['amount'] < 0).any(), "原数据里没有负数，测试失去意义"
        # 3. 核心断言：清洗后的数据，绝对不能有负数
        #  .any()
        #  相当于：“只要有哪怕一个符合，就算你赢。” 常用于找脏数据（比如：只要查出一个负数，我就报错）。
        #  .all()
        #  相当于：“必须全票通过，少一个都不行。” 常用于验证清洗结果（比如：清洗后，所有的金额都必须大于0
        assert  (cleaned_data['amount'] > 0).all(), "清洗失败，有负数"

    def test_null_orders(self,cleaned_data):
        assert (orders['user_id'].isnull()).any(),"原数据没有空值"
        # orders_cleaned = clean_data(orders, users)
        assert (cleaned_data['user_id'].notnull()).all(),'数据清洗失败，有空值'

    def test_duplicate_orders(self,cleaned_data):
        assert orders.duplicated(subset=['order_id']).any(),'没有重复订单'
        # orders_cleaned = clean_data(orders, users)
        assert not cleaned_data.duplicated(subset=['order_id']).any(),'清洗失败，还有重复订单'

    def test_orphan_orders(self,cleaned_data):
        user_allid = users['user_id'].astype(float)
        orphan_orders = ~(orders['user_id'].isin(user_allid)) & (orders['user_id'] != -1)
        assert orphan_orders.any(),"没有孤儿数据"
        # orders_cleaned = clean_data(orders, users)
        orphan_orders_after = ~(cleaned_data['user_id'].isin(user_allid)) & (cleaned_data['user_id'] != -1)
        assert not orphan_orders_after.any(),'清洗失败，仍有孤儿数据'

    @pytest.mark.parametrize("column, condition_desc, expected_valid", [
        ("amount", "金额不能为负", lambda df: (df['amount'] >= 0).all()),
        ("user_id", "用户ID不能为空", lambda df: (df['user_id'].notnull()).all())
    ])
    def test_data_cleanliness_parametrized(self, cleaned_data, column, condition_desc, expected_valid):
        # expected_valid 是一个 lambda 函数，我们直接传入清洗后的表去执行它
        assert expected_valid(cleaned_data), f"清洗失败，{condition_desc}"
