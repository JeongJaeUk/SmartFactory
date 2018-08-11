import pandas as pd
import factoryheader

work_list = pd.read_excel('inputdata.xlsx', sheet_name='work_list')
machine_available = pd.read_excel('inputdata.xlsx', sheet_name='machine_available')
item_work_time = pd.read_excel('inputdata.xlsx', sheet_name='item_work_time')
resetting_time = pd.read_excel('inputdata.xlsx', sheet_name='resetting_time')

work_list_matrix = work_list.as_matrix()
machine_available_matrix = machine_available.as_matrix()
item_work_time_matrix = item_work_time.as_matrix()
resetting_time_matrix = resetting_time.as_matrix()

"""
품목을 입력 받았을 때 그 품목의 공정가능한 기계를 배열로 만들어 준다.
availlist = factoryheader.getAvailableList(machine_available_matrix, "B")
print(availlist)
"""

"""
품목을 입력 받았을 때 그 품목의 공정시간을 반환한다.
num = factoryheader.getWorkingTime(item_work_time_matrix, "A")
print(num)
"""

print(work_list_matrix)