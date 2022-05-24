# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Address(models.Model):
    useraddressid = models.AutoField(db_column='userAddressID', primary_key=True)  # Field name made lowercase.
    auth_user = models.ForeignKey('AuthUser', models.DO_NOTHING)
    firstname = models.CharField(db_column='firstName', max_length=45)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=45)  # Field name made lowercase.
    streetaddress = models.CharField(db_column='streetAddress', max_length=45)  # Field name made lowercase.
    city = models.CharField(max_length=45)
    zipcode = models.IntegerField(db_column='zipCode')  # Field name made lowercase.
    state = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'address'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Deliverydriver(models.Model):
    driverid = models.AutoField(db_column='driverID', primary_key=True)  # Field name made lowercase.
    driverfirstname = models.CharField(db_column='driverFirstName', max_length=45)  # Field name made lowercase.
    driverlastname = models.CharField(db_column='driverLastName', max_length=45)  # Field name made lowercase.
    carmodel = models.CharField(db_column='carModel', max_length=45)  # Field name made lowercase.
    licenseplate = models.CharField(db_column='licensePlate', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'deliveryDriver'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Groceryitem(models.Model):
    groceryid = models.AutoField(db_column='groceryID', primary_key=True)  # Field name made lowercase.
    grocerystore_storeid = models.ForeignKey('Grocerystore', models.DO_NOTHING, db_column='groceryStore_storeID')  # Field name made lowercase.
    groceryname = models.CharField(db_column='groceryName', max_length=45)  # Field name made lowercase.
    category = models.CharField(max_length=45)
    price = models.FloatField()
    brand = models.CharField(max_length=45)
    description = models.CharField(max_length=100)
    stock = models.IntegerField()
    dest = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groceryItem'


class Grocerystore(models.Model):
    storeid = models.AutoField(db_column='storeID', primary_key=True)  # Field name made lowercase.
    grocerystoreadd_storeaddressid = models.ForeignKey('Grocerystoreadd', models.DO_NOTHING, db_column='groceryStoreAdd_storeAddressID')  # Field name made lowercase.
    storename = models.CharField(db_column='storeName', max_length=45)  # Field name made lowercase.
    description = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'groceryStore'


class Grocerystoreadd(models.Model):
    storeaddressid = models.AutoField(db_column='storeAddressID', primary_key=True)  # Field name made lowercase.
    streetaddress = models.CharField(db_column='streetAddress', max_length=45)  # Field name made lowercase.
    city = models.CharField(max_length=45)
    zipcode = models.IntegerField(db_column='zipCode')  # Field name made lowercase.
    state = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'groceryStoreAdd'


class Orderstatus(models.Model):
    orderstatusid = models.AutoField(db_column='orderStatusID', primary_key=True)  # Field name made lowercase.
    purchaseinfo_purchaseid = models.ForeignKey('Purchaseinfo', models.DO_NOTHING, db_column='purchaseInfo_purchaseID')  # Field name made lowercase.
    deliverydriver_driverid = models.ForeignKey(Deliverydriver, models.DO_NOTHING, db_column='deliveryDriver_driverID', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=45, blank=True, null=True)
    ordertime = models.DateTimeField(db_column='orderTime')  # Field name made lowercase.
    archive = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orderStatus'


class Purchaseinfo(models.Model):
    purchaseid = models.AutoField(db_column='purchaseID', primary_key=True)  # Field name made lowercase.
    userpaymentinfo_paymentid = models.ForeignKey('Userpaymentinfo', models.DO_NOTHING, db_column='userPaymentInfo_paymentID', blank=True, null=True)  # Field name made lowercase.
    grocerystore_storeid = models.ForeignKey(Grocerystore, models.DO_NOTHING, db_column='groceryStore_storeID', blank=True, null=True)  # Field name made lowercase.
    totalprice = models.FloatField(db_column='totalPrice', blank=True, null=True)  # Field name made lowercase.
    totalitems = models.IntegerField(db_column='totalItems', blank=True, null=True)  # Field name made lowercase.
    datetime = models.DateTimeField(db_column='dateTime', blank=True, null=True)  # Field name made lowercase.
    purchased = models.IntegerField(blank=True, null=True)
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    address_useraddressid = models.ForeignKey(Address, models.DO_NOTHING, db_column='address_userAddressID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'purchaseInfo'


class PurchaseinfoHasGroceryitem(models.Model):
    purchaseinfo_has_groceryitemid = models.AutoField(db_column='purchaseInfo_has_groceryItemID', primary_key=True)  # Field name made lowercase.
    purchaseinfo_purchaseid = models.ForeignKey(Purchaseinfo, models.DO_NOTHING, db_column='purchaseInfo_purchaseID')  # Field name made lowercase.
    groceryitem_groceryid = models.ForeignKey(Groceryitem, models.DO_NOTHING, db_column='groceryItem_groceryID')  # Field name made lowercase.
    purchased = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchaseInfo_has_groceryItem'


class Userpaymentinfo(models.Model):
    paymentid = models.AutoField(db_column='paymentID', primary_key=True)  # Field name made lowercase.
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    cardnumber = models.CharField(max_length=16)
    securitynumber = models.IntegerField()
    expirationdate = models.CharField(db_column='expirationDate', max_length=10)  # Field name made lowercase.
    zipcode = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'userPaymentInfo'
