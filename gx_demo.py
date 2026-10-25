import great_expectations as gx
from check_data import orders


def run_gx():
    print("正在初始化 GX 引擎并建立本地项目目录...")
    # 使用 file 模式，数据会保存在本地 gx_project 文件夹里
    context = gx.get_context(mode="file", project_root_dir="./gx_project")

    # 接入数据
    data_source = context.data_sources.add_pandas("my_pandas_source")
    data_asset = data_source.add_dataframe_asset(name="orders_asset")
    batch_definition = data_asset.add_batch_definition_whole_dataframe("batch_def")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": orders})

    # 规则1：order_id 必须唯一
    print("\n--- 校验 1：订单唯一性 ---")
    res1 = batch.validate(gx.expectations.ExpectColumnValuesToBeUnique(column="order_id"))
    print(f"校验结果：{'✅ 通过' if res1.success else '❌ 失败'} | 未通过的行数：{res1.result.get('unexpected_count')}")

    # 规则2：amount 必须在 0-10000 之间
    print("\n--- 校验 2：金额范围 ---")
    res2 = batch.validate(gx.expectations.ExpectColumnValuesToBeBetween(column="amount", min_value=0, max_value=10000))
    print(f"校验结果：{'✅ 通过' if res2.success else '❌ 失败'} | 未通过的行数：{res2.result.get('unexpected_count')}")

    # 规则3：user_id 必须非空
    print("\n--- 校验 3：用户ID完整性 ---")
    res3 = batch.validate(gx.expectations.ExpectColumnValuesToNotBeNull(column="user_id"))
    print(f"校验结果：{'✅ 通过' if res3.success else '❌ 失败'} | 未通过的行数：{res3.result.get('unexpected_count')}")

    # 生成报告
    print("\n正在生成 HTML 数据质量报告...")
    context.build_data_docs()

    print("\n✅ GX 校验完成！请去你左侧的项目文件夹里，找这个路径：")
    print("👉 gx_project -> gx -> uncommitted -> data_docs -> local_site -> index.html")
    print("右键 index.html，选择在浏览器中打开（或者双击），就能看到红绿报告了！")


if __name__ == "__main__":
    run_gx()