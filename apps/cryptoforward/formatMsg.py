import hashlib
from datetime import datetime

def GetTradingDefaultInfoFormat():
    m1 = hashlib.md5(str(datetime.now()).encode("utf-8"))
    h1 = m1.hexdigest()
    return "fingerPrint={0}\npair=<交易对>\namount=<交易量>\ndirection=<rise/fall>".format(h1)

def ParseTradingFormat(info):
    res = {}
    variables = infos.split()
    for var in variables:
        info = var.split("=", 1)
        res[info[0]] = info[1]
    return res