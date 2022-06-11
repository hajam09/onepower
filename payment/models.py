import datetime
import random

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomerAccount, Employee
from energy.models import IconTbl


def generateReferenceNumber():
    return random.randint(1000000000, 9999999999)


class Currency(models.Model):
    internalKey = models.CharField(max_length=2048)
    languageKey = models.CharField(max_length=2048)
    isoCode = models.CharField(max_length=2048)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


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
    paymentMethod = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    sortCode = models.CharField(max_length=2048, blank=True, null=True)
    accountNo = models.PositiveBigIntegerField()
    accountName = models.CharField(max_length=2048, blank=True, null=True)
    referenceNumber = models.CharField(max_length=2048, blank=True, null=True)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class Cheque(models.Model):
    paymentMethod = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    chequeNo = models.IntegerField()
    sortCode = models.CharField(max_length=2048, blank=True, null=True)
    accountNo = models.PositiveBigIntegerField()
    issueDt = models.DateField()
    referenceNumber = models.CharField(max_length=2048, blank=True, null=True)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class PaymentRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        REQUESTING = 'REQUESTING', _('Requesting')
        IN_PROGRESS_PENDING = 'IN_PROGRESS_PENDING', _('In Progress Pending')
        IN_PROGRESS_FAILED_PENDING_RETRY = 'IN_PROGRESS_FAILED_PENDING_RETRY', _('In Progress Failed Pending Retry')
        SUCCESSFUL = 'SUCCESSFUL', _('Successful')
        CANCELLED = 'CANCELLED', _('Cancelled')
        FAILED_PENDING_RETRY = 'FAILED_PENDING_RETRY', _('Failed Pending Retry')
        FAILED_REQUESTING_AGAIN = 'FAILED_REQUESTING_AGAIN', _('Failed Requesting Again')
        PENDING_AUTHORISATION = 'PENDING_AUTHORISATION', _('Pending Authorisation')
        PENDING_FINAL_AUTHORISATION = 'PENDING_FINAL_AUTHORISATION', _('Pending Final Authorisation')

    paymentMethodType = models.ForeignKey(PaymentMethodType, on_delete=models.PROTECT)
    requestId = models.PositiveBigIntegerField(default=generateReferenceNumber)
    transactionId = models.PositiveBigIntegerField(default=generateReferenceNumber)
    paymentMethod = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    createdUser = models.ForeignKey(Employee, on_delete=models.SET_NULL)
    createdDttm = models.DateTimeField(auto_now_add=True)
    postedDt = models.DateField()
    collectionDt = models.DateField()
    status = models.CharField(choices=Status.choices, default=Status.PENDING)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    cancelledDttm = models.DateTimeField()
    paymentCancellationReason = models.TextField(blank=True, null=True)
    amount = models.DecimalField()
    description = models.TextField(blank=True, null=True)
    payee = models.ForeignKey(CustomerAccount, on_delete=models.PROTECT)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class Payment(models.Model):
    paymentMethodType = models.ForeignKey(PaymentMethodType, on_delete=models.PROTECT)
    paymentRequest = models.ForeignKey(PaymentRequest, on_delete=models.PROTECT)
    transactionId = models.PositiveBigIntegerField(default=generateReferenceNumber)
    customerAccount = models.ForeignKey(CustomerAccount, on_delete=models.PROTECT)
    createdDttm = models.DateTimeField(auto_now_add=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    amount = models.DecimalField()
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class Charges(models.Model):
    customerAccount = models.ForeignKey(CustomerAccount, on_delete=models.PROTECT)
    standingCharge = models.DecimalField()
    unitRate = models.DecimalField()
    createdUser = models.ForeignKey(User, on_delete=models.SET_NULL)
    fromDttm = models.DateTimeField(default=datetime.date.today)
    toDttm = models.DateTimeField(default=datetime.datetime.max)
    createdDttm = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)
