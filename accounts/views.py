from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from cart.models import Order, Item
from django.db.models import Sum, Count
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})

@staff_member_required
def admin_dashboard(request):

    users = User.objects.filter(is_staff=False).annotate(
        total_movies_purchased = Sum('order__item__quantity'),
        total_orders = Count('order', distinct=True),
        total_spent = Sum('order__total')
    ).order_by('-total_movies_purchased')

    top_user = users.first()

    commenters = User.objects.filter(is_staff=False).annotate(
        total_comments = Count('review', distinct=True)
    ).order_by('-total_comments')

    top_commenter = commenters.first()

    template_data = {
        'title': 'Admin Dashboard',
        'users': users,
        'top_user': top_user,
        'top_user_count': top_user.total_movies_purchased,
        'commenters': commenters,
        'top_commenter': top_commenter,
        'top_commenter_count': top_commenter.total_comments
    }

    return render(request, 'accounts/admin_dashboard.html', {'template_data': template_data})
