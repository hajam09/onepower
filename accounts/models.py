import datetime
import random

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from energy.models import BillingCycle
from payment.models import Currency


def generateReferenceNumber():
    return random.randint(1000000000, 9999999999)


class Country(models.Model):
    internalKey = models.CharField(max_length=2048, blank=True, null=True)
    languageKey = models.CharField(max_length=2048, blank=True, null=True)
    isoCode = models.CharField(max_length=2048, blank=True, null=True)
    dialCode = models.CharField(max_length=2048, blank=True, null=True)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class Address(models.Model):
    address1 = models.CharField(max_length=2048, blank=True, null=True)
    address2 = models.CharField(max_length=2048, blank=True, null=True)
    address3 = models.CharField(max_length=2048, blank=True, null=True)
    address4 = models.CharField(max_length=2048, blank=True, null=True)
    address5 = models.CharField(max_length=2048, blank=True, null=True)
    postcode = models.CharField(max_length=2048, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='employee')
    number = models.BigIntegerField(max_length=10, editable=False, unique=True, default=generateReferenceNumber)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL)
    createdUser = models.ForeignKey(User, on_delete=models.SET_NULL)
    terminatedUser = models.ForeignKey(User, on_delete=models.SET_NULL)
    createdDttm = models.DateTimeField(auto_now_add=True)
    fromDttm = models.DateTimeField(default=datetime.date.today)
    toDttm = models.DateTimeField(default=datetime.datetime.max)
    modifiedDttm = models.DateTimeField(auto_now=True)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class CustomerAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='customerAccounts')
    number = models.BigIntegerField(max_length=10, editable=False, unique=True, default=generateReferenceNumber)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL)
    createdDttm = models.DateTimeField(auto_now_add=True)
    createdUser = models.ForeignKey(User, on_delete=models.SET_NULL)
    fromDttm = models.DateTimeField(default=datetime.date.today)
    toDttm = models.DateTimeField(default=datetime.datetime.max)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    salesTaxExempt = models.BooleanField(default=False)
    terminatedUser = models.ForeignKey(User, on_delete=models.SET_NULL)
    companyName = models.CharField(max_length=2048, blank=True, null=True)
    companyNumber = models.BigIntegerField()
    billingCycle = models.ForeignKey(BillingCycle, on_delete=models.PROTECT)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class Company(models.Model):
    name = models.CharField(max_length=2048, blank=True, null=True)
    sortCode = models.CharField(max_length=2048, blank=True, null=True)
    accountNo = models.PositiveBigIntegerField()
    accountName = models.CharField(max_length=2048, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class Contact(models.Model):
    internalKey = models.CharField(max_length=2048, blank=True, null=True, unique=True)
    description = models.TextField()
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class ContactVersion(models.Model):
    class Title(models.TextChoices):
        DR = 'DR', _('Dr')
        MISS = 'MISS', _('Miss')
        MR = 'MR', _('Mr')
        MRS = 'MRS', _('Mrs')
        MS = 'MS', _('Ms')
        PROF = 'PROF', _('Prof')

    contact = models.ForeignKey(Contact, on_delete=models.PROTECT)
    fromDttm = models.DateTimeField(default=datetime.date.today)
    toDttm = models.DateTimeField(default=datetime.datetime.max)
    title = models.CharField(choices=Title.choices, default=Title.MR)
    initials = models.CharField(max_length=2048, blank=True, null=True)
    firstName = models.CharField(max_length=2048, blank=True, null=True)
    lastName = models.CharField(max_length=2048, blank=True, null=True)
    jobTitle = models.CharField(max_length=2048, blank=True, null=True)
    number1 = models.CharField(max_length=2048, blank=True, null=True)
    number2 = models.CharField(max_length=2048, blank=True, null=True)
    number3 = models.CharField(max_length=2048, blank=True, null=True)
    email = models.EmailField()
    webBrowser = models.CharField(max_length=2048, blank=True, null=True)
    careOf = models.CharField(max_length=2048, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)


class ComponentGroup(models.Model):
    internalKey = models.CharField(max_length=2048, blank=True, null=True, unique=True)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    languageKey = models.CharField(max_length=2048, blank=True, null=True)
    code = models.CharField(max_length=2048, blank=True, null=True)
    icon = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)

    class Meta:
        verbose_name_plural = "ComponentGroup"

    def __str__(self):
        return self.internalKey

    def getRelatedFeatureComponentByOrderNo(self):
        return self.components.all().order_by('orderNo')


class Component(models.Model):
    componentGroup = models.ForeignKey(ComponentGroup, on_delete=models.CASCADE, related_name="components")
    internalKey = models.CharField(max_length=2048, blank=True, null=True)
    reference = models.CharField(max_length=2048, blank=True, null=True)
    languageKey = models.CharField(max_length=2048, blank=True, null=True)
    code = models.CharField(max_length=2048, blank=True, null=True)
    icon = models.CharField(max_length=2048, blank=True, null=True)
    deleteFl = models.BooleanField(default=False)
    orderNo = models.IntegerField(default=1, blank=True, null=True)
    versionNo = models.IntegerField(default=1, blank=True, null=True)

    class Meta:
        ordering = ['componentGroup', 'orderNo']
        verbose_name_plural = "Component"

    def __str__(self):
        return self.internalKey
