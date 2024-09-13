from django.shortcuts import render
import json
from django.http import HttpResponse, HttpResponseRedirect
from .formatMsg import ParseTradingFormat
from .models import DepositAccount, ExcangeSignalTrading
from django_q.tasks import async_task, result
from django.views.decorators.csrf import csrf_exempt
from Queue import Queue
import requests
from django.core.cache import cache
from django_redis import get_redis_connection

accountPair = {} # finger-print:Account pair map
signalPair = {} # finger-print:Signal pair map

signalQueue = Queue()
con = get_redis_connection("default")

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
            if signals.count() > 0:
                item = {"fingerPrint":data["fingerPrint"], "entities":signals.all(), "context":data}
                print("放入 交易信号 ", signalPair)
                signalQueue.put(item)

            accounts = DepositAccount.objects.filter(trade_pair__finger_print=data["fingerPrint"])
            if accounts.count() > 0:
                accountPair[data["fingerPrint"]] = {"entities":accounts.all(), "context":data}
                print("放入 关联账户 ", signalPair)
            return resMsg("ok")
        else:
            errorMsg("incomeing data wrong, income data not correct:{0}".format(txt))

    return errorMsg("wrong method")

def execute_tasks_signal():
    if signalQueue.qsize() > 0:
        originalSize = signalQueue.qsize()
        for num in range(originalSize):
            item = signalQueue.get()
            context = item["context"]
            for singalEntity in item["entities"]:
                data = {}
                if context["direction"] == "rise":
                    order = item.order_list.filter(order_state=ExchangeOrder.State.FINISH).latest("id")
                    if item.signal_type == SignalType.BUY_LOW_ONLY and order.trading_Type == TradingType.SELL_FUTURE_LOW:
                        data = json.loads(singalEntity.format_string_enter_long)
                        data["trade_type"] = TradingType.BUY_FUTURE_LOW
                    elif item.signal_type == SignalType.SELL_HIGH_ONLY and order.trading_Type == TradingType.BUY_FUTURE_HIGH:
                        data = json.loads(singalEntity.format_string_exit_short)
                        data["trade_type"] = TradingType.BUY_FUTURE_HIGH
                    elif item.signal_type == SignalType.DUEL:
                        pass #以后再写双向的
                elif context["direction"] == "fall":
                    if item.signal_type == SignalType.BUY_LOW_ONLY and order.trading_Type == TradingType.BUY_FUTURE_LOW:
                        data = json.loads(singalEntity.format_string_exit_long)
                        data["trade_type"] = TradingType.SELL_FUTURE_LOW
                    elif item.signal_type == SignalType.SELL_HIGH_ONLY and order.trading_Type == TradingType.SELL_FUTURE_HIGH:
                        data = json.loads(singalEntity.format_string_enter_short)
                        data["trade_type"] = TradingType.BUY_FUTURE_HIGH
                    elif item.signal_type == SignalType.DUEL:
                        pass #以后再写双向的
                data["amount"] = context["amount"]
                data["timestamp"] = context["timenow"]
                data["instrument"] = context["ticker"]
                re = request.post(singalEntity.signal_api, data=json.dumps(data))
                if re.status == 500:
                    data["order_state"] = ExchangeOrder.State.FINISH
                item.order_list.create(exchange_orderId="signal"+re.data.id, trading_pair=item.trading_pair, order_state=data["order_state"], trading_type=data["trade_type"], amount=data["amount"])
                item.order_list.save()
                print(re)
    
def attach_order_(task, orders):
    pass
