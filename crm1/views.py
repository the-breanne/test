from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.db.models import Sum
from _decimal import Decimal

from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse


import csv

from django.http import HttpResponse


now = timezone.now()
def home(request):
   return render(request, 'crm1/home.html',
                 {'crm1': home})


def login(request):
   return render(request, 'crm1/templates/registration/login.html',
                 {'crm1': login})

@login_required
def customer_list(request):
    customer = Customer.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm1/customer_list.html',
                 {'customers': customer})


def contact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email_address']
            subject = "Hi from Dog Bites"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'arturounotest@gmail.com', [email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("crm1:home")

    form = ContactForm()
    return render(request, "crm1/contact.html", {'form': form})



@login_required
def customer_edit(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   if request.method == "POST":
       # update
       form = CustomerForm(request.POST, instance=customer)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.updated_date = timezone.now()
           customer.save()
           customer = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm1/customer_list.html',
                         {'customers': customer})
   else:
        # edit
       form = CustomerForm(instance=customer)
   return render(request, 'crm1/customer_edit.html', {'form': form})

@login_required
def customer_delete(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   customer.delete()
   return redirect('crm1:customer_list')




@login_required
def prod(request):
   products = Product.objects.filter(created_date__lte=timezone.now())
   return render(request, 'crm1/prod.html', {'products': products})



@login_required
def product_new(request):
   if request.method == "POST":
       form = ProductForm(request.POST)
       if form.is_valid():
           product = form.save(commit=False)
           product.created_date = timezone.now()
           product.save()
           products = Product.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm1/prod.html',
                         {'products': products})
   else:
       form = ProductForm()
       # print("Else")
   return render(request, 'crm1/product_new.html', {'form': form})


@login_required
def product_edit(request, pk):
   if request.method == "POST":
       form = ProductForm(request.POST, instance=product)
       if form.is_valid():
           product = form.save()
           product.updated_date = timezone.now()
           product.save()
           products = Product.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm1/prod.html', {'products': products})
   else:
       # print("else")
       form = ProductForm(instance=product)
   return render(request, 'crm1/product_edit.html', {'form': form})


@login_required
def product_delete(request, pk):
   product = get_object_or_404(Product, pk=pk)
   product.delete()
   return redirect('crm1:product_list')


@login_required
def summary(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    products = Product.objects.filter(cust_name=pk)
    sum_product_charge = \
        Product.objects.filter(cust_name=pk).aggregate(Sum('charge'))


    return render(request, 'crm1/summary.html', {'customer': customer,
                              'products': products,
                              'sum_product_charge': sum_product_charge,})


@login_required
def export_customers(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'

    writer = csv.writer(response)
    writer.writerow(['cust_name', 'organization', 'role', 'email', 'phone_number', 'bldgroom', 'account_number', 'address', 'city', 'state', 'zipcode'])

    customers = Customer.objects.all().values_list('cust_name', 'organization', 'role', 'email', 'phone_number', 'bldgroom', 'account_number', 'address', 'city', 'state', 'zipcode')
    for customer in customers:
        writer.writerow(customer)

    return response
from django.shortcuts import render

# Create your views here.

