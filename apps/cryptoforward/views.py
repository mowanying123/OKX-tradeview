from django.shortcuts import render
import json
from django.http import HttpResponse, HttpResponseRedirect
from .formatMsg import ParseTradingFormat
from .models import DepositAccount, ExcangeSignalTrading

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
def trade_API_view(request):
    if request.method == "POST":
        txt = request.data.decode('utf-8')
        data = ParseTradingFormat(txt)
        if "fingerPrint" in data:
            signals = ExcangeSignalTrading.objects.filter(trade_pair__finger_print=data["fingerPrint"])
            if signals.count > 0:
                signalPair[data["fingerPrint"]] = signals.all()
            accounts = ExcangeSignalTrading.objects.filter(trade_pair__finger_print=data["fingerPrint"])
            if accounts.count > 0:
                accountPair[data["fingerPrint"]] = accounts.all()
            return resMsg("ok")
        else:
            errorMsg("incomeing data wrong, income data not correct:{0}".format(txt))

    return errorMsg("wrong method")