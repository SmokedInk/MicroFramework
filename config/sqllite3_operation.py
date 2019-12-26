# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   sqllite3_operation
# @Time:    2019-05-09 21:15:57

import os
import sqlite3

from config.settings import BASE_DIR


def get_db_cur():
    """
    创建sqllite3对象及游标
    :return: sqllite3对象及游标
    """
    db_path = os.path.join(BASE_DIR+'\config', "IPProxy.db")
    conn = sqlite3.connect(db_path, timeout=30.0)
    cur = conn.cursor()
    return conn, cur


def create_many(ip_list):
    """
    批量写入
    :param ip_list: 代理IP列表
    :return: None
    """
    conn, cur = get_db_cur()
    sql_insert = "INSERT INTO proxy VALUES(?,?,?,?,?)"
    insert_success = 0
    for ip in ip_list:
        try:
            cur.execute(sql_insert, ip)
            insert_success += 1
        except sqlite3.Error as err:
            conn.rollback()
        continue
    conn.commit()
    print("新增成功 {} 条".format(insert_success))
    close(cur, conn)


def find_query():
    """
    查询数据，每次10条
    :return: 代理IP列表
    """
    conn, cur = get_db_cur()
    cur.execute('SELECT * FROM proxy where effectiveness="连接正常" LIMIT 10')
    ip_list = []
    for eachOne in cur.fetchall():
        ip_list.append(eachOne[0])
    close(cur, conn)
    return ip_list


def select_total():
    """
    查询所有正常连接的代理IP
    :return: 代理IP列表
    """
    conn, cur = get_db_cur()
    cur.execute('SELECT * FROM proxy where effectiveness="连接正常"')
    ip_list = []
    for eachOne in cur.fetchall():
        ip_list.append((eachOne[0], eachOne[2], eachOne[3]))
    close(cur, conn)
    return ip_list


def select_count():
    """
    查询可用代理IP的总数量
    :return: 可用代理IP的总量
    """
    conn, cur = get_db_cur()
    cur.execute('SELECT count(*) FROM proxy where effectiveness="连接正常"')
    count = cur.fetchone()[0]
    close(cur, conn)
    return count


def update_many(ip_desc_dict):
    """
    批量更新
    :param ip_desc_dict: 代理IP列表字典
    :return:
    """
    conn, cur = get_db_cur()
    sql_up_01 = 'UPDATE proxy SET effectiveness = "无法连接", update_time = ? WHERE host = ?'
    sql_up_02 = 'UPDATE proxy SET update_time = ? WHERE host = ?'
    try:
        up_count = 0
        for k, v in ip_desc_dict.items():
            if k == "normal_ip_list":
                p = cur.executemany(sql_up_02, v)
                up_count += p.rowcount
            elif k == "failure_ip_list":
                p = cur.executemany(sql_up_01, v)
                up_count += p.rowcount
        conn.commit()
        print("更新成功 {} 条".format(up_count))
    except Exception as err:
        conn.rollback()
        print(err)
    finally:
        close(cur, conn)


def delete_many():
    """
    删除状态为无法连接的代理IP
    :return:
    """
    conn, cur = get_db_cur()
    sql_de = "delete from proxy where effectiveness='无法连接'"
    try:
        p = cur.execute(sql_de)
        del_count = p.rowcount
        conn.commit()
        print("成功删除 {} 条".format(del_count))
    except sqlite3.OperationalError as err:
        conn.rollback()
        print("删除失败", err)
    finally:
        close(cur, conn)


def close(cur, conn):
    """
    关闭sqllite3游标及对象
    :param cur: 游标对象
    :param conn: 数据库对象
    :return: None
    """
    cur.close()
    conn.close()


if __name__ == '__main__':
    # count = select_count()
    # print(count)
    delete_many()
