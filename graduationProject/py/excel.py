def extract_excel(file_name):
    import pandas as pd
    import math

    work_list = pd.read_excel(file_name, sheet_name='work_list')
    machine_available = pd.read_excel(file_name, sheet_name='machine_available')
    item_work_time = pd.read_excel(file_name, sheet_name='item_work_time')
    resetting_time = pd.read_excel(file_name, sheet_name='resetting_time')

    available = machine_available.as_matrix()  # 작업별 가능한 기계
    work_todo = work_list.as_matrix()  # 주문목록
    work_time = item_work_time.as_matrix()  # 작업별 소요시간
    rest_time = resetting_time.as_matrix()  # 공정간 쉬는 시간

    index = str(resetting_time.to_dict('split')).split(']')[0].replace("'", '').replace("{index: [", '')
    indexs = index.split(', ')

    available_array = [[] for _ in range(len(machine_available))]  # 이중배열 선언 0 index 가 기계번호 그 뒤로는 모두 가용 품목
    len_available = 0
    for i, t in enumerate(available):
        if type(t[0]) != int:
            break
        len_available += 1
        for j in t:
            if type(j) == float:    # 빈공간을 nan 으로 읽는 것을 방지 작업과 정수를 match 시키기 위해 nan 을 빼야 함
                if math.isnan(j):
                    continue
            available_array[i].append(j)

    # 품목명, 소요시간, 가능한 기계, 주문시간(일자), due_date, 우선순위, 주문번호
    all_work_tuple = [[] for _ in range(len(work_list))]
    # 소요시간, 가능한 기계, due_date, 우선순위, 주문번호
    work_tuple = [[] for _ in range(len(work_list))]

    for i, tuples in enumerate(work_todo):
        time = 0
        available_machine = []
        for j in work_time:
            if tuples[0] == j[0]:
                time = int(j[1])
        for k in available_array:
            if tuples[0] in k:
                available_machine.append(k[0])
        all_work_tuple[i] = (tuples[0], time, available_machine, tuples[1], tuples[2], tuples[3], tuples[4])
        work_tuple[i] = (time, available_machine, tuples[2], tuples[3], tuples[4], 0, tuples[0])
    # print(work_tuple)

    return all_work_tuple, work_tuple, rest_time, len_available, indexs