

def GetTradingDefaultInfoFormat(h1):
    return "fingerPrint={0}\npair=<交易对>\namount=<交易量>\ndirection=<rise/fall>".format(h1)

def ParseTradingFormat(infos):
    res = {}
    variables = infos.split()
    for var in variables:
        info = var.split("=", 1)
        res[info[0]] = info[1]
    return res
        