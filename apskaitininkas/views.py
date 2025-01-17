from django.shortcuts import render, get_object_or_404, redirect
from .models import ProductOrService, Client, Category, IssuedInvoice, ReceivedInvoice, Transaction
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from .forms import IssuedInvoiceForm, ReceivedInvoiceForm, IssuedInvoiceLineFormSet
import plotly.graph_objects as go
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def invoices(request):
    return render(request, 'invoices.html')


def index(request):
    num_issuedinvoices_pen = IssuedInvoice.objects.filter(status__exact="PE").count()
    num_receivedinvoices_pen = ReceivedInvoice.objects.filter(status__exact="PE").count()
    context = {
        'num_issuedinvoices_pen': num_issuedinvoices_pen,
        'num_receivedinvoices_pen': num_receivedinvoices_pen,
    }
    return render(request, 'index.html', context=context)


def merchandise(request):
    context = {
        'merchandise': Category.objects.all()
    }
    return render(request, 'merchandise.html', context=context)


def clients(request):
    query = request.GET.get('query')
    sort = request.GET.get('sort')
    clients = Client.objects.all()

    if query:
        clients = clients.filter(
            Q(name__icontains=query) |
            Q(company_id__icontains=query) |
            Q(email__icontains=query)
        )

    if sort == 'name_asc':
        clients = clients.order_by('name')
    elif sort == 'name_desc':
        clients = clients.order_by('-name')
    elif sort == 'company_id_asc':
        clients = clients.order_by('company_id')
    elif sort == 'company_id_desc':
        clients = clients.order_by('-company_id')
    else:
        clients = clients.order_by('id')

    paginator = Paginator(clients, 10)
    page_number = request.GET.get('page')
    clients = paginator.get_page(page_number)

    context = {
        'clients': clients,
    }

    return render(request, 'clients.html', context=context)


def categories(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    query = request.GET.get('query')
    sort = request.GET.get('sort')
    products = ProductOrService.objects.filter(category=category)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query)
        )

    if sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')
    elif sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'category': category,
        'products': products,
    }

    return render(request, 'categories.html', context)


def issued_invoices(request):
    invoices = IssuedInvoice.objects.all()
    paginator = Paginator(invoices, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'issued_invoices.html', {'page_obj': page_obj})


def received_invoices(request):
    invoices = ReceivedInvoice.objects.all()
    paginator = Paginator(invoices, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'received_invoices.html', {'page_obj': page_obj})


def edit_issued_invoice(request, pk):
    invoice = get_object_or_404(IssuedInvoice, pk=pk)
    form = IssuedInvoiceForm(instance=invoice)
    formset = IssuedInvoiceLineFormSet(instance=invoice)

    if request.method == "POST":
        form = IssuedInvoiceForm(request.POST, instance=invoice)
        formset = IssuedInvoiceLineFormSet(request.POST, instance=invoice)

        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            formset.instance = invoice
            for form in formset:
                if form.cleaned_data and not all(value == "" for value in form.cleaned_data.values()):
                    form.save()
            return redirect("issued_invoices")

    context = {
        "form": form,
        "formset": formset,
        "invoice": invoice,
    }
    return render(request, "edit_issued_invoice.html", context=context)


def edit_received_invoice(request, invoice_id):
    invoice = get_object_or_404(ReceivedInvoice, id=invoice_id)
    if request.method == "POST":
        form = ReceivedInvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect('received_invoices')  # Grįžti į sąskaitų sąrašą
    else:
        form = ReceivedInvoiceForm(instance=invoice)
    return render(request, 'edit_received_invoice.html', {'form': form, 'invoice': invoice})


def create_invoice(request):
    if request.method == "POST":
        form = IssuedInvoiceForm(request.POST)
        formset = IssuedInvoiceLineFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            invoice_lines = formset.save(commit=False)
            for line in invoice_lines:
                line.invoice = invoice
                line.save()
            return redirect('issued_invoices')
    else:
        form = IssuedInvoiceForm()
        formset = IssuedInvoiceLineFormSet()
    return render(request, 'create_invoice.html', {'form': form, 'formset': formset})


def register_invoice(request):
    form = ReceivedInvoiceForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('received_invoices')

    context = {
        'form': form,
    }
    return render(request, 'register_invoice.html', context)


def transactions(request):
    transactions = Transaction.objects.all()
    context = {
        'transactions': transactions,
    }
    return render(request, 'transactions.html', context)


@login_required
def custom_login(request):
    return render(request, 'index.html')

def custom_logout(request):
    logout(request)
    return redirect('login')
