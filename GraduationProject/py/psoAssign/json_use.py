def extract_json(input_json):
    import json
    with open(input_json, encoding="utf-8") as f:
        data = json.load(f)


    workList = data['workList']
    available = data["machineAvailable"]
    item_time = data["itemWorkTime"]
    resetting = data["resettingTime"]
    work_tuple = []

    available_array = [[] for _ in range(len(available))]  # 이중배열 선언 0 index 가 기계번호 그 뒤로는 모두 가용 품목
    len_available = 0
    for i, t in enumerate(available):
        len_available += 1
        for j in t:
            available_array[i].append(j)

    for i, tuples in enumerate(workList):
        available_machine = []
        for i2, k in enumerate(available_array):
            if tuples["품목"] in k:
                available_machine.append(i2+1)
        for _ in range(int(tuples["남은공정수"])):
            work_tuple.append((0, available_machine, workList[i]["deadline"], int(workList[i]["우선순위"]), int(workList[i]["주문번호"]),
                              0, workList[i]["품목"], 0, workList[i]["주문자"], workList[i]["주문수량"], workList[i]["주문시간"]))

    sequence = [[] for _ in range(0, len(item_time))]

    for i, p in enumerate(item_time):
        sequence[i].append([p["name"], int(p["processNum"]), p["processTimes"]])

    return work_tuple, resetting, len(data["machineArray"]), sequence
