from django.db import models

# Create your models here.
class Person(models.Model):
    Name=models.CharField(max_length=20)
    email=models.EmailField()
    pho_no=models.IntegerField()
    username=models.TextField(max_length=20, unique=True)
    password=models.TextField(max_length=128)
    Image = models.ImageField(upload_to='users/', blank=True, null=True)

    def __str__(self):
        return self.username

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user_details=models.ForeignKey(Person,on_delete=models.CASCADE)
    product_details= models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    total_price=models.IntegerField(null=True)

class Wishlist(models.Model):
    user_details=models.ForeignKey(Person,on_delete=models.CASCADE)
    product_details=models.ForeignKey(Product,on_delete=models.CASCADE)

class Feedback(models.Model):
    user_details = models.ForeignKey(Person, on_delete=models.CASCADE)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user_details.username} - {self.submitted_at.strftime('%Y-%m-%d')}"

class Order(models.Model):
    user = models.ForeignKey('Person', on_delete=models.CASCADE)
    address = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Paid', 'Paid'),
            ('Processing', 'Processing'),
            ('Shipped', 'Shipped'),
            ('On the way', 'On the Way'),
            ('Delivered', 'Delivered'),
        ],
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot of product price

    def total_price(self):
        return self.price * self.quantity


class Payment(models.Model):
    order = models.OneToOneField('Order', on_delete=models.CASCADE, related_name='payment')
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('created', 'Created'), ('successful', 'Successful'), ('failed', 'Failed')],
        default='created'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.status}"

class PasswordReset(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)









