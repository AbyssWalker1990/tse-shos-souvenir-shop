from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm
from .models import Profile
from goods.models import OrderProduct, OrderCard
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.


def login_user(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('goods')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Користувача не існує')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('goods')
        else:
            messages.error(request, 'Логін або пароль введені неправильно')
    return render(request, 'userprofile/login_register.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()
    error = ''

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(form.errors.as_data())

        if form.errors:
            error = form.errors.as_data()

        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            messages.success(request, 'Акаунт користувача створено!')

            login(request, user)
            pk = user.profile.id

            return redirect('profile', pk)

    context = {'page': page, 'form': form, 'error': error}
    return render(request, 'userprofile/register_form.html', context)


@login_required(login_url='login')
def profile(request, pk):
    user_id = Profile.objects.get(id=pk)
    context = {'user_id': user_id}
    return render(request, 'userprofile/profile.html', context)


@login_required(login_url='login')
def edit_account(request, pk):
    user_profile = request.user.profile
    form = ProfileForm(instance=user_profile)
    pk = user_profile.id

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.save()

            return redirect('profile', pk)

    context = {'form': form, 'user_profile': user_profile}
    return render(request, 'userprofile/edit_account.html', context)


def bucket(request, pk):
    user_id = Profile.objects.get(id=pk)
    user_profile = request.user.profile
    order_cards = OrderCard.objects.all().filter(client=user_profile)
    order_products = OrderProduct.objects.all().filter(client=user_profile, status="PROCESSING")
    total_sum = sum([i.total_price for i in order_products])
    context = {'user_id': user_id,
               'order_products': order_products,
               'total_sum': total_sum,
               'order_cards': order_cards,
               }
    return render(request, 'userprofile/bucket.html', context)



def _get_session_id(request):
    current_session = request.session.session_key
    if not current_session:
        current_session = request.session.create()
    return current_session


def non_user_bucket(request):
    try:
        card = OrderCard.objects.get(session_id=_get_session_id(request))
    except OrderCard.DoesNotExist:
        card = OrderCard.objects.create(
            session_id=_get_session_id(request)
        )
    products = OrderProduct.objects.all().filter(session_id=card)

    context = {'card': card,
               'products': products}

    return render(request, 'userprofile/non-user-bucket.html', context)


def delete_item(request, pk):
    product = OrderProduct.objects.get(id=pk)
    user_id = request.user.profile.id
    product.delete()
    return redirect('bucket', user_id)


def delete_item_non_user(request, pk):
    product = OrderProduct.objects.get(id=pk)
    product.delete()
    return redirect('non-user-bucket')

def increase_item(request, pk):
    product = OrderProduct.objects.get(id=pk)
    user_id = request.user.profile.id
    product.count += 1
    product.save()
    return redirect('bucket', user_id)


def increase_item_non_user(request, pk):
    product = OrderProduct.objects.get(id=pk)
    product.count += 1
    product.save()
    return redirect('non-user-bucket')



def decrease_item(request, pk):
    product = OrderProduct.objects.get(id=pk)
    user_id = request.user.profile.id

    product.count -= 1
    if product.count < 0:
        product.count = 0
    product.save()
    return redirect('bucket', user_id)

def decrease_item_non_user(request, pk):
    product = OrderProduct.objects.get(id=pk)
    product.count -= 1
    if product.count < 0:
        product.count = 0
    product.save()
    return redirect('non-user-bucket')



