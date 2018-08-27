from pyswarm import pso
from excel import extract_excel
from dateutil.parser import parse

works_all, works, rest_time, machine_amount, indexs = extract_excel('inputdata.xlsx')  # 엑셀에서 데이터를 가져 옴
alpha = 0  # [[] for _ in range(machine_amount)]  # 전날 스케줄링 하지 않은 시간을 기록하기 위함.
day = parse('20180812') # 날짜는 스케줄링을 실행하는 날짜와 스케줄링 대상이 되는 날짜와 그 다음 날짜를 가진다.

# works 의 구성 : (소요시간, 가능한 기계, due_date, 우선순위, 주문번호)
# work  의 구성 : (소요시간, 가능한 기계, due_date, 우선순위, 주문번호, 변수'x')

optimal_score = 2**63
optimal_schedule_machine = []  # 주문번호 순으로 가공기계가 입력됨
optimal_schedule = []

# 기계별 당일 남은시간을 저장하는 배열
remain_time = [0 for i in range(machine_amount)]

# evaluation 에서의 변수 x 중 소수 부분을 사용해서 sorting 하기 위한 key 값
def sort_by_decimal(item):
    a = item[5] - int(item[5])
    return a

def sort_by_order(item):
    return item[4]

# print 하기 위한 key 값인데 아직 못쓰고 있음
def sort_for_print(item):
    return item[0]

def resetingTime(alpha, beta):
    resting_time = rest_time[indexs.index(alpha), indexs.index(beta)]
    return resting_time

def print_result():
    result = [[] for _ in range(0, len(optimal_schedule_machine))]
    global optimal_schedule
    for i2, job in enumerate(optimal_schedule):
        print(i2)
        result[i2].append(optimal_schedule_machine[job-1])
        result[i2].append(job)
        result[i2].append(works[job-1][6])

    print(result)

# evaluation 함수 :
def evaluation(work, time, day):
    # import datetime
    machine = []  # 작업당 배정된 기계 0~n이 들어간다.
    scheduled_list = []  # 스케줄링에 들어간 작업번호 (처리 될 작업번호)

    for i2, w in enumerate(work):
        integer = int(w[5])
        # 마지막 정수가 되어버리면 machine 이 매칭되지 않아서 예외처리함
        if w[5] - integer == 0 and integer != 0:
            integer -= 1
        # 변수에서 정수를 추출하여 작동시킬 기계를 정함 배열 index(1번기계: 0 2번기계: 1)
        machine.append(work[i2][1][integer]-1)

    # 기계의 수만큼 이중 list를 생성. 기계마다의 시간을 계산하기 위함(24h)
    m_list = [[1440 + remain_time[i6], 'First'] for i6 in range(0, machine_amount)]
    # 변수 x를 기준으로 sort된 리스트
    sort_work = sorted(work, key=sort_by_decimal)

    for j in sort_work:
        if m_list[machine[j[4]-1]][0] - (j[0] + resetingTime(m_list[machine[j[4] - 1]][1], j[6])) >= 0:
            m_list[machine[j[4] - 1]][0] -= (j[0] + resetingTime(m_list[machine[j[4] - 1]][1], j[6]))
            m_list[machine[j[4] - 1]][1] = j[6]
            scheduled_list.append(j[4])
    # print(scheduled_list)

    score = 0
    for job in work:
        if job[4] in scheduled_list:
            continue
        else:
            if (day-parse(str(job[2]))).days <= 0:
                score += job[0]
    # print(score)
    global optimal_score

    if score < optimal_score:
        global optimal_schedule_machine
        global optimal_schedule
        optimal_score = score
        optimal_schedule_machine = machine
        optimal_schedule = scheduled_list

    # 데드라인 넘겼을 때 패널티 부여 해야한다.(우선순위 반영)

    return score


def input_pso(x):
    amounts = len(works)
    for i4 in range(0, amounts):
        a = list(works[i4])
        a[5] = x[i4]
        works[i4] = tuple(a)

    score = evaluation(works, 24 + alpha, day)
    return score

lb = []  # work 마다의 lower bound
ub = []  # work 마다의 upper bound
amount = len(works)  # work 의 갯수

# upper bound 를 가용기계의 수만큼 할당함
for i in range(0, amount):
    lb.append(0)
    ub.append(len(works[i][1]))

# 실행부
xopt, fopt = pso(input_pso, lb, ub)

# 결과 출력
print(xopt) # x출력
print(fopt) # 최저 코스트

print_result()
# print_schedule(fopt)

