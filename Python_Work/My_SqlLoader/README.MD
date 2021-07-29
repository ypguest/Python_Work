# 1.主要程序简介
## 1.1 xmcmappingloader.py模块
用于将XMC提供的DailyMapping文件上传至数据库
1. load xmc mapping file;<br/>
2. 如果文件loading成功，则将将文件名写入xmcmappingloader中;<br/>

涉及函数：
@DirFolder;<br/>
@FileRepeatChk;<br/>
@mappingloader;<br/>

输出：
@loader：xmcmappingloader;<br/>
@database：xmc_mapping_table;<br/>

*备注*：当前主要通过production folder下的DailyMapping folder中的数据进行上传，但是发现一部分数据不完善，故加入MAPPING floder下的数据，通过xmcmappingloader_v0.1.py loader对数据进行上传<br/>
<hr/>

## 1.2 xmcwiploader.py



<hr/>

## 1.3 psmcwiploader.py
功能1：用于更新psmc当前Lot状态
1. 读取01_PTC_Wip（psmc）中的wip文件，并更新至psmc_wip_tracing_table和psmc_lot_tracing_table<br/>
2. 如果录入的Lot_Id在数据库psmc_lot_tracing_table已经存在，则将psmc_lot_tracing_table数据库中的该Lot信息调出，根据Current_Time确认是否需要更新;<br/>
   -> 调用RepeatWaferCheck函数，将Wafer No按时间排序，靠前的Wafer No需要删除；
3. 如果文件loading成功，则将将文件名写入psmcwiploader中;<br/>

涉及函数：
@PsmcWipLoader `主函数`
@DataToWafer
@RepeatLotCheck
@DirFolder
@FileRepeatChk
@RepeatWaferCheck
@MysqlUpdate

输出：<br/>
@loader：psmc_wip_tracing_table<br/>
@database：psmcwiploader<br/>
@database：psmc_lot_tracing_table<br/>
@database：psmc_lot_tracing_table<br/>