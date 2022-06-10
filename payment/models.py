import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomerAccount
from energy.models import IconTbl


class PaymentMethodType(models.Model):
    # For example Direct Debit, Credit/Debit Card, Cheque, Cash, Direct Bank Transfer
    internalKey = models.CharField(max_length=2048, blank=True, null=True)
    languageKey = models.CharField(max_length=2048, blank=True, null=True)
    iconTbl = models.ForeignKey(IconTbl, on_delete=models.PROTECT)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class PaymentMethod(models.Model):
    # An existing method of payment against an Account

    class PaymentMethodStatus(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        ACTIVE = 'ACTIVE', _('Active')
        CANCELLED = 'CANCELLED', _('Cancelled')
        FAILED = 'FAILED', _('Failed')
        REQUESTING_ACTIVATION = 'REQUESTING_ACTIVATION', _('RequestingActivation')
        PENDING_CANCELLATION = 'PENDING_CANCELLATION', _('PendingCancellation')
        REQUESTING_CANCELLATION = 'REQUESTING_CANCELLATION', _('RequestingCancellation')
        FAILED_CANCELLATION = 'FAILED_CANCELLATION', _('FailedCancellation')
        PAUSED = 'PAUSED', _('Paused')
        COOLING_OFF = 'COOLING_OFF', _('CoolingOff')

    paymentMethodType = models.ForeignKey(PaymentMethodType, on_delete=models.PROTECT)
    customerAccount = models.ForeignKey(CustomerAccount, on_delete=models.PROTECT)
    paymentMethodStatus = models.CharField(choices=PaymentMethodStatus.choices, default=PaymentMethodStatus.PENDING)
    fromDttm = models.DateTimeField(default=datetime.date.today)
    toDttm = models.DateTimeField(default=datetime.datetime.max)
    createdDttm = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class DirectDebit(models.Model):
    paymentMethod = models.ForeignKey(PaymentMethodType, on_delete=models.PROTECT)
    sortCode = models.CharField(max_length=2048, blank=True, null=True)
    accountNo = models.PositiveBigIntegerField()
    accountName = models.CharField(max_length=2048, blank=True, null=True)
    referenceNumber = models.CharField(max_length=2048, blank=True, null=True)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class Cheque(models.Model):
    paymentMethod = models.ForeignKey(PaymentMethodType, on_delete=models.PROTECT)
    chequeNo = models.IntegerField()
    sortCode = models.CharField(max_length=2048, blank=True, null=True)
    accountNo = models.PositiveBigIntegerField()
    issueDt = models.DateField()
    referenceNumber = models.CharField(max_length=2048, blank=True, null=True)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class Payment(models.Model):
    pass


class PaymentMethodEvent(models.Model):
    pass


class AccountTransaction(models.Model):
    pass


class Charges(models.Model):
    customerAccount = models.ForeignKey(CustomerAccount, on_delete=models.PROTECT)
    standingCharge = models.DecimalField()
    unitRate = models.DecimalField()


class Currency(models.Model):
    internalKey = models.CharField(max_length=2048)
    languageKey = models.CharField(max_length=2048)
    isoCode = models.CharField(max_length=2048)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)
