
# -*- coding:utf-8 -*-
"""
  スプレッドシートを扱う
  json sheet key fileとシートキーが必要


"""
import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import pysnooper


import os
from dotenv import load_dotenv
import logging

lg = logging.getLogger(__name__)

# 環境変数を参照
load_dotenv()
SHEET_JSON_FILE = os.getenv('SHEET_JSON_FILE')
SHEET_KEY = os.getenv('SHEET_KEY')
SHEET_NAME = os.getenv('SHEET_NAME')





#スプレッドシートからデータ取得用
#@pysnooper.snoop()
def get_sheet_with_pd(sheetname=SHEET_NAME):
    """
    df = get_as_dataframe(worksheet, skiprows=0, header=0)を使うと
    要素のtypeがnumpyになるのでget_all_recordsで取得してからDFに変換
    """
    try:
        gc = gspread.service_account(SHEET_JSON_FILE)
        sh = gc.open_by_key(SHEET_KEY)
        worksheet = sh.worksheet(sheetname)
        list_of_dict = worksheet.get_all_records()
        df = pd.DataFrame(list_of_dict)
        return df
    except Exception as e:
        lg.exception(e)

#@pysnooper.snoop()
def set_sheet_with_pd(sheetname, df):
    lg.debug(sheetname)
    try:
        gc = gspread.service_account(SHEET_JSON_FILE)
        sh = gc.open_by_key(SHEET_KEY)
        worksheet = sh.worksheet(sheetname)
        set_with_dataframe(worksheet, df)
        print("set df ok")
    except Exception as e:
        lg.exception(e)
    

#スプレッドシートからデータ取得用
#@pysnooper.snoop()
def get_sheet_values_of_list(sheetname):
    """
    シートからデータをリストのリストとして取得
    """
    try:
        gc = gspread.service_account(SHEET_JSON_FILE)
        sh = gc.open_by_key(SHEET_KEY)
        worksheet = sh.worksheet(sheetname)
        list_of_lists = worksheet.get_all_values()
        return list_of_lists
    except Exception as e:
        lg.exception(e)


#@pysnooper.snoop()
def sheet_all_clear(sheetname):
    """
    シートからデータをリストのリストとして取得
    """
    try:
        gc = gspread.service_account(SHEET_JSON_FILE)
        sh = gc.open_by_key(SHEET_KEY)
        worksheet = sh.worksheet(sheetname)
        worksheet.clear()
    except Exception as e:
        lg.exception(e)



# シート名、キャラ名,行の名前、書きこむ値が引数
#@pysnooper.snoop()
def writeSheet(sheetname, col_name, row_name, input_val):
    gc = gspread.service_account(SHEET_JSON_FILE)
    sh = gc.open_by_key(SHEET_KEY)
    worksheet = sh.worksheet(sheetname)
    # 最初の列と列を読み込む
    row_num = worksheet.row_values(1)
    col_num = worksheet.col_values(1)
    # 読み込んだ最初の列の列番号のインデックス
    mycol = col_num.index(col_name) + 1
    myrow = row_num.index(row_name) + 1
    # 指定した行を出す
    worksheet.update_cell(mycol, myrow, input_val)

#@pysnooper.snoop()
def sheet_add_row(sheetname, row_vals):
    #row_vals = list or dict
    #ワークシート選択
    gc = gspread.service_account(SHEET_JSON_FILE)
    sh = gc.open_by_key(SHEET_KEY)
    worksheet = sh.worksheet(sheetname)
    #書き込み.リストのリストだったら
    if isinstance(row_vals[0], list):
        worksheet.append_rows(row_vals)
    #単体のリストなら
    else:
        worksheet.append_row(row_vals)
    lg.debug('append row: {}'.format(row_vals))




