# !/usr/bin/python
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import re

# pd设置
pd.set_option('display.max_columns', None)   # 显示不省略行
pd.set_option('display.max_rows', None)      # 显示不省略列
pd.set_option('display.width', None)         # 显示不换行


def cover_html_file(_url_path, _data_path):
    with open(_url_path, "r", encoding="utf-8") as file:
        content = file.read()          # 读取文件
        soup = BeautifulSoup(content, "lxml")
        # 修改1：CSS路径
        producer_link = soup.html.head.link
        producer_link['href'] = r'config\styles.css'    # 修改CSS文件路
        # 修改2：标题
        producer_h1 = soup.html.body.find_all(name='h1')
        producer_h1[0].string = 'By Lot Summary'
        producer_h1[1].string = 'Detail Wafer Map Gallery'
        # 将原有的汇总表删除
        producer_ul = soup.html.body.find(name='ul')
        producer_ul.decompose()
        producer_ol = soup.html.body.find(name='ol')
        producer_ol.decompose()
        # 添加新表的CSS设置至HTML文件
        table_config = BeautifulSoup("""
        <div style = "display:bolck;padding-top:20px">  
        <style type="text/css">
          table.tftable {font-size:12px; color:#333333; width:100%; border-width:1px; border-color:#729ea5; border-collapse:collapse; }
          table.tftable th {font-size:12px;background-color:#acc8cc;border-width: 1px;padding: 8px;border-style: solid;border-color: #729ea5; text-align:left;}
          table.tftable tr {background-color:#d4e3e5;}
          table.tftable td {font-size:12px;border-width: 1px;padding: 8px;border-style: solid;border-color: #729ea5;}
        </style>
        <!-- Row Highlight Javascript -->
        <script type="text/javascript">
            window.onload=function(){
            var tfrow = document.getElementById('tftable').rows.length;
            var tbRow=[];
            for (var i=1;i<tfrow;i++) {
                tbRow[i]=document.getElementById('tftable').rows[i];
                tbRow[i].onmouseover = function(){
                  this.style.backgroundColor = '#ffffff';
                };
                tbRow[i].onmouseout = function() {
                  this.style.backgroundColor = '#d4e3e5';
                };
                }
            };
        </script>
         """, "lxml").body.contents[0]
        producer_h1[0].insert_after(table_config)

        lot_infor = pd.DataFrame(columns=['Source Lot', 'Stage', 'Link'])
        compiler = re.compile(r".*Wafer Map Gallery \(Source Lot = ([A-Za-z0-9]{6}\.S).* Stage = ([A-Za-z0-9]{3})\)", re.S | re.I)
        row = 0
        # 获取lot + stage + index的顺序
        for child in soup.html.body.find_all('h2'):
            re_lot = re.search(compiler, child.get_text())
            lot_infor.loc[row, 'Source Lot'] = re_lot.group(1)
            lot_infor.loc[row, 'Stage'] = re_lot.group(2)
            lot_infor.loc[row, 'Link'] = """<a href="#page_bookmark{}">Page {}</a>""".format(row+1, row+1)
            row = row + 1
        # 添加新表
        table_html = gentable(_data_path, lot_infor).body.contents[0]
        producer_script = soup.html.body.script
        producer_script.insert_after(table_html)

    with open(_url_path, 'w') as fp:   # 将改变后的HTML写入文件
        fp.write(soup.prettify())  # prettify()的作用是将sp美化一下，有可读性


def gentable(_data_path, _lot_infor):

    _data = pd.read_excel(io=_data_path)

    for i in range(1, _data.shape[1]):
        _data.iloc[:, i:i+1] = round(_data.iloc[:, i:i+1], 2)  # 将yield转换为小数点两位
    _data = pd.merge(_lot_infor, _data, how='left', on=['Source Lot', 'Stage'])
    _order = ['Source Lot', 'Product', 'Program', 'Stage', 'Wcnt', 'Yield', 'Link']
    _data = _data[_order]
    _data_html = _data.to_html(index_names=True, escape=False)
    _soup = BeautifulSoup(_data_html, "lxml")
    _soup.table['id'] = "tftable"  # 修改属性
    _soup.table['class'] = "tftable"  # 修改属性
    _soup.table['frame'] = "hsides"  # 修改属性
    _soup.table['align'] = "center"  # 修改属性
    return _soup


if __name__ == '__main__':
    url_path = r"//arctis/qcxpub/QRE/04_QA(Component)/99_Daily_Report/99_QRE_CP_Yield_Report/CP_Map_Report/7.13Daily_Report_Map_Gallery.html"
    data_path = r"//arctis/qcxpub/QRE/04_QA(Component)/99_Daily_Report/99_QRE_CP_Yield_Report/CP_Map_Report/7.13_LOT LIST.xlsx"
    cover_html_file(url_path, data_path)
