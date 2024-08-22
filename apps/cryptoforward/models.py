from django.db import models
from hashid_field import HashidAutoField
from django.contrib.auth.models import User as AuthUser, AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from .formatMsg import GetTradingDefaultInfoFormat
from django.utils.translation import gettext_lazy as _

class tradingType(models.IntegerChoices):
        BUY = 1, _("买入")
        SELL = 2, _("卖出")
        BUY_FUTURE_LOW = 3, _("做多买入")
        SELL_FUTURE_HIGH = 4, _("做空卖出")
        SELL_FUTURE_LOW = 5, _("做多卖出")
        BUY_FUTURE_HIGH = 6, _("做空买入")

# Create your models here.
class TradingPair (models.Model):
    id = models.AutoField(primary_key=True)
    treading_pair_currency = models.CharField(max_length=200, verbose_name="交易对币种")
    finger_print = HashidAutoField(verbose_name="指纹值")
    trading_context = models.TextField(blank=True, default=getHash, verbose_name="交易信息Context(json 格式)")

    def getHash(self):
        return GetTradingDefaultInfoFormat()

    def __str__(self):
        return "{0}-{1}".format(self.treading_pair_currency, self.finger_print)

class ExchangeChannel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name="交易所名称")
    base_url = models.CharField(max_length=200, verbose_name="交易所接口base url")

    def __str__(self):
        return self.name

class ExchangeOrder(models.Model):
    class State(models.IntegerChoices):
        UNKNOWN = 0, _("未知")
        PROCEED = 1, _("进行中")
        FINISH = 2, _("完成")
        FAILD = 3, _("失败")
    
    id = models.AutoField(primary_key=True)
    exchange_orderId = models.CharField(max_length=200, verbose_name="交易所订单Id")
    exchange = models.ForeignKey(ExchangeChannel, on_delete=models.CASCADE, related_name='exchange_order', verbose_name="关联交易所")
    trading_pair = models.ForeignKey(TradingPair, on_delete=models.CASCADE, related_name='order_trading_pair', verbose_name="关联交易对")
    amount = models.FloatField(default=0.0, verbose_name="交易数量")
    leverge = models.FloatField(default=1.0, verbose_name="交易杠杆")
    order_state = models.IntegerField(choices=State, verbose_name="订单状态")
    trading_Type = models.IntegerField(choices=tradingType, verbose_name="交易类型")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="交易创建时间")
    
    def __str__(self):
        return self.exchange_orderId
    
class ExchangeAccountInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=200, verbose_name="交易所账户名")
    token = models.CharField(max_length=200, verbose_name="交易所接口 token")
    exchange = models.ForeignKey(ExchangeChannel, on_delete=models.CASCADE, related_name='exchange_account', verbose_name="关联交易所")

    def __str__(self):
        return self.user_name

class ExcangeSignalTrading(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name="交易管道信号名称")
    trade_pair = models.ForeignKey(TradingPair, blank=true, null=True, on_delete=models.CASCADE, related_name='pipeline_trading_pair', verbose_name="关联交易对" )
    signal_api = models.CharField(max_length=200, verbose_name="交易信号api")
    format_string = models.TextField(blank=True, verbose_name="交易信号格式(json 格式)")
    order_list = models.ManyToManyField(ExchangeOrder, verbose_name="订单列表")

    def __str__(self):
        return self.user_name

class AccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class DepositAccount(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True, verbose_name="账户名")
    nickname = models.CharField(max_length=100, blank=True, verbose_name="昵称")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    trade_pair = models.ForeignKey(TradingPair, blank=True, null=True, on_delete=models.CASCADE, related_name='account_trading_pair', verbose_name="关联交易对")
    related_account = models.ForeignKey(ExchangeAccountInfo, on_delete=models.CASCADE, related_name='account_trading_pair', verbose_name="关联账户")
    order_list = models.ManyToManyField(ExchangeOrder, verbose_name="订单列表")

    objects = AccountManager()

    USERNAME_FIELD = 'account_name'

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.password = make_password(self.password)  # 确保在创建时加密密码
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.nickname
