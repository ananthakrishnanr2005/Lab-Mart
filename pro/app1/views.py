from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import *
from django.http import HttpResponse
from .form import *
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
import razorpay

def loading(request):
    return render(request, "loading.html")

def index(request):
    return render(request, "index.html")

def userhome(request):
    return render(request, "userhome.html")

def adminhome(request):
    return render(request, "adminhome.html")

def about(request):
    return render(request, "about.html")

def register(request):
    if request.method == 'POST':
        a = request.POST.get('name')
        b = request.POST.get('email')
        c = request.POST.get('pho_no')
        d = request.POST.get('username')
        e = request.POST.get('password')
        f = request.FILES.get('Image')

        if Person.objects.filter(username=d).exists():
            messages.error(request, "Username already taken. Please choose another.")
            return redirect(register)

        data = Person.objects.create(
            Name=a,
            email=b,
            pho_no=c,
            username=d,
            password=e,
            Image=f
        )
        return redirect(login)
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Try to find user in Person model
            data = Person.objects.get(username=username)
            if data.password == password:
                request.session['uname'] = data.username   # use consistent session key
                return redirect('userhome')  # use URL name
            else:
                return HttpResponse('Login Failed')
        except Person.DoesNotExist:
            # Handle admin login separately
            if username == 'admin' and password == '1234':
                request.session['uname'] = 'admin'
                return redirect('adminhome')
            else:
                return HttpResponse('Login Failed')

    return render(request, 'login.html')

def viewuser(request):
    data = Person.objects.all()
    return render(request, 'viewuser.html', {'Person': data})

def deleteuser(request,id):
    data=Person.objects.get(pk=id)
    data.delete()
    return redirect(viewuser)

def addproduct(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        image = request.FILES.get("image")

        product = Product(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            image=image
        )
        product.save()
        messages.success(request, "Product added successfully!")
        return redirect(viewproduct)

    return render(request, "addproduct.html")

def viewproduct(request):
    products = Product.objects.all().order_by("-created_at")
    return render(request, "viewproduct.html", {"products": products})

def updateproduct(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect(viewproduct)
    else:
        form = ProductForm(instance=product)

    return render(request, "updateproduct.html", {"form": form})

def deleteproduct(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return redirect(viewproduct)

def orderdetails(request):
    return render(request,'orderdetails.html')

def logout(request):
    if 'uname' in request.session:
        request.session.flush()
    return redirect(index)

def userabout(request):
    return render(request, "userabout.html")

def userprofile(request):
    if 'uname' not in request.session:
        return HttpResponse("Please login first")
    try:
        user = Person.objects.get(username=request.session['uname'])
    except Person.DoesNotExist:
        return HttpResponse("User not found")
    return render(request, 'userprofile.html', {'Person': [user]})

def updateprofile(request, id):
    person = get_object_or_404(Person, id=id)
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            return redirect('userprofile')
    else:
        form = PersonForm(instance=person)

    return render(request, 'updateprofile.html', {'form': form})

def viewuserdetails(request, id):
    person = get_object_or_404(Person, id=id)
    return render(request, 'viewuserdetails.html', {'Person': [person]})

def shop(request):
    products = Product.objects.all().order_by("-created_at")
    return render(request, "shop.html", {"products": products})


def addtowishlist(request, pid):
    if 'uname' not in request.session:
        return HttpResponse("Please Login")

    username = request.session['uname']
    user = get_object_or_404(Person, username=username)
    prod = get_object_or_404(Product, id=pid)

    # Check if product already exists in wishlist
    if Wishlist.objects.filter(user_details=user, product_details=prod).exists():
        messages.success(request, "Already in Wishlist")
        return redirect(shop)
    else:
        Wishlist.objects.create(
            user_details=user,
            product_details=prod
        )
        messages.success(request, "Added to Wishlist")
        return redirect(shop)

def wishlist(request):
    if 'uname' not in request.session:
        return HttpResponse("Please login first")
    user = Person.objects.get(username=request.session['uname'])

    items = Wishlist.objects.filter(user_details=user)

    return render(request, 'wishlist.html', {'items': items})

def removefromwishlist(request, wid):
    if 'uname' not in request.session:
        return HttpResponse("Please login first")

    user = get_object_or_404(Person, username=request.session['uname'])
    # Get the wishlist item belonging to this user
    wishlist_item = get_object_or_404(Wishlist, id=wid, user_details=user)

    # Delete the item
    wishlist_item.delete()
    messages.success(request, "Item removed from Wishlist")

    # Redirect back to wishlist page
    return redirect(wishlist)

def movetocart(request, wid):
    if 'uname' not in request.session:
        return HttpResponse("Please login first")

    user = get_object_or_404(Person, username=request.session['uname'])
    # Get the wishlist item
    wish_item = get_object_or_404(Wishlist, id=wid, user_details=user)
    product = wish_item.product_details

    # Check if product already exists in cart
    if Cart.objects.filter(user_details=user, product_details=product).exists():
        messages.success(request, "Already in Cart")
    else:
        Cart.objects.create(
            user_details=user,
            product_details=product,
            quantity=1  # default quantity
        )
        messages.success(request, "Moved to Cart")

    # Remove from wishlist
    wish_item.delete()

    return redirect('wishlist')


def addtocart(request,pid):
    if 'uname' not in request.session:
        return HttpResponse("Please Login")
    username=request.session['uname']
    user=Person.objects.get(username=username)
    prod=Product.objects.get(id=pid)

    try:
        item=Cart.objects.get(user_details=user,product_details=prod)
        item.quantity+=1
        item.total_price=item.quantity*prod.price
        item.save()
    except Cart.DoesNotExist:
        Cart.objects.create(
            user_details=user,
            product_details=prod,
            quantity=1,
            total_price=prod.price
        )
    messages.success(request, "Cart Added")
    return redirect(shop)

def cart(request):
    if 'uname' not in request.session:
        return HttpResponse("Please login first")
    user = Person.objects.get(username=request.session['uname'])

    items = Cart.objects.filter(user_details=user)
    total = sum(item.quantity * item.product_details.price for item in items)

    return render(request, 'cart.html', {'items': items, 'total': total})

def removefromcart(request, cid):
    if 'uname' not in request.session:
        return HttpResponse("Please login first")

    user = get_object_or_404(Person, username=request.session['uname'])
    # Get the cart item belonging to this user
    cart_item = get_object_or_404(Cart, id=cid, user_details=user)

    # Delete the item
    cart_item.delete()
    messages.success(request, "Item removed from Cart")

    # Redirect back to cart page
    return redirect(cart)

def updatecartquantity(request, cid):
    if 'uname' not in request.session:
        return HttpResponse("Please login first")

    if request.method == "POST":
        user = get_object_or_404(Person, username=request.session['uname'])
        cart_item = get_object_or_404(Cart, id=cid, user_details=user)

        try:
            new_quantity = int(request.POST.get("quantity", cart_item.quantity))
            if new_quantity > 0:
                cart_item.quantity = new_quantity
                cart_item.total_price = new_quantity * cart_item.product_details.price
                cart_item.save()
                messages.success(request, "Quantity updated successfully")
            else:
                messages.error(request, "Quantity must be at least 1")
        except ValueError:
            messages.error(request, "Invalid quantity")

    return redirect("cart")

def checkout(request):
    if 'uname' not in request.session:
        return HttpResponse("Please login first")

    user = Person.objects.get(username=request.session['uname'])
    items = Cart.objects.filter(user_details=user)

    if not items.exists():
        messages.error(request, "Your cart is empty")
        return redirect('cart')

    # Calculate total dynamically
    total = sum(item.quantity * item.product_details.price for item in items)

    # Add a computed field for each item
    for item in items:
        item.computed_total = item.quantity * item.product_details.price

    return render(request, 'checkout.html', {
        'items': items,
        'total': total,
        'user': user
    })

def addfeedback(request):
    form = FeedbackForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        feedback = form.save(commit=False)

        # Safely get logged-in user from session
        uname = request.session.get('uname')
        if not uname:
            # If session expired or user not logged in, redirect to login page
            return redirect('login')

        try:
            reg_user = Person.objects.get(username=uname)
        except Person.DoesNotExist:
            # If the user is not found in DB, force login again
            return redirect('login')

        feedback.user_details = reg_user
        feedback.save()

        # Redirect to success page (use URL name defined in urls.py)
        return redirect('addfeedback')

    return render(request, "addfeedback.html", {'form': form})

def viewfeedback(request):
    # Use select_related for efficiency, order newest first
    feedbacks = Feedback.objects.select_related('user_details').order_by('-submitted_at')
    return render(request, "viewfeedback.html", {'feedbacks': feedbacks})

def placeorder(request):
    if 'uname' not in request.session:
        return redirect('userhome')

    # Get the logged-in user instance
    username = request.session.get('uname')
    user = Person.objects.get(username=username)

    # Get all cart items for this user
    cart_items = Cart.objects.filter(user_details=user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty")
        return redirect('cart')

    # Calculate total
    total = sum(item.quantity * item.product_details.price for item in cart_items)
    total_paise = int(total * 100)  # Razorpay expects amount in paise

    if request.method == 'POST':
        address = request.POST['address']

        order = Order.objects.create(
            user=user,
            address=address,
            total=total,
            status='pending'
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product_details,
                quantity=item.quantity,
                price=item.product_details.price
            )

        client = razorpay.Client(
            auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM")
        )

        payment_data = client.order.create({
            'amount': total_paise,
            'currency': 'INR',
            'payment_capture': '1'
        })

        Payment.objects.create(
            order=order,
            razorpay_order_id=payment_data['id'],
            status='created'
        )

        return render(request, 'paynow.html', {
            'payment': payment_data,
            'user': user,
            'products': [item.product_details for item in cart_items],
            'cart_items': cart_items,
            'total': total,
        })

    return redirect('checkout')

def ordersuccess(request):
    if request.method != 'POST':
        return HttpResponse("Invalid request")

    # Razorpay sends form data, not JSON
    razorpay_order_id = request.POST.get('razorpay_order_id')
    razorpay_payment_id = request.POST.get('razorpay_payment_id')
    razorpay_signature = request.POST.get('razorpay_signature')

    if not (razorpay_order_id and razorpay_payment_id and razorpay_signature):
        return HttpResponse("Missing payment details")

    payment = get_object_or_404(Payment, razorpay_order_id=razorpay_order_id)
    order = payment.order

    client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })

        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature = razorpay_signature
        payment.status = 'successful'
        payment.save()

        order.status = 'paid'
        order.save()

        Cart.objects.filter(user_details=order.user).delete()

        return render(request, 'ordersuccess.html', {
            'user': order.user,
            'address': order.address,
            'total': order.total,
            'items': order.items.all()
        })

    except razorpay.errors.SignatureVerificationError:
        payment.status = 'failed'
        payment.save()
        order.status = 'failed'
        order.save()
        return HttpResponse("Payment verification failed")


def myorders(request):
    if 'uname' not in request.session:
        return HttpResponse("Please login first")

    # Get the logged-in user from session
    try:
        user = Person.objects.get(username=request.session['uname'])
    except Person.DoesNotExist:
        return HttpResponse("User not found")

    # Fetch orders belonging to this user
    orders = Order.objects.filter(user=user).order_by('-created_at')

    return render(request, "myorders.html", {"orders": orders})

def userorderdetails(request, order_id):
    # Ensure user is logged in
    if 'uname' not in request.session:
        return redirect(userhome)

    # Get logged-in user instance
    username = request.session.get('uname')
    user = get_object_or_404(Person, username=username)

    # Get order belonging to this user
    order = get_object_or_404(Order, id=order_id, user=user)

    return render(request, 'userorderdetails.html', {
        'order': order,
        'items': order.items.all(),   # product name, price, quantity
    })

def orderdetails(request):
    orders = Order.objects.all()
    return render(request, "orderdetails.html", {"orders": orders})

def updateorderstatus(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status:
            order.status = new_status
            order.save()
            return redirect(orderdetails)

    return render(request, "updateorderstatus.html", {"order": order})

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Person.objects.get(email=email)
        except Person.DoesNotExist:
            messages.info(request, "Email id not registered")
            return redirect(forgotpassword)

        # Generate secure token
        token = get_random_string(length=32)
        PasswordReset.objects.create(user=user, token=token)

        # Send email
        reset_link = f'http://127.0.0.1:8000/resetpassword/{token}'
        try:
            send_mail(
                'Reset Your Password',
                f'Click the link to reset your password: {reset_link}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )

            messages.success(request, "Password reset link sent to your email")
        except Exception as e:
            messages.error(request, "Network connection failed")
            return redirect(forgotpassword)

    return render(request, 'forgot.html')


def resetpassword(request, token):
    try:
        password_reset = PasswordReset.objects.get(token=token)
    except PasswordReset.DoesNotExist:
        messages.error(request, "Invalid or expired token")
        return redirect(forgotpassword)

    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')

        if new_password == repeat_password:
            password_reset.user.password = make_password(new_password)
            password_reset.user.save()
            password_reset.delete()
            messages.success(request, "Password reset successful. Please login.")
            return redirect(login)
        else:
            messages.error(request, "Passwords do not match")

    return render(request, 'reset.html', {'token': token})












