import psoAssign
import json
from psoAssign.pyswarm import pso
from psoAssign.json_use import extract_json
from dateutil.parser import parse
import sys

input_json = './input.json'
# input_json = json.loads(input_json)
works, rest_time, machine_amount, sequence, available = extract_json(input_json)  # 엑셀에서 데이터를 가져 옴

alpha = 0  # [[] for _ in range(machine_amount)]  # 전날 스케줄링 하지 않은 시간을 기록하기 위함.
day = parse('20180811')

# works 의 구성 : (소요시간, 가능한 기계, due_date, 우선순위, 주문번호, 0, 품목)
# work  의 구성 : (소요시간, 가능한 기계, due_date, 우선순위, 주문번호, 변수'x', 품목)

pri_optimal_score = 2 ** 63  # optimal
pri_optimal_schedule_machine = []  # 주문번호 순으로 가공기계가 입력됨
pri_optimal_m_list = []
pri_optimal_non_list = []

Dday_optimal_score = 2 ** 63  # optimal
Dday_optimal_schedule_machine = []  # 주문번호 순으로 가공기계가 입력됨
Dday_optimal_m_list = []
Dday_optimal_non_list = []

comb_optimal_score = 2 ** 63  # optimal
comb_optimal_schedule_machine = []  # 주문번호 순으로 가공기계가 입력됨
comb_optimal_m_list = []
comb_optimal_non_list = []

# 공정별로 나눔
def ressetingTime(alpha1, beta):
    if alpha1 == ' ':
        return 0
    else:
        resting_time = rest_time[alpha1][beta]
        return int(resting_time)

# 우선순위를 기준으로 sorting
def sort_by_decimal(item):
    tem = item[5] - int(item[5])
    return tem

# 공정순서를 기준으로 sorting
def sort_by_jobnum(item):
    tem1 = item[6].split("_")
    return tem1[1]

# 작업순서대로 sorting
def sort_by_job(item):
    return item[4]

temp = 0
repeat = 0
temps = 0

for i9, m in enumerate(works):
    b = list(works[i9])
    for h in available:
        if m[6] == h[0]:
            b[11] = h[1:]
            continue
    works[i9] = tuple(b)
# print(works)

for i5, w in enumerate(works):
    a = list(works[i5])
    for i6, n in enumerate(sequence):
        if a[6] == n[0][0]:
            # print(works[i5][6])
            if w[4] == temps:
                repeat += 1
                temp = int(n[0][1]) - repeat
                a[6] = str(works[i5][6]) + '_' + str(temp)
            else:
                repeat = 0
                a[6] = str(works[i5][6]) + '_' + str(n[0][1])
            a[0] = int(n[0][2][temp - 1])
            works[i5] = tuple(a)
            temps = w[4]
            continue
    # print(works[i5])
works = sorted(works, key=sort_by_decimal)

# 공정으로 인해 늘어난 작업번호를 tuple에 추가
for i8, u in enumerate(works):
    b = list(works[i8])
    b[7] = i8
    works[i8] = tuple(b)
# print(works)


########################################################## 이까지는 공통으로 모두 work 처리함 ############################
def Pretreatment(work):
    machine = []  # 작업당 배정된 기계 0~n이 들어간다.

    for i2, w1 in enumerate(work):
        integer = int(w1[5])
        # 마지막 정수가 되어버리면 machine 이 매칭되지 않아서 예외처리함
        if w1[5] - integer == 0 and integer != 0:
            integer -= 1
        # 변수에서 정수를 추출하여 작동시킬 기계를 정함 배열 index(1번기계: 0 2번기계: 1)
        machine.append(work[i2][1][integer] - 1)

    # 기계마다 사용된 시간을 계산하여 스케줄링이 가능한지를 알아보기 위함(24h)
    m_list = [[1440, [], " "] for _ in range(0, machine_amount)]
    sort_work = sorted(work, key=sort_by_decimal)
    # sort_work = sorted(sort_works1, key=sort_by_jobnum)
    sort_work2 = sort_work
    ##########################################################################

    # 변수 x를 기준으로 sort 된 리스트

    # print(sort_work)
    sort_work_len = len(sort_work) + 1
    last_work = [[1440, 1] for _ in range(0, len(sort_work))]

    # sort_work 가 while 문을 넘어서 갯수가 변하지 않으면 더이상 작업을 할 수 없다는 말임


    scheduled_list = []

    scheduled_len = len(scheduled_list) + 1
    fire = 0
    while len(scheduled_list) != scheduled_len:

        i7 = 0
        fire += 1
        # print(fire)

        scheduled_len = len(scheduled_list)

        for i7 in range(len(sort_work)):
        # while i7 < len(sort_work):
            for y in range(len(sort_work[i7][11])):

                # 조건 1 : 기계의 남은시간이 0 미만이 되는 작업은 입력 될 수 없다.
                # 조건 2 : 작업끼리 겹치지 않기 위해서 한 작업의 마지막 작업시간보다 빠른 시간에는 입력 될 수 없다.
                # 조건 3 : 같은 작업에서 공정 순서가 빠른 순서로만 입력된다. 뛰어넘는것도 불가능하다.
                # print("check")
                # print(len(sort_work[i7][11]))
                # print(int(sort_work[i7][5])-y)
                # print(sort_work[i7][11][int(sort_work[i7][5])-y])
                machine1 = sort_work[i7][11][int(sort_work[i7][5])-y] - 1
                reset = ressetingTime(m_list[machine1][2], sort_work[i7][6].split("_")[0])
                if m_list[machine1][0] - (sort_work[i7][0] + reset) >= 0 and \
                        last_work[sort_work[i7][4] - 1][0] >= m_list[machine1][0] and \
                        last_work[sort_work[i7][4] - 1][1] == int(sort_work[i7][6].split("_")[1]):
                    ###############################             조건            ###########################################
                    # print("check")
                    # start = 1440 - m_list[machine1][0]
                    # m_list 에 수행 된 작업의 정보를 입력한다. (작업번호, 작업이름, resetting 시간, 작업시작, 작업시간, 작업 끝난 시간)
                    m_list[machine1][1].append(
                        [sort_work[i7][6].split("_")[0],
                         sort_work[i7][4],
                         int(sort_work[i7][6].split("_")[1]),
                         sort_work[i7][0],
                         reset,
                         # start + reset,
                         # 1440 - (m_list[machine[sort_work[i7][7] - 1]][0] - (reset + sort_work[i7][0])),
                         sort_work[i7][8],
                         sort_work[i7][9]]
                    )

                    # m_list 의 시간에서 작업시간과 ressetingTime 을 뺀다.
                    m_list[machine1][0] -= (sort_work[i7][0] + reset)

                    # m_list 에 가장 최근 수행 된 작업의 종류를 입력한다.
                    m_list[machine1][2] = sort_work[i7][6].split("_")[0]
                    # 작업번호를 기준으로 마지막으로 수행이 끝난 시간을 기록한다.
                    last_work[sort_work[i7][4] - 1][0] = m_list[machine1][0]
                    last_work[sort_work[i7][4] - 1][1] += 1
                    # if machine[sort_work[i7][7] - 1] == 0:
                    #     print("check")

                    scheduled_list.append(sort_work[i7][7])
                    break
                else:
                    if y == len(sort_work[i7][11])-1:
                        break
    i8 = 0
    # print(scheduled_list)
    # print()
    while i8 < len(sort_work2):
        if sort_work2[i8][7] not in scheduled_list:
            del sort_work2[i8]
        else:
            i8 += 1
    # print(len(scheduled_list))
    # print(m_list)

    return sort_work2, m_list


def print_result():
    global optimal_schedule

    for i2, item in enumerate(pri_optimal_m_list):
        print(item)
        print("\n" + str(i2 + 1) + " 번기계:")
        for t in item[1]:
            print("품 : " + t[1] + " 주 : " + str(t[0]) + " 남 : " + str(t[2]))
    for i3, item in enumerate(Dday_optimal_m_list):
        print("\n" + str(i3 + 1) + " 번기계:")
        for t in item[1]:
            print("품 : " + t[1] + " 주 : " + str(t[0]) + " 남 : " + str(t[2]))
    for i3, item in enumerate(comb_optimal_m_list):
        print("\n" + str(i3 + 1) + " 번기계:")
        for t in item[1]:
            print("품 : " + t[1] + " 주 : " + str(t[0]) + " 남 : " + str(t[2]))
    # return result


# evaluation 함수 :
def pri_evaluation(work, time, days):
    non_scheduled_list = []

    sort_work, m_list = Pretreatment(work)
    # print(m_list)

    score = 0

    for job in sort_work:
        if job[4] not in non_scheduled_list:
            score += job[3]
            non_scheduled_list.append(job[4])
    # print(len(non_scheduled_list))

    global pri_optimal_score
    # print(str(score) + " _ " + str(pri_optimal_score))

    if score < pri_optimal_score:
        global pri_optimal_schedule_machine
        global pri_optimal_m_list
        global pri_optimal_non_list

        pri_optimal_score = score
        pri_optimal_m_list = m_list
        pri_optimal_non_list = sort_work
    return score


def Dday_evaluation(work, time, days):
    non_scheduled_list = []

    sort_work, m_list = Pretreatment(work)
    # print(m_list)

    score = 0

    for job in sort_work:
        if job[4] not in non_scheduled_list:
            score += (parse(str(job[2])) - days).days
            non_scheduled_list.append(job[4])
    # print(parse(str(job[2])))

    global Dday_optimal_score
    # print(str(score) + " _ " + str(Dday_optimal_score))

    if score < Dday_optimal_score:
        global Dday_optimal_schedule_machine
        global Dday_optimal_m_list
        global Dday_optimal_non_list
        Dday_optimal_score = score
        Dday_optimal_m_list = m_list
        Dday_optimal_non_list = sort_work
    return score


def comb_evaluation(work, time, days):
    non_scheduled_list = []

    sort_work, m_list = Pretreatment(work)
    # print(m_list)

    score = 0

    for job in sort_work:
        if job[4] not in non_scheduled_list:
            temp2 = 1
            if (parse(str(job[2])) - days).days < 0:
                temp2 = -1
            score += (6 - job[3]) + temp2 * (((parse(str(job[2]))) - days).days ** 2)
            non_scheduled_list.append(job[4])

    global comb_optimal_score
    # print(str(score) + " _ " + str(comb_optimal_score))

    if score < comb_optimal_score:
        global comb_optimal_schedule_machine
        global comb_optimal_m_list
        global comb_optimal_non_list

        comb_optimal_score = score
        comb_optimal_m_list = m_list
        comb_optimal_non_list = sort_work
    return score


def pri_input_pso(x):
    amounts = len(works)
    for i4 in range(0, amounts):
        a = list(works[i4])
        a[5] = x[i4]
        works[i4] = tuple(a)

    score = pri_evaluation(works, 24 + alpha, day)

    return score


def Dday_input_pso(x):
    amounts = len(works)
    for i4 in range(0, amounts):
        a = list(works[i4])
        a[5] = x[i4]
        works[i4] = tuple(a)

    score = Dday_evaluation(works, 24 + alpha, day)

    return score


def comb_input_pso(x):
    amounts = len(works)
    for i4 in range(0, amounts):
        a = list(works[i4])
        a[5] = x[i4]
        works[i4] = tuple(a)

    score = comb_evaluation(works, 24 + alpha, day)

    return score


lb = []  # work 마다의 lower bound
ub = []  # work 마다의 upper bound
amount = len(works)  # work 의 갯수

# upper bound 를 가용기계의 수만큼 할당함
for i in range(0, amount):
    lb.append(0)
    ub.append(len(works[i][1]))


def priority(flag):
    comb_xopt1, optimal_score = pso(pri_input_pso, lb, ub, flag=flag)
    global pri_optimal_non_list
    global pri_optimal_m_list
    pri_non = []
    works_p = sorted(pri_optimal_non_list, key=sort_by_job)
    temp_p = 0
    for p in works_p:
        if p[4] != temp_p:
            pri_non.append([p[6].split("_")[0], p[10], p[2], p[3], p[4], 1, p[8], p[9]])
        else:
            b = list(pri_non[- 1])
            b[5] += 1
            pri_non[- 1] = tuple(b)
        temp_p = p[4]

    temp2 = [[] for _ in range(0, len(pri_optimal_m_list))]
    for i2 in range(len(temp2)):
        temp2[i2] = [pri_optimal_m_list[i2][1]]
        temp2[i2].append(1440 - pri_optimal_m_list[i2][0])
        temp2[i2].append(len(pri_optimal_m_list[i2][1]))
    return temp2, optimal_score, pri_non


def Dday(flag):
    comb_xopt1, optimal_score = pso(Dday_input_pso, lb, ub, flag=flag)
    global Dday_optimal_non_list
    global Dday_optimal_m_list
    Dday_non = []
    works_d = sorted(Dday_optimal_non_list, key=sort_by_job)
    temp_d = 0
    for d in works_d:
        if d[4] != temp_d:
            Dday_non.append((d[6].split("_")[0], d[10], d[2], d[3], d[4], 1, d[8], d[9]))
        else:
            b = list(Dday_non[- 1])
            b[5] += 1
            Dday_non[- 1] = tuple(b)
        temp_d = d[4]

    temp2 = [[] for _ in range(len(Dday_optimal_m_list))]
    for i2 in range(len(temp2)):
        temp2[i2] = [Dday_optimal_m_list[i2][1]]
        temp2[i2].append(1440 - Dday_optimal_m_list[i2][0])
        temp2[i2].append(len(Dday_optimal_m_list[i2][1]))

    return temp2, optimal_score, Dday_non


def combination(flag):
    comb_xopt1, optimal_score = pso(comb_input_pso, lb, ub, flag=flag)
    global comb_optimal_non_list
    global comb_optimal_m_list
    comb_non = []
    works_c = sorted(comb_optimal_non_list, key=sort_by_job)
    temp_c = 0
    for c in works_c:
        if c[4] != temp_c:
            comb_non.append([c[6].split("_")[0], c[10], c[2], c[3], c[4], 1, c[8], c[9]])
        else:
            b = list(comb_non[- 1])
            b[5] += 1
            comb_non[- 1] = tuple(b)
        temp_c = c[4]

    temp2 = [[] for _ in range(0, len(comb_optimal_m_list))]
    for i2 in range(len(temp2)):
        temp2[i2] = [comb_optimal_m_list[i2][1]]
        temp2[i2].append(1440 - comb_optimal_m_list[i2][0])
        temp2[i2].append(len(comb_optimal_m_list[i2][1]))
    return temp2, optimal_score, comb_non


# 실행부

def pso_result():

    priority_list, priority_score, priority_non_list = priority(True)
    Dday_list, Dday_score, Dday_non_list = Dday(True)
    comb_list, comb_score, comb_non_list = combination(True)

    global Dday_optimal_score
    global pri_optimal_score
    global comb_optimal_score
    Dday_optimal_score = 2 ** 63  # optimal
    pri_optimal_score = 2 ** 63  # optimal
    comb_optimal_score = 2 ** 63  # optimal

    pre_priority_list, pre_priority_score, pre_priority_non_list = priority(False)
    pre_Dday_list, pre_Dday_score, pre_Dday_non_list = Dday(False)
    pre_comb_list, pre_comb_score, pre_comb_non_list = combination(False)


    return priority_list, priority_score, priority_non_list, Dday_list, Dday_score, Dday_non_list, comb_list, comb_score, comb_non_list, pre_priority_list, pre_priority_score, pre_priority_non_list, pre_Dday_list, pre_Dday_score, pre_Dday_non_list, pre_comb_list, pre_comb_score, pre_comb_non_list


