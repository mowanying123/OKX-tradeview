from django.db import models
from django.contrib.auth.models import User as AuthUser, AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_photo = models.ImageField(upload_to='product_photos/')  # 假设你已经设置了媒体文件存储
    product_description = models.TextField()
    product_quantity = models.IntegerField()

    def __str__(self):
        return self.product_name

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(models.Model):
    # 如果使用Django内置的用户认证系统，则可以继承AuthUser
    # 否则，可以定义自己的用户模型
    class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.password = make_password(self.password)  # 确保在创建时加密密码
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.nickname

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    created_time = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f"Order {self.order_id}"