import time
import win32com.client
import pandas as pd

class Creon:
    def __init__(self):
        self.obj_CpCodeMgr  = win32com.client.Dispatch('CpUtil.CpCodeMgr')
        self.obj_CpCybos    = win32com.client.Dispatch('CpUtil.CpCybos')
        self.obj_StockChart = win32com.client.Dispatch('CpSysDib.StockChart')
        
    def requestChartData(self, code, date_from, date_to):
#         b_connect = self.obj_CpCybos.IsConnect

        if self.obj_CpCybos.IsConnect == 1: 
           print("연결 정상") 
        else: 
           print("연결 실패")
           return None
           
        list_field_key = [0, 1, 2, 3, 4, 5, 8]
        list_field_name  = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']
        dict_chart = {name:[] for name in list_field_name}
        
        self.obj_StockChart.setInputValue(0, 'A'+code)
        self.obj_StockChart.setInputValue(1, ord('1')) # 0:개수, 1:기간
        self.obj_StockChart.setInputValue(2, date_to)   # 종료일
        self.obj_StockChart.setInputValue(3, date_from) # 시작일
        self.obj_StockChart.setInputValue(5, list_field_key) # 필드
        self.obj_StockChart.setInputValue(6, ord('D')) # 'D', 'W', 'M', 'm', 'T'
        self.obj_StockChart.BlockRequest()
        
        status  = self.obj_StockChart.GetDibStatus()
        msg = self.obj_StockChart.GetDibMsg1()
        print("통신상태:{} {}".format(status, msg))
        
        if status != 0:
            return None
        
        cnt = self.obj_StockChart.GetHeaderValue(3) # 수신개수
        for i in range(cnt):
            dict_item = (
                {name: self.obj_StockChart.GetDataValue(pos, i)
                 for pos, name in zip(range(len(list_field_name)), list_field_name)}
            )
            
            for k, v in dict_item.items():
                dict_chart[k].append(v)
            
        print("차트: {} {}".format(cnt, dict_chart))
        
        return pd.DataFrame(dict_chart, columns=list_field_name)
            


if __name__ == '__main__':
    creon = Creon()
    print(creon.requestChartData('035420', 20150101, 20171201))
    

