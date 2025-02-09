# Generated by Django 5.1.4 on 2025-01-14 17:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apskaitininkas', '0003_invoice_created_at_invoice_updated_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('INCOME', 'Income'), ('EXPENSE', 'Expense')], max_length=10, verbose_name='Transaction type')),
                ('invoice_number', models.CharField(max_length=100, verbose_name='Invoice number')),
                ('related_company_id', models.CharField(blank=True, max_length=20, verbose_name='Company ID')),
                ('related_party', models.CharField(max_length=255, verbose_name='Payer/Payee')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Transaction amount')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Transaction date')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='receivedinvoice',
            name='bank_account',
            field=models.CharField(blank=True, max_length=50, verbose_name='Bank account'),
        ),
        migrations.AddField(
            model_name='receivedinvoice',
            name='company_id',
            field=models.CharField(blank=True, max_length=20, verbose_name='Company id'),
        ),
        migrations.AddField(
            model_name='receivedinvoice',
            name='currency',
            field=models.CharField(default='EUR', max_length=3, verbose_name='Currency'),
        ),
        migrations.AddField(
            model_name='receivedinvoice',
            name='email',
            field=models.EmailField(blank=True, max_length=50, verbose_name='Email adress'),
        ),
        migrations.AddField(
            model_name='receivedinvoice',
            name='phone',
            field=models.CharField(blank=True, max_length=20, verbose_name='Phone number'),
        ),
        migrations.AddField(
            model_name='receivedinvoice',
            name='vat_number',
            field=models.CharField(blank=True, max_length=20, verbose_name='VAT payer number'),
        ),
        migrations.AddField(
            model_name='receivedinvoice',
            name='vat_rate',
            field=models.DecimalField(decimal_places=2, default=21.0, max_digits=5, verbose_name='VAT Rate (%)'),
        ),
        migrations.AlterField(
            model_name='client',
            name='vat_number',
            field=models.CharField(blank=True, max_length=20, verbose_name='VAT payer number'),
        ),
        migrations.AlterField(
            model_name='receivedinvoice',
            name='due_date',
            field=models.DateField(blank=True, null=True, verbose_name='Invoice payment due date'),
        ),
        migrations.AlterField(
            model_name='receivedinvoice',
            name='issue_date',
            field=models.DateField(blank=True, null=True, verbose_name='Invoice issue Date'),
        ),
        migrations.RenameModel(
            old_name='InvoiceLine',
            new_name='IssuedInvoiceLine',
        ),
        migrations.CreateModel(
            name='IssuedInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=100, unique=True, verbose_name='Invoice Number')),
                ('date', models.DateField(verbose_name='Invoice issue date')),
                ('due_date', models.DateField(verbose_name='Invoice payment due date')),
                ('status', models.CharField(choices=[('PA', 'Paid'), ('PE', 'Pending'), ('OV', 'Overdue'), ('CA', 'Cancelled')], default='PE', max_length=20, verbose_name='Invoice status')),
                ('apply_vat', models.BooleanField(default=False, verbose_name='Apply VAT')),
                ('vat_rate', models.DecimalField(decimal_places=2, default=21.0, max_digits=5, verbose_name='VAT amount (%)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('currency', models.CharField(default='EUR', max_length=3, verbose_name='Currency')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='apskaitininkas.client')),
                ('issued_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='issuedinvoiceline',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='apskaitininkas.issuedinvoice'),
        ),
        migrations.DeleteModel(
            name='Invoice',
        ),
    ]
