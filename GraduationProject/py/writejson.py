import json
from collections import OrderedDict
from greedy.greed import getDeadlineResult
from greedy.greed import getPriorityResult
from greedy.greed import getCombiResult
from psoAssign.pso_assignment import pso_result
# from psoAssign.pso_assignment import Dday
# from psoAssign.pso_assignment import combination
# from psoAssign.pso_assignment import pre_priority
# from psoAssign.pso_assignment import pre_Dday
# from psoAssign.pso_assignment import pre_combination

greedy_deadline_machine_result, greedy_deadline_score, greedy_deadline_remain_works = getDeadlineResult()
greedy_priority_machine_result, greedy_priority_score, greedy_priority_remain_works = getPriorityResult()
greedy_combi_machine_result, greedy_combi_score, greedy_combi_remain_works = getCombiResult()

pso_priority_machine_result, pso_priority_score, pso_priority_remain_works, pso_deadline_machine_result, pso_deadline_score, pso_deadline_remain_works, pso_combi_machine_result, pso_combi_score, pso_combi_remain_works, psopre_priority_machine_result, psopre_priority_score, psopre_priority_remain_works, psopre_deadline_machine_result, psopre_deadline_score, psopre_deadline_remain_works, psopre_combi_machine_result, psopre_combi_score, psopre_combi_remain_works = pso_result()

# pso_deadline_machine_result, pso_deadline_score, pso_deadline_remain_works = Dday(True)
# pso_priority_machine_result, pso_priority_score, pso_priority_remain_works = priority(True)
# pso_combi_machine_result, pso_combi_score, pso_combi_remain_works = combination(True)
#
# Dday_optimal_score = 2 ** 63  # optimal
# pri_optimal_score = 2 ** 63  # optimal
# comb_optimal_score = 2 ** 63  # optimal
#
# psopre_deadline_machine_result, psopre_deadline_score, psopre_deadline_remain_works = Dday(False)
# psopre_priority_machine_result, psopre_priority_score, psopre_priority_remain_works = priority(False)
# psopre_combi_machine_result, psopre_combi_score, psopre_combi_remain_works = combination(False)


def convertTime(time):
    hour = time // 60
    minute = time % 60
    if minute < 10:
        result = str(hour) + ":0" + str(minute)
    else:
        result = str(hour) + ":" + str(minute)
    return result

def makeJson(machineresult, score, remainwork):
    resultList = OrderedDict()
    resultList["resultList"] = []
    resultList["columnName"] = ["주문번호", "품목명", "공정번호", "배정기계", "시작시간", "종료시간", "공정시간", "재셋팅시간", "주문자", "주문수량"]
    resultList["remaincol"] = ["품목", "주문시간", "deadline", "우선순위", "주문번호", "남은공정수", "주문자", "주문수량"]
    for i in range(len(machineresult)):
        time = 0
        for j in range(machineresult[i][2]):
            element = OrderedDict()
            element["주문번호"] = str(machineresult[i][0][j][1])
            element["품목명"] = machineresult[i][0][j][0]
            element["공정번호"] = str(machineresult[i][0][j][2])
            element["배정기계"] = str(i + 1)
            element["시작시간"] = convertTime(time)
            element["종료시간"] = convertTime(time + machineresult[i][0][j][3] + machineresult[i][0][j][4])
            time = time + machineresult[i][0][j][3] + machineresult[i][0][j][4]
            element["공정시간"] = str(machineresult[i][0][j][3])
            element["재셋팅시간"] = str(machineresult[i][0][j][4])
            element["주문자"] = machineresult[i][0][j][5]
            element["주문수량"] = str(machineresult[i][0][j][6])
            resultList["resultList"].append(element)
    resultList["remainWorks"] = []
    for i in range(len(remainwork)):
        element = OrderedDict()
        element["품목"] = remainwork[i][0]
        element["주문시간"] = str(remainwork[i][1])
        element["deadline"] = str(remainwork[i][2])
        element["우선순위"] = str(remainwork[i][3])
        element["주문번호"] = str(remainwork[i][4])
        element["남은공정수"] = str(remainwork[i][5])
        element["주문자"] = remainwork[i][6]
        element["주문수량"] = str(remainwork[i][7])
        resultList["remainWorks"].append(element)
    resultList["score"] = score
    return resultList

greedy_deadline_resultlist = makeJson(greedy_deadline_machine_result, greedy_deadline_score, greedy_deadline_remain_works)
greedy_priority_resultlist = makeJson(greedy_priority_machine_result, greedy_priority_score, greedy_priority_remain_works)
greedy_combi_resultlist = makeJson(greedy_combi_machine_result, greedy_combi_score, greedy_combi_remain_works)

pso_deadline_resultlist = makeJson(pso_deadline_machine_result, pso_deadline_score, pso_deadline_remain_works)
pso_priority_resultlist = makeJson(pso_priority_machine_result, pso_priority_score, pso_priority_remain_works)
pso_combi_resultlist = makeJson(pso_combi_machine_result, pso_combi_score, pso_combi_remain_works)

psopre_deadline_resultlist = makeJson(psopre_deadline_machine_result, psopre_deadline_score, psopre_deadline_remain_works)
psopre_priority_resultlist = makeJson(psopre_priority_machine_result, psopre_priority_score, psopre_priority_remain_works)
psopre_combi_resultlist = makeJson(psopre_combi_machine_result, psopre_combi_score, psopre_combi_remain_works)


greedy_temp = OrderedDict()
greedy_temp["deadline"] = greedy_deadline_resultlist
greedy_temp["priority"] = greedy_priority_resultlist
greedy_temp["combie"] = greedy_combi_resultlist

pso_temp = OrderedDict()
pso_temp["deadline"] = pso_deadline_resultlist
pso_temp["priority"] = pso_priority_resultlist
pso_temp["combie"] = pso_combi_resultlist

psopre_temp = OrderedDict()
psopre_temp["deadline"] = psopre_deadline_resultlist
psopre_temp["priority"] = psopre_priority_resultlist
psopre_temp["combie"] = psopre_combi_resultlist

totalresult = OrderedDict()
totalresult["greedy"] = greedy_temp
totalresult["pso"] = pso_temp
totalresult["psopre"] = psopre_temp

temp = json.dumps(totalresult, ensure_ascii=False, indent="\t")

f = open("../saveresult/result.json", 'w')
f.write(temp)
f.close()

print(temp)
