from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import IssuedInvoice, ReceivedInvoice, Transaction


@receiver(post_save, sender=IssuedInvoice)
def create_transaction_for_issued_invoice(sender, instance, **kwargs):
    if instance.status == 'PA':
        subtotal = instance.calculate_subtotal()
        vat_amount = instance.calculate_vat_amount()
        total = instance.calculate_total()

        Transaction.objects.update_or_create(
            issued_invoice=instance,
            defaults={
                'transaction_type': 'IN',
                'company_id': instance.client.company_id if instance.client else '',
                'amount_without_vat': subtotal,
                'vat_amount': vat_amount,
                'total_amount': total,
                'currency': instance.currency,
                'date': instance.updated_at.date(),
            }
        )


@receiver(post_save, sender=ReceivedInvoice)
def create_transaction_for_received_invoice(sender, instance, **kwargs):
    if instance.status == 'PA':
        subtotal = instance.subtotal()
        vat_amount = instance.vat_amount or 0
        total = instance.amount

        Transaction.objects.update_or_create(
            received_invoice=instance,
            defaults={
                'transaction_type': 'EX',
                'company_id': instance.company_id,
                'amount_without_vat': -subtotal,
                'vat_amount': -vat_amount,
                'total_amount': -total,
                'currency': instance.currency,
                'date': instance.updated_at.date(),
            }
        )
