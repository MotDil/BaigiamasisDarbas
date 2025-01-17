from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from django.db.models import CharField


class Category(models.Model):
    name = models.CharField('Product or service category', max_length=500)
    cover = models.ImageField('Cover image', upload_to='covers', blank=True, null=True)

    def __str__(self):
        return self.name


class ProductOrService(models.Model):
    name = models.CharField('Product or service name', max_length=255)
    description = models.TextField('Product or service description', max_length=500, blank=True)
    price = models.DecimalField('Price', max_digits=100, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField('Company or person name', max_length=255)
    company_id = models.CharField('Company id', max_length=20, blank=True)
    vat_number = models.CharField('VAT payer number', max_length=20, blank=True)
    email = models.EmailField('Email adress', max_length=50, blank=True)
    phone = models.CharField('Phone number', max_length=20, blank=True)
    address = models.CharField('Adress', max_length=255)

    def __str__(self):
        return self.name


class IssuedInvoice(models.Model):
    STATUS_CHOICES = [
        ('PA', 'Paid'),
        ('PE', 'Pending'),
        ('OV', 'Overdue'),
        ('CA', 'Cancelled')
    ]
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    invoice_number = models.CharField('Invoice Number', max_length=100, unique=True)
    date = models.DateField(verbose_name='Invoice issue date')
    due_date = models.DateField(verbose_name='Invoice payment due date')
    status = models.CharField('Invoice status', max_length=20, choices=STATUS_CHOICES, default='PE')
    apply_vat = models.BooleanField('Apply VAT', default=False)
    vat_rate = models.DecimalField('VAT amount (%)', max_digits=5, decimal_places=2, default=21.00)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    currency = models.CharField('Currency', max_length=3, default='EUR')

    def clean(self):
        if self.apply_vat == True and self.vat_rate <= 0:
            raise ValidationError("VAT rate must be positive if VAT is applied.")
        if self.due_date < self.date:
            raise ValidationError("Due date cannot be earlier than the invoice date.")

    def calculate_subtotal(self):
        return sum(line.line_total() for line in self.lines.all())

    def calculate_vat_amount(self):
        if self.apply_vat:
            return self.calculate_subtotal() * (self.vat_rate / 100)
        return 0

    def calculate_total(self):
        subtotal = self.calculate_subtotal()
        vat_amount = self.calculate_vat_amount()
        return subtotal + vat_amount

    def __str__(self):
        return f"Invoice #{self.id} - {self.client.name}"


class IssuedInvoiceLine(models.Model):
    invoice = models.ForeignKey(IssuedInvoice, related_name='lines', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductOrService, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Enter quantity of the products or services')
    price = models.DecimalField('Price (leave blank to use product price)', max_digits=10,
                                decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def line_total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"


class ReceivedInvoice(models.Model):
    STATUS_CHOICES = [
        ('PA', 'Paid'),
        ('PE', 'Pending'),
        ('OV', 'Overdue'),
        ('CA', 'Cancelled'),
    ]
    invoice_number = models.CharField('Invoice number', max_length=100, unique=True)
    supplier = models.CharField('Supplier name', max_length=255)
    company_id = models.CharField('Company id', max_length=20, blank=True)
    vat_number = models.CharField('VAT payer number', max_length=20, blank=True)
    email = models.EmailField('Email adress', max_length=50, blank=True)
    phone = models.CharField('Phone number', max_length=20, blank=True)
    bank_account = CharField('Bank account', max_length=50, blank=True)
    issue_date = models.DateField(verbose_name='Invoice issue Date', blank=True, null=True)
    due_date = models.DateField(verbose_name='Invoice payment due date', blank=True, null=True)
    amount = models.DecimalField('Amount without VAT', max_digits=10, decimal_places=2)
    apply_vat = models.BooleanField('Apply VAT', default=False)
    vat_amount = models.DecimalField('VAT amount', max_digits=10, decimal_places=2, blank=True, null=True)
    vat_rate = models.DecimalField('VAT Rate (%)', max_digits=5, decimal_places=2, default=21.00)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='PE')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Uploaded By')
    pdf_file = models.FileField('PDF Invoice', upload_to='received_invoices/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    currency = models.CharField('Currency', max_length=3, default='EUR')

    def clean(self):
        if self.due_date and self.issue_date and self.due_date < self.issue_date:
            raise ValidationError("Due date cannot be earlier than the issue date.")

    def is_overdue(self):
        if not self.due_date or self.status != 'PE':
            return False
        return self.due_date < date.today()

    def subtotal(self):
        return self.amount

    def total(self):
        return self.amount + (self.vat_amount or 0)

    def save(self, *args, **kwargs):
        if self.apply_vat:
            self.vat_amount = self.amount * (self.vat_rate / 100)
        else:
            self.vat_amount = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Received Invoice #{self.invoice_number} - {self.supplier} - {self.amount:.2f} €"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Income'),
        ('EX', 'Expense'),
    ]

    transaction_type = models.CharField('Transaction type', max_length=10, choices=TRANSACTION_TYPES)
    issued_invoice = models.ForeignKey(IssuedInvoice, on_delete=models.SET_NULL, null=True, blank=True, )
    received_invoice = models.ForeignKey(ReceivedInvoice, on_delete=models.SET_NULL, null=True, blank=True, )
    company_id = models.CharField('Company ID', max_length=20, blank=True)
    amount_without_vat = models.DecimalField('Amount without VAT', max_digits=10,
                                             decimal_places=2, blank=True, null=True)
    vat_amount = models.DecimalField('VAT amount', max_digits=10, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField('Total amount (with VAT)', max_digits=10, decimal_places=2)
    currency = models.CharField('Currency', max_length=3, default='EUR')
    date = models.DateField('Transaction date', auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
