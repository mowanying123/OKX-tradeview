import hashlib
from datetime import datetime

def GetTradingDefaultInfoFormat(finger):
    return "fingerPrint={0}\npair=<交易对>\namount=<交易量>\ndirection=<rise/fall>".format(finger)

def ParseTradingFormat(info):
    res = {}
    variables = infos.split()
    for var in variables:
        info = var.split("=", 1)
        res[info[0]] = info[1]
    return res