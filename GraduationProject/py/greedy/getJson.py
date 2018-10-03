import json

def getAvailableMachineList(itemname, machine):
    result = []
    for i in range(len(machine)):
        for j in range(len(machine[i])):
            if itemname == machine[i][j]:
                result.append(machine[i][0])
    return result

def extract_json(file_name):
    with open(file_name, encoding="utf-8") as f:
        data = json.load(f)

    workList = data['workList']
    machine_available = data["machineAvailable"]
    item_time = data["itemWorkTime"]
    resetting = data["resettingTime"]

    available = [[] for _ in range(len(machine_available))] # 작업별 가능한 기계
    work_todo = [[] for _ in range(len(workList))] # 주문목록
    work_time = [[] for _ in range(len(item_time))] # 작업별 소요시간
    machine_amount = len(available)
    all_work_list = [[] for _ in range(len(workList))]

    for i in range(len(available)):
        available[i].append(i+1)
        temp_available = []
        for j in range(len(machine_available[i])):
            temp_available.append(machine_available[i][j])
        available[i] = available[i] + temp_available

    for i in range(len(work_todo)):
        work_todo[i].append(workList[i]['품목'])
        work_todo[i].append(workList[i]['주문시간'])
        work_todo[i].append(workList[i]['deadline'])
        work_todo[i].append(workList[i]['우선순위'])
        work_todo[i].append(workList[i]['주문번호'])
        work_todo[i].append(workList[i]['남은공정수'])
        work_todo[i].append(workList[i]['주문자'])
        work_todo[i].append(workList[i]['주문수량'])

    for i in range(len(work_time)):
        work_time[i].append(item_time[i]['name'])
        work_time[i].append(item_time[i]['processNum'])
        for j in range(len(item_time[i]['processTimes'])):
            work_time[i].append(int(item_time[i]['processTimes'][j]))

    for i in range(len(work_todo)):
        all_work_list[i] = (work_todo[i][0], int(work_todo[i][5]), getAvailableMachineList(work_todo[i][0], available),
                            int(work_todo[i][1]), int(work_todo[i][2]), int(work_todo[i][3]), int(work_todo[i][4]), work_todo[i][6], int(work_todo[i][7]))

    return all_work_list, resetting, machine_amount, work_time
