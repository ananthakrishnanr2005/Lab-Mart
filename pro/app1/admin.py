from django.contrib import admin
from django.contrib.auth.models import User

from.models import *

# Register your models here.
admin.site.register(Person)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Feedback)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
