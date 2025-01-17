from django.contrib import admin
from .models import Category, ProductOrService, Client, IssuedInvoice, IssuedInvoiceLine, ReceivedInvoice, Transaction


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ProductOrServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_id', 'vat_number', 'email', 'phone', 'address')
    search_fields = ('name', 'company_id', 'vat_number', 'email', 'phone', 'address')


class IssuedInvoiceLineInline(admin.TabularInline):
    model = IssuedInvoiceLine
    extra = 1
    fields = ('product', 'quantity', 'price')


class IssuedInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'client', 'date', 'due_date', 'status', 'apply_vat', 'vat_rate',
        'issued_by', 'subtotal', 'vat_amount', 'total'
    )
    list_filter = ('status', 'apply_vat', 'issued_by', 'date', 'due_date')
    search_fields = ('client__name', 'client__email', 'status')
    readonly_fields = ('calculate_subtotal', 'calculate_vat_amount', 'calculate_total')
    inlines = [IssuedInvoiceLineInline]

    def subtotal(self, obj):
        return f"{obj.calculate_subtotal():.2f} €"

    subtotal.short_description = 'Subtotal (no VAT)'

    def vat_amount(self, obj):
        return f"{obj.calculate_vat_amount():.2f} €"

    vat_amount.short_description = 'VAT Amount'

    def total(self, obj):
        return f"{obj.calculate_total():.2f} €"

    total.short_description = 'Total (with VAT)'


class IssuedInvoiceLineAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'product', 'quantity', 'price', 'line_total')
    list_filter = ('invoice', 'product')
    search_fields = ('product__name',)

    def line_total(self, obj):
        return f"{obj.line_total():.2f} €"

    line_total.short_description = 'Line Total'


class ReceivedInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_number', 'supplier', 'issue_date', 'due_date',
        'amount', 'vat_amount', 'status', 'uploaded_by', 'is_overdue'
    )
    list_filter = ('status', 'supplier', 'issue_date', 'due_date')
    search_fields = ('invoice_number', 'supplier')
    readonly_fields = ('is_overdue',)

    def is_overdue(self, obj):
        return obj.is_overdue()

    is_overdue.short_description = 'Overdue'
    is_overdue.boolean = True


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_type', 'date', 'issued_invoice', 'received_invoice',
        'amount_without_vat', 'vat_amount', 'total_amount', 'currency', 'company_id'
    )
    list_filter = ('transaction_type', 'date', 'currency',)
    search_fields = ('issued_invoice__invoice_number', 'received_invoice__invoice_number', 'company_id')
    readonly_fields = ('transaction_type', 'date', 'issued_invoice', 'received_invoice', 'amount_without_vat',
                       'vat_amount', 'total_amount', 'currency', 'company_id', 'created_at', 'updated_at')


admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductOrService, ProductOrServiceAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(IssuedInvoice, IssuedInvoiceAdmin)
admin.site.register(IssuedInvoiceLine, IssuedInvoiceLineAdmin)
admin.site.register(ReceivedInvoice, ReceivedInvoiceAdmin)
admin.site.register(Transaction, TransactionAdmin)
