import datetime
import random

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import Address, CustomerAccount
from payment.models import Currency


def generateReferenceNumber():
    return random.randint(1000000000, 9999999999)


class IconTbl(models.Model):
    name = models.CharField(max_length=2048, blank=True, null=True)
    file = models.ImageField(upload_to='icons')
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class UtilityMarket(models.Model):
    internalKey = models.CharField(max_length=2048, blank=True, null=True)  # GAS / ELECTRICITY / WATER
    languageKey = models.CharField(max_length=2048, blank=True, null=True)
    iconTbl = models.ForeignKey(IconTbl, on_delete=models.PROTECT)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class MeterPoint(models.Model):
    utilityMarket = models.ForeignKey(UtilityMarket, on_delete=models.PROTECT)
    identifier = models.BigIntegerField(max_length=10, editable=False, unique=True, default=generateReferenceNumber)
    lastPublishDttm = models.DateTimeField()
    nextPublishDttm = models.DateTimeField()
    address = models.ForeignKey(Address, on_delete=models.SET_NULL)
    customerAccount = models.ForeignKey(CustomerAccount, on_delete=models.PROTECT)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class BillingCycle(models.Model):
    name = models.CharField(max_length=2048, blank=True, null=True)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class BillPeriod(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', _('Open')
        CLOSED = 'CLOSED', _('Closed')

    customerAccount = models.ForeignKey(CustomerAccount, on_delete=models.PROTECT)
    status = models.CharField(choices=Status.choices, default=Status.OPEN)
    fromDttm = models.DateTimeField()
    toDttm = models.DateTimeField()
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class Bill(models.Model):
    class Status(models.TextChoices):
        ACCEPTED = 'ACCEPTED', _('Accepted')
        DRAFT = 'DRAFT', _('Draft')
        READY_FOR_ACCEPTANCE = 'READY_FOR_ACCEPTANCE', _('Ready For Acceptance')
        ACCEPTANCE_PENDING = 'ACCEPTANCE_PENDING', _('Acceptance Pending')

    customerAccount = models.ForeignKey(CustomerAccount, on_delete=models.PROTECT)
    billPeriod = models.ForeignKey(BillPeriod, on_delete=models.PROTECT)
    billedFromDttm = models.DateTimeField()
    billedToDttm = models.DateTimeField()
    number = models.BigIntegerField(max_length=10, editable=False, unique=True, default=generateReferenceNumber)
    description = models.TextField()
    versionNumber = models.IntegerField()
    createdDttm = models.DateTimeField(auto_now_add=True)
    createdUser = models.ForeignKey(User, on_delete=models.SET_NULL)
    issueDt = models.DateField()
    dueDt = models.DateField()
    netAmount = models.DecimalField()
    grossAmount = models.DecimalField()
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    salesTaxAmount = models.DecimalField()
    status = models.CharField(choices=Status.choices, default=Status.DRAFT)
    acceptedDttm = models.DateTimeField()
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class MeterReading(models.Model):
    meterPoint = models.ForeignKey(MeterPoint, on_delete=models.PROTECT)
    value = models.FloatField()
    fromDttm = models.DateTimeField(default=datetime.date.today)
    toDttm = models.DateTimeField(default=datetime.datetime.max)
    createdDttm = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)
