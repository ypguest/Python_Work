import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from pandas import Series

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


filepath = r"Z:\QRE\00_Production_Public\Donghu\Donghu-SEDSOC\17 Quality_control\02_WAT\Donghu_SEDS1_3DIC_WAT_Tracking_Table1.xlsm"
# 读取第二张表参数的名称
Names = pd.read_excel(filepath, sheet_name="spec", usecols=[2], names=['Item Name'])

LotId = pd.read_excel(filepath, sheet_name="3D_raw", usecols=[2], names=['XMC_Lot_Wafer'])

# 将dataframe转换为list，不改动原有df，故需要重新存储这个list
LotIdList = LotId['XMC_Lot_Wafer'].tolist()

# 现在导入第一张表
itemstr = """IBRI_BALTM_2_2	 IBRI_LHB_S3U_630	KRC_LHB_S3U_1	RC_LHB_S3U_630	RC_LHB_T3U_315	RS_BALTM_2_2	VBD_BALTM_2_2	VBD_LHB_S3U_630	IDOF_HN12_10_D06_D4
IDOF_HP12_10_D06_D4	IDOF_LN12_10_D06_D4	IDOF_LP12_10_D06_D4	IDOF_N25_10_D28	IDOF_P25_10_D28	IDOF_RN12_10_D06_D4	IDOF_RP12_10_D06_D4	IDS_HN12_10_D06_D4
IDS_HP12_10_D06_D4	IDS_LN12_10_D06_D4	IDS_LP12_10_D06_D4	IDS_N25_10_D28	IDS_P25_10_D28	IDS_RN12_10_D06_D4	IDS_RP12_10_D06_D4	RS_NDFSAB_1D8_50
RS_NWSTI_1D8_50	RS_PPSAB_1D8_50	RS_PWSTI_1D8_50	VTL_HN12_10_10	VTL_HN12_10_D06_D4	VTL_HP12_10_10	VTL_HP12_10_D06_D4	VTL_LN12_10_10	VTL_LN12_10_D06_D4
VTL_LP12_10_10	VTL_LP12_10_D06_D4	VTL_N25_10_10	VTL_N25_10_D28	VTL_P25_10_10	VTL_P25_10_D28	VTL_RN12_10_10	VTL_RN12_10_D06_D4	VTL_RP12_10_10
VTL_RP12_10_D06_D4	CB_MAX	CS16K	CW_MAX	ION24060_O	ION49100_O	IONH49100_I	IONL24080_O	IONL24SA108_I	IONL49115_O	IONL_W_C	IONL_W_G	IONR_W_C
IOP24060_O	IOP49100_O	IOPL24SA100_I	IOPL24SA108_I	IOPSV570	N24_Toxe	P24_Toxe	P49_Toxe	RC_1C_N065	RC_1C_N120	RC_1C_P065	RC_1C_P120
RC_1TH_080	RC_2TH	RC_NG_N065	RC_WL	RS_1AL	RS_2AL	RS_DNW	RS_N24	RS_NMRS	RS_NW	RS_P24	RS_PL	RS_PW	RS_W	R_BL_1	R_WL_1	VTL_W_C	VTL_W_G
VTN24060_O	VTN49100_O	VTNH49100_I	VTNL24080_O	VTNL24SA108_I	VTNL49115_O	VTP24060_O	VTP49100_O	VTPL24SA100_I	VTPL24SA108_I	VTPSV570_O	VTR_W_C	VTSAN1	VTSAP1"""

# print(type(str.split()))
# print(str.split())

# NameList是第一张表的参数名称
NameList = itemstr.split()
df1 = pd.read_excel(filepath, sheet_name="3D_raw", usecols=list(range(4, 104)), names=NameList)

# print(df1) 第一张表的数据导入成功
# 导入第二张表的上下spec值

SpecData = pd.read_excel(filepath, sheet_name="spec", usecols=[3, 4, 5], names=['Spec High', 'Spec Low', 'Spec Target'])


# 对表二操作，现将参数名和各个spec值对应起来
SpecList = Names.join(SpecData)
# print(SpecList)
# print(df1)
# print(type(SpecList))
# print(type(SpecList['name']))
# SpecListName=list[SpecList['name']]
# SpecList1=SpecList(index=SpecList['name'])
# print(SpecList1)

SpecList.set_index(["Item Name"], inplace=True)
SPstack = SpecList.stack()
# print(SP)
SpecList = SPstack.to_frame()

# print(SpecList)
# print(df1)
# df1.set_index(["name"], inplace=True)
# #
# SpecFinal = df1.join(SpecList)
# #对数据进行处理，na值全取0
# # df1.fillna(value=0,inplace=True)
# # SpecList.fillna(value=0,inplace=True)
# # #规定数据格式
df3 = pd.DataFrame(df1, dtype=np.float)
SpecList1 = pd.DataFrame(SpecList, dtype=np.float)
# # # # #
# SpecFinal = df3.join(SpecList)

count = 0
for name in NameList:
     # 从第一张表中画折线图
     aaa = plt.figure(figsize=(10, 4))
     xzb = list(range(14))
     plt.plot(xzb, df1[name], 'ko-')
     plt.title(name)
     #从第二张表中画spec
     a= name in SpecList1.index
     count=count+1

     plt.xticks(xzb, LotIdList, color='k', rotation=90)
     if a == True :
         A = SpecList1.loc[name].loc['Spec High']
         A1 = SpecList1.loc[name].loc['Spec High'].values
         B = SpecList1.loc[name].loc['Spec Low']
         B1 = SpecList1.loc[name].loc['Spec Low'].values
         C = SpecList1.loc[name].loc['Spec Target']
         C1 = SpecList1.loc[name].loc['Spec Target'].values
         plt.axhline(y=A1, color='r', linestyle='--')
         plt.axhline(y=B1, color='b', linestyle='--')
         plt.axhline(y=C1, color='r', linestyle='--')
         # ticks = aaa.set_xticks(list(range(16)))
         # labels=aaa.set_xlabels(['PPB113#03','PPB113#04','PPB113#05','PPB113#06','PPB113#07','PPB113#08','PPB020#08','PPB020#09',\
         #  'PPB020#10','PPB020#11','PPB020#12','PPB020#13','PPB020#15','PPB020#16','PPB020#17','PPB020#19'])
         # 储存当前图表
         plt.figure(figsize=(1, 1)) ###这一行可以改表格的比例！！
         # plt.show()
     aaa.savefig(r'Z:\QRE\00_Production_Public\Donghu\Donghu-SEDSOC\17 Quality_control\02_WAT\data\spc[%d].png' % count, bbox_inches='tight')
