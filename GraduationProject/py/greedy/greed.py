from greedy.getJson import extract_json
import sys
# 기본적으로 우선으로 보는 것(deadline, 우선순위, 작업시간)이 동등하다면 주문번호를 우선으로 본다.
data = './input.json'

works_list, resetting_time, machine_amount, listOfProcess = extract_json(data)

# 날짜
day = 20180811
dayWorkCount = 0
# 총 공정 수
total_process_num = 0

# 품목명을 받아 품목명 번호 값 리턴
def itemName(alpha):
    temp = [0 for _ in range(len(listOfProcess))]
    for i in range(len(listOfProcess)):
        temp[i] = listOfProcess[i][0]
    itemname = temp.index(alpha)
    return itemname

# resetting시간을 리턴하는 함수
def resetTime(alpha, beta):
    if alpha == 'first':
        reset_time = 0
    else:
        reset_time = int(resetting_time[alpha][beta])
    return reset_time

# day에 주문한 품목들
dayWorkCount = len(works_list)

today_list = [[] for _ in range(dayWorkCount)]

# 지정한 날짜에 주문된 품목 리스트
for i in range(dayWorkCount):
    today_list[i] = works_list[i]
    total_process_num = total_process_num + today_list[i][1]

# 기계 별 리스트(배치된 품목 리스트(품명, 시간, 주문번호, 공정번호), 사용된 시간(분), 들아간 작업 수, 마지막에 들어간 품목명)
machine_state_deadline = [[[], 0, 0, 'first'] for _ in range(machine_amount)]
machine_state_priority = [[[], 0, 0, 'first'] for _ in range(machine_amount)]
machine_state_combi = [[[], 0, 0, 'first'] for _ in range(machine_amount)]

#스케줄링 별 패널티 score
panelity_score_deadline = 0
panelity_score_priority = 0
panelity_score_combi = 0

#스케줄링 되지 않은 공정이 들어가는 배열
rest_after_deadline = []
rest_after_priority = []
rest_after_combi = []

#스케줄링 되지 않은 작업이 들어가는 배열
rest_after_deadline_result = []
rest_after_priority_result = []
rest_after_combi_result = []


# 작업별 차지한 시간을 표시하는 2차원 배열, 각 배열에는 작업시작시간, 종료시간의 순서쌍이 여러개(공정 수) 들어간다.
check_overlap_table_deadline = [[(0,0), (0,0), (0,0), (0,0)] for _ in range(dayWorkCount)]
check_overlap_table_priority = [[(0,0), (0,0), (0,0), (0,0)] for _ in range(dayWorkCount)]
check_overlap_table_combi = [[(0,0), (0,0), (0,0), (0,0)] for _ in range(dayWorkCount)]

# 작업을 넣을 때 겹치는 지, 공정번호 낮을수록 먼저하는지 확인
# 들어갈수 있으면 1을 리턴 없으면 0을 리턴
# parameter : 주문번호, 시작시간, 종료시간, 공정 번호
def checkOverlap(orderNum, start, finish, processNum, timetable):
    possiblecheck = 0
    if processNum == 0:
        possiblecheck = 1
    else:
        if timetable[orderNum - 1][processNum - 1][1] != 0:
            if timetable[orderNum - 1][processNum - 1][1] <= start:
                possiblecheck = 1
    return possiblecheck

# deadline 우선 스케줄링
def deadline_scheduling():
    # 마감일-현재날짜 순으로 정렬
    # 정렬된 작업이 들어갈 리스트(품목명, 주문번호, 공정수, 가용기계리스트, 마감일까지 남은시간(작을수록 우선))
    work_state_deadline = [[] for _ in range(len(today_list))]
    for i in range(len(today_list)):
        work_state_deadline[i] = [today_list[i][0], today_list[i][6], today_list[i][1],
                                  today_list[i][2], today_list[i][4] - day, today_list[i][7], today_list[i][8], today_list[i][3], today_list[i][4], today_list[i][5]]

    work_state_deadline.sort(key=lambda x:x[4])

    # 정렬된 것을 공정수에 따라 입력 파일로 생성
    # 품목명 주문번호 공정번호 기계리스트
    total_process_list = [[] for _ in range(total_process_num)]

    count = 0
    for i in range(len(work_state_deadline)):
        for j in range(work_state_deadline[i][2]):
            total_process_list[count] = [work_state_deadline[i][0], work_state_deadline[i][1], j + 1, listOfProcess[itemName(work_state_deadline[i][0])][j + 2],
                                         work_state_deadline[i][3], work_state_deadline[i][5], work_state_deadline[i][6], work_state_deadline[i][4],
                                         work_state_deadline[i][7], work_state_deadline[i][8], work_state_deadline[i][9]]
            count = count + 1

    for i in range(count):
        inputcheck = 0
        for j in range(len(total_process_list[i][4])):
            now_machine_num = total_process_list[i][4][j] - 1
            if machine_state_deadline[now_machine_num][1] + total_process_list[i][3] + resetTime(machine_state_deadline[now_machine_num][3], total_process_list[i][0]) < 1440:
                if checkOverlap(total_process_list[i][1], machine_state_deadline[now_machine_num][1], machine_state_deadline[now_machine_num][1] + total_process_list[i][3] + resetTime(machine_state_deadline[now_machine_num][3], total_process_list[i][0]), total_process_list[i][2] - 1, check_overlap_table_deadline) == 1:
                    check_overlap_table_deadline[total_process_list[i][1] - 1][total_process_list[i][2] - 1] = (machine_state_deadline[now_machine_num][1], machine_state_deadline[now_machine_num][1] + total_process_list[i][3] + resetTime(machine_state_deadline[now_machine_num][3], total_process_list[i][0]))
                    machine_state_deadline[now_machine_num][0].append([total_process_list[i][0], total_process_list[i][1], total_process_list[i][2], total_process_list[i][3], resetTime(machine_state_deadline[now_machine_num][3], total_process_list[i][0]), total_process_list[i][5], total_process_list[i][6]])
                    machine_state_deadline[now_machine_num][1] = machine_state_deadline[now_machine_num][1] + total_process_list[i][3] + resetTime(machine_state_deadline[now_machine_num][3], total_process_list[i][0])
                    machine_state_deadline[now_machine_num][2] = machine_state_deadline[now_machine_num][2] + 1
                    machine_state_deadline[now_machine_num][3] = total_process_list[i][0]
                    inputcheck = 1
                    break
        if inputcheck == 0:
            rest_after_deadline.append([total_process_list[i][0], total_process_list[i][8], total_process_list[i][9], total_process_list[i][10],
                                       total_process_list[i][1], total_process_list[i][2], total_process_list[i][5], total_process_list[i][6]])

# 우선순위 우선 스케줄링
def priority_scheduling():
    # 마감일-현재날짜 순으로 정렬
    # 정렬된 작업이 들어갈 리스트(품목명, 주문번호, 공정수, 가용기계리스트, 마감일까지 남은시간(작을수록 우선))
    work_state_priority = [[] for _ in range(len(today_list))]
    for i in range(len(today_list)):
        work_state_priority[i] = [today_list[i][0], today_list[i][6], today_list[i][1], today_list[i][2],
                                  today_list[i][5], today_list[i][7], today_list[i][8], today_list[i][3], today_list[i][4]]

    work_state_priority.sort(key=lambda x:-x[4])

    # 정렬된 것을 공정수에 따라 입력 파일로 생성
    # 품목명 주문번호 공정번호 기계리스트
    total_process_list = [[] for _ in range(total_process_num)]

    count = 0
    for i in range(len(work_state_priority)):
        for j in range(work_state_priority[i][2]):
            total_process_list[count] = [work_state_priority[i][0], work_state_priority[i][1], j + 1, listOfProcess[itemName(work_state_priority[i][0])][j + 2],
                                         work_state_priority[i][3], work_state_priority[i][5], work_state_priority[i][6], work_state_priority[i][7], work_state_priority[i][8],
                                         work_state_priority[i][4]]
            count = count + 1

    for i in range(count):
        inputcheck = 0
        for j in range(len(total_process_list[i][4])):
            now_machine_num = total_process_list[i][4][j] - 1
            if machine_state_priority[now_machine_num][1] + total_process_list[i][3] + resetTime(machine_state_priority[now_machine_num][3], total_process_list[i][0]) < 1440:
                if checkOverlap(total_process_list[i][1], machine_state_priority[now_machine_num][1], machine_state_priority[now_machine_num][1] + total_process_list[i][3] + resetTime(machine_state_priority[now_machine_num][3], total_process_list[i][0]), total_process_list[i][2] - 1, check_overlap_table_priority) == 1:
                    check_overlap_table_priority[total_process_list[i][1] - 1][total_process_list[i][2] - 1] = (machine_state_priority[now_machine_num][1], machine_state_priority[now_machine_num][1] + total_process_list[i][3] + resetTime(machine_state_priority[now_machine_num][3], total_process_list[i][0]))
                    machine_state_priority[now_machine_num][0].append([total_process_list[i][0], total_process_list[i][1], total_process_list[i][2], total_process_list[i][3], resetTime(machine_state_priority[now_machine_num][3], total_process_list[i][0]), total_process_list[i][5], total_process_list[i][6]])
                    machine_state_priority[now_machine_num][1] = machine_state_priority[now_machine_num][1] + total_process_list[i][3] + resetTime(machine_state_priority[now_machine_num][3], total_process_list[i][0])
                    machine_state_priority[now_machine_num][2] = machine_state_priority[now_machine_num][2] + 1
                    machine_state_priority[now_machine_num][3] = total_process_list[i][0]
                    inputcheck = 1
                    break
        if inputcheck == 0:
            rest_after_priority.append([total_process_list[i][0], total_process_list[i][7], total_process_list[i][8], total_process_list[i][9],
                 total_process_list[i][1], total_process_list[i][2], total_process_list[i][5], total_process_list[i][6]])

# 우선순위와 deadline을 복합적으로 적용
def combi_scheduling():
    # 마감일-현재날짜 순으로 정렬
    # 정렬된 작업이 들어갈 리스트(품목명, 주문번호, 공정수, 가용기계리스트, 마감일까지 남은시간(작을수록 우선))
    work_state_combi = [[] for _ in range(len(today_list))]
    for i in range(len(today_list)):
        if (today_list[i][4] - day) >= 0:
            work_state_combi[i] = [today_list[i][0], today_list[i][6], today_list[i][1], today_list[i][2],
                                   ((6 - today_list[i][5]) + ((today_list[i][4] - day) * (today_list[i][4] - day))),
                                   today_list[i][7], today_list[i][8], today_list[i][3], today_list[i][4], today_list[i][5]]
        else:
            work_state_combi[i] = [today_list[i][0], today_list[i][6], today_list[i][1], today_list[i][2],
                                   ((6 - today_list[i][5]) - ((today_list[i][4] - day) * (today_list[i][4] - day))),
                                   today_list[i][7], today_list[i][8], today_list[i][3], today_list[i][4], today_list[i][5]]

    work_state_combi.sort(key=lambda x:x[4])

    # 정렬된 것을 공정수에 따라 입력 파일로 생성
    # 품목명 주문번호 공정번호 기계리스트
    total_process_list = [[] for _ in range(total_process_num)]

    count = 0
    for i in range(len(work_state_combi)):
        for j in range(work_state_combi[i][2]):
            total_process_list[count] = [work_state_combi[i][0], work_state_combi[i][1], j + 1, listOfProcess[itemName(work_state_combi[i][0])][j + 2],
                                         work_state_combi[i][3], work_state_combi[i][5], work_state_combi[i][6], work_state_combi[i][7], work_state_combi[i][8],
                                         work_state_combi[i][9], work_state_combi[i][4]]
            count = count + 1

    for i in range(count):
        inputcheck = 0
        for j in range(len(total_process_list[i][4])):
            now_machine_num = total_process_list[i][4][j] - 1
            if machine_state_combi[now_machine_num][1] + total_process_list[i][3] + resetTime(machine_state_combi[now_machine_num][3], total_process_list[i][0]) < 1440:
                if checkOverlap(total_process_list[i][1], machine_state_combi[now_machine_num][1], machine_state_combi[now_machine_num][1] + total_process_list[i][3] + resetTime(machine_state_combi[now_machine_num][3], total_process_list[i][0]), total_process_list[i][2] - 1, check_overlap_table_combi) == 1:
                    check_overlap_table_combi[total_process_list[i][1] - 1][total_process_list[i][2] - 1] = (machine_state_combi[now_machine_num][1], machine_state_combi[now_machine_num][1] + total_process_list[i][3] + resetTime(machine_state_combi[now_machine_num][3], total_process_list[i][0]))
                    machine_state_combi[now_machine_num][0].append([total_process_list[i][0], total_process_list[i][1], total_process_list[i][2], total_process_list[i][3], resetTime(machine_state_combi[now_machine_num][3], total_process_list[i][0]), total_process_list[i][5], total_process_list[i][6]])
                    machine_state_combi[now_machine_num][1] = machine_state_combi[now_machine_num][1] + total_process_list[i][3] + resetTime(machine_state_combi[now_machine_num][3], total_process_list[i][0])
                    machine_state_combi[now_machine_num][2] = machine_state_combi[now_machine_num][2] + 1
                    machine_state_combi[now_machine_num][3] = total_process_list[i][0]
                    inputcheck = 1
                    break
        if inputcheck == 0:
            rest_after_combi.append([total_process_list[i][0], total_process_list[i][7], total_process_list[i][8], total_process_list[i][9],
                                        total_process_list[i][1], total_process_list[i][2], total_process_list[i][5], total_process_list[i][6]])

def getDeadlineResult():
    deadline_scheduling()
    panelity = 0
    for i in range(len(rest_after_deadline)):
        overlapcheck = 0
        for j in range(len(rest_after_deadline_result)):
            if rest_after_deadline_result[j][4] == rest_after_deadline[i][4]:
                rest_after_deadline_result[j][5] = rest_after_deadline_result[j][5] + 1
                overlapcheck = 1
                break
        if overlapcheck == 0:
            rest_after_deadline[i][5] = 1
            rest_after_deadline_result.append(rest_after_deadline[i])

    rest_after_deadline_result.sort(key=lambda x: x[4])

    for i in range(len(rest_after_deadline_result)):
        panelity = panelity + (rest_after_deadline_result[i][2] - day)

    panelity_score_deadline = panelity

    return machine_state_deadline, panelity_score_deadline, rest_after_deadline_result

def getPriorityResult():

    priority_scheduling()
    panelity = 0
    for i in range(len(rest_after_priority)):
        overlapcheck = 0
        for j in range(len(rest_after_priority_result)):
            if rest_after_priority_result[j][4] == rest_after_priority[i][4]:
                rest_after_priority_result[j][5] = rest_after_priority_result[j][5] + 1
                overlapcheck = 1
                break
        if overlapcheck == 0:
            rest_after_priority[i][5] = 1
            rest_after_priority_result.append(rest_after_priority[i])

    rest_after_priority_result.sort(key=lambda x: x[4])

    for i in range(len(rest_after_priority_result)):
        panelity = panelity + rest_after_priority_result[i][3]

    panelity_score_priority = panelity

    return machine_state_priority, panelity_score_priority, rest_after_priority_result

def getCombiResult():
    combi_scheduling()
    panelity = 0
    for i in range(len(rest_after_combi)):
        overlapcheck = 0
        for j in range(len(rest_after_combi_result)):
            if rest_after_combi_result[j][4] == rest_after_combi[i][4]:
                rest_after_combi_result[j][5] = rest_after_combi_result[j][5] + 1
                overlapcheck = 1
                break
        if overlapcheck == 0:
            rest_after_combi[i][5] = 1
            rest_after_combi_result.append(rest_after_combi[i])

    rest_after_combi_result.sort(key=lambda x: x[4])

    for i in range(len(rest_after_combi_result)):
        if (rest_after_combi_result[i][2] - day) >= 0:
            panelity = panelity + (6-rest_after_combi_result[i][3]) + ((rest_after_combi_result[i][2] - day) * (rest_after_combi_result[i][2] - day))
        else:
            panelity = panelity + (6 - rest_after_combi_result[i][3]) - ((rest_after_combi_result[i][2] - day) * (rest_after_combi_result[i][2] - day))

    panelity_score_combi = panelity

    return machine_state_combi, panelity_score_combi, rest_after_combi_result
