json_condition = {
    "operation": "",
    "operand1": "",
    "operand2": "",
    "constOperand1": 0,
    "constOperand2": 0,
}

json_operation = {
    "operation": "",
    "result": 0,
    "operand1": "",
    "operand2": "",
    "constOperand1": 0,
    "constOperand2": 0,
}

json_match = {
    "state": 0,
    # Only set the needed one, the others are not to be pushed to ONOS
    # "condition0": False,
    # "condition1": False,
    # "condition2": False,
    # "condition3": False,
    #"efsmExtraMatch": dict(),
}

json_efsm_entry = {
    "match": "",
    "nextState": 0,
    "operations": [],
    "pktAction": 0
}

json_pkt_action = {
    "action": "",
    "id": 0
}
