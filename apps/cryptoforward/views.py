from django.shortcuts import render
import json
from django.http import HttpResponse, HttpResponseRedirect
from .formatMsg import ParseTradingFormat
from .models import DepositAccount, ExcangeSignalTrading

from django.views.decorators.csrf import csrf_exempt

accountPair = {} # finger-print:Account pair map
signalPair = {} # finger-print:Signal pair map

def resMsg(data):
    return HttpResponse(json.dumps({"ret":200, "data":data}), content_type="text/json")

def resErrObj(data):
    return HttpResponse(json.dumps({"ret":402, "data":data}), content_type="text/json")

def errorMsg(msg):
    print("something went wrong\n======================\n", msg, "\n======================")
    return HttpResponse(json.dumps({"ret":400, "msg":msg}), content_type="text/json")

# Create your views here.
@csrf_exempt
def trade_API_view(request):
    if request.method == "POST":
        txt = request.body.decode("utf-8")
        data = ParseTradingFormat(txt)
        if "fingerPrint" in data:
            signals = ExcangeSignalTrading.objects.filter(trade_pair__finger_print=data["fingerPrint"])
            if signals.count > 0:
                signalPair[data["fingerPrint"]] = {"entities":signals.all(), "context":txt}
                print("放入 交易信号 ", signalPair)
            accounts = ExcangeSignalTrading.objects.filter(trade_pair__finger_print=data["fingerPrint"])
            if accounts.count > 0:
                accountPair[data["fingerPrint"]] = {"entities":accounts.all(), "context":txt}
                print("放入 关联账户 ", signalPair)
            return resMsg("ok")
        else:
            errorMsg("incomeing data wrong, income data not correct:{0}".format(txt))

    return errorMsg("wrong method")