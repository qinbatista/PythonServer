"""
    需要使用到的模块:
    xlrd,xlwt,xlutils 写入数据库
    os 建立新文件
    re 表头匹配创建
    pymysql 操作数据库
    DBUtils 数据库连接池
"""
import os
import re
import xlrd
from xlwt import Workbook
from xlutils.copy import copy
import pymysql
from DBUtils.PooledDB import PooledDB

# 配置数据连接信息
__config = {
    "host": "192.168.1.102",
    "port": 3306,
    "user": "root",
    "password": "lukseun",
    "database": "staff"
}

# 建立数据库连接池
POOL = PooledDB(
    pymysql, 5,  # 5为连接池里的最少连接数
    **__config,
    setsession=['SET AUTOCOMMIT = 1']  # 设置线程池是否打开自动更新的配置，0为False，1为True
)

# 准备Excel信息
workbook = Workbook()  # 新建一个工作簿
book_name = '打卡记录表.xls'


def get_data():
    """
    获取数据库信息，以字典的形式返回
    每一条数据是字典，所有数据是一个列表嵌套字典
    :return: 两个list，存放表头，存放表单信息
    """
    db = POOL.connection()
    # DictCursor,以字典形式返回数据
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = """
        SELECT t.data_time as "日期",u.user_name as "姓名",
               t.check_in as "上班打卡",t.check_out as "下班打卡",
               TIMEDIFF(t.check_out,t.check_in) as "上班时长"
        FROM userinfo u JOIN timeinfo t 
        ON u.unique_id = t.unique_id  
        WHERE u.user_name != ""
        ORDER BY t.data_time
    """
    cursor.execute(sql)
    temp = cursor.fetchall()
    # print(temp)

    # 遍历内部字典取出所有key存储为表头信息
    header = []
    for k in temp[0]:
        header.append(k)

    # 列表嵌套列表形式存储所有数据
    all_data = []
    # 遍历列表temp，取出所有value作为表格内容
    for i in temp:
        i['上班时长'] = str(i['上班时长'])  # 必须把时间类型替换转换成字符串
        all_data.append(list(i.values()))  # i.values() 取字典里的v
    return header, all_data


def create_xls(path, sheet_name, value):
    """
    创建Excel表
    系统中没有的时候新建表并新建第一张sheet，往表格中写入表头
    存在的时候，添加新的表格，并写入表头
    :param path:  表文件名称
    :param sheet_name:  表格名称
    :param value: 表头信息
    """
    index = len(value)  # 获取一行需要写入数据的个数

    # 如果Excel表不存在 则新创建并添加表头
    if not os.path.exists(path):
        os.system(r"touch {}".format(path))  # 调用系统命令行来创建文件
        sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建第一个表格
        # 往表格中写入表头数据（对应的行和列）
        for i in range(0, index):
            sheet.write(0, i, value[i])
        workbook.save(path)  # 保存Excel工作簿
        # print("==========   {}   表格创建成功!==========".format(sheet_name))

    else:
        rb = xlrd.open_workbook(path, formatting_info=True)  # 读取表格
        wb = copy(rb)  # 对原文件进行复制，保存成新的文件

        # 获取workbook中所有的表格
        sheets = rb.sheet_names()
        if sheet_name not in sheets:
            new_sheet = wb.add_sheet(sheet_name)  # 在工作簿中新添加一个表格
            # 向表格中写入表头数据（对应的行和列）
            for i in range(0, index):
                new_sheet.write(0, i, value[i])
            wb.save(path)  # 保存工作簿
            # print("==========   {}   表格添加成功!==========".format(sheet_name))


def write_xls_append(path, value, sheet_name):
    """
    以数据追加的方式逐条写入Excel表
    :param path:  要写入的表文件名
    :param value: list 待写入的数据
    :param sheet_name: 表格名称
    :return:
    """
    index = len(value)  # 获取一行要写入数据的个数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    i = sheets.index(sheet_name)  # 获取表格在Excel中序列位置
    worksheet = workbook.sheet_by_name(sheets[i])  # 按索引取到表格

    rows_old = worksheet.nrows  # 获取表格中已存在数据的行数
    # 得到表格中存在的所有的日期 包括空串
    all_date = []
    for n in range(1, rows_old):
        cell = worksheet.cell_value(n, 0)  # 取第一列数据
        if cell not in all_date:
            all_date.append(cell)
    # print("现在表中第一列已经有的日期：{}".format(all_date))

    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(i)  # 获取转化后工作簿中的第一个表格

    """
        用行数进行
        行数=1, 说明只有表头，把第一组数据写入第二行
        行数>1, 用all_date判断
            如果value[0]不在列表里，空一行从rows+1写入
            存在列表里，接着写
    """
    if rows_old <= 1:
        for x in range(0, index):
            new_worksheet.write(rows_old, x, value[x])
    else:
        if value[0] in all_date:
            for x in range(0, index):
                new_worksheet.write(rows_old, x, value[x])
        else:
            for x in range(0, index):
                new_worksheet.write(rows_old + 1, x, value[x])

    # 保存工作簿
    new_workbook.save(path)
    # print("{}:{}    打卡信息写入Excel成功！！！".format(value[1], value[0]))


if __name__ == '__main__':
    # 获取表头和表单数据
    if os.path.exists(book_name):
        os.remove(book_name)
    (title, data) = get_data()
    print("生成中....")
    # 遍历data中所有列表的日期，通过正则表达式获取年月作为sheet
    for i in data:
        for j in i:
            date_list = re.findall('\d{4}-\d{2}', i[0])  # findall返回列表
            # 每一个date_list是只包含一个日期信息的列表
            # print("-----    {}  -----".format(date_list[0]))
            # 此时的i是每一条源数据
            # 通过sheetname[0]取到要传入的表格名
            sheet_name = date_list
            create_xls(book_name, sheet_name[0], title)
            write_xls_append(book_name, i, sheet_name[0])
            # 每写完一条数据必须跳出该for循环，开始写下一条
            break
    print("生成完毕:"+book_name)
