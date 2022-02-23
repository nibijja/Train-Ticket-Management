from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class ProfileManager(BaseUserManager):
    def create_user(self, gender, first_name, last_name, email, mobile, active_code, password = None):
        if not first_name:
            raise ValueError("User must provide a First Name")
        if not last_name:
            raise ValueError("User must provide a Last Name")
        if not email:
            raise ValueError("User must provide an Email")
        if not mobile:
            raise ValueError("User must provide a Contact Number")

        user = self.model(
            first_name      = first_name,
            last_name       = last_name,
            email           = self.normalize_email(email),
            mobile          = mobile,
            gender          = gender,
            active_code     = active_code,
        )

        user.set_password( password )
        user.save( using = self._db )
        return user

    def create_superuser(self, gender, first_name, last_name, email, mobile, password,):
        user = self.create_user(
            first_name      = first_name,
            last_name       = last_name,
            email           = self.normalize_email(email),
            mobile          = mobile,
            password        = password,
            gender          = gender,
            active_code     = 420022,

        )
        user.is_admin       = True
        user.is_staff       = True
        user.is_superuser   = True
        user.save(using = self._db)
        return user




class Profile(AbstractBaseUser):
    gender_choice= {
        ('Male', 'Male'),
        ('Female', 'Female'),
    }
    first_name      = models.CharField(max_length = 50)
    last_name       = models.CharField(max_length = 50)
    email           = models.EmailField(max_length = 50, unique = True)
    mobile          = models.IntegerField(unique = True)
    date_joined     = models.DateTimeField(auto_now_add = True)
    last_login      = models.DateTimeField(auto_now = True)
    is_admin        = models.BooleanField(default = False)
    is_active       = models.BooleanField(default = True)
    is_staff        = models.BooleanField(default = False)
    is_superuser    = models.BooleanField(default = False)
    gender          = models.CharField(max_length = 6, blank = False, null = False, choices = gender_choice)
    active_code     = models.CharField(max_length = 6)
    reset_code      = models.CharField(max_length = 6, null = True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile', 'gender', ]

    objects = ProfileManager()


    def __ste__(self):
        return self.first_name + "," + self.last_name + "," + self.email + "," + "," + self.mobile + "," + self.gender

    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Tickets(models.Model):
    ticket_id       = models.AutoField(primary_key = True)
    status          = models.CharField(max_length = 10, default = "Unverified")
    date            = models.DateField()
    day             = models.CharField(max_length = 10)
    verify_code     = models.TextField(max_length = 10)
    train_name      = models.CharField(max_length = 50)
    train_id        = models.IntegerField()
    frome           = models.CharField(max_length = 50)
    to              = models.CharField(max_length = 50)
    classes         = models.CharField(max_length = 50)
    adult           = models.IntegerField()
    child           = models.IntegerField()
    departure_time  = models.CharField(max_length = 50)
    arrival_time    = models.CharField(max_length = 50)
    buyer_id        = models.IntegerField()
    buyer_name      = models.CharField(max_length = 100)
    email           = models.EmailField(max_length = 50)
    mobile          = models.IntegerField()
    fair            = models.DecimalField(max_digits = 6, decimal_places = 2)
    charge          = models.DecimalField(max_digits = 6, decimal_places = 2)
    total           = models.DecimalField(max_digits = 6, decimal_places = 2)

class Stations(models.Model):
    station_name            = models.CharField(max_length = 50)
    factors                 = models.DecimalField(max_digits = 4, decimal_places = 2)
    station_id              = models.IntegerField(primary_key = True)

class Trains(models.Model):
    train_name             = models.CharField(max_length = 50)
    factors                = models.DecimalField(max_digits = 4, decimal_places = 2)
    train_id               = models.IntegerField(primary_key = True)
    departure_time         = models.TimeField()
    offday                 = models.CharField(max_length = 10)
    stopages               = models.CharField(max_length = 5000)
    ac_b_seat              = models.IntegerField()
    ac_s_seat              = models.IntegerField()
    f_b_seat               = models.IntegerField()
    f_s_seat               = models.IntegerField()
    snigdha_seat           = models.IntegerField()
    s_chair_seat           = models.IntegerField()
    sulov_seat             = models.IntegerField()
    total                  = models.IntegerField()

class SatTrains(models.Model):
    train_name            = models.CharField(max_length = 50)
    factors               = models.DecimalField(max_digits = 4, decimal_places = 2)
    train_id              = models.IntegerField(primary_key = True)
    departure_time        = models.TimeField()
    offday                = models.CharField(max_length = 10)
    stopages               = models.CharField(max_length = 5000)
    ac_b_seat              = models.IntegerField()
    ac_s_seat              = models.IntegerField()
    f_b_seat               = models.IntegerField()
    f_s_seat               = models.IntegerField()
    snigdha_seat           = models.IntegerField()
    s_chair_seat           = models.IntegerField()
    sulov_seat             = models.IntegerField()
    total                  = models.IntegerField()

class SunTrains(models.Model):
    train_name            = models.CharField(max_length = 50)
    factors               = models.DecimalField(max_digits = 4, decimal_places = 2)
    train_id              = models.IntegerField(primary_key = True)
    departure_time        = models.TimeField()
    offday                = models.CharField(max_length = 10)
    stopages               = models.CharField(max_length = 5000)
    ac_b_seat              = models.IntegerField()
    ac_s_seat              = models.IntegerField()
    f_b_seat               = models.IntegerField()
    f_s_seat               = models.IntegerField()
    snigdha_seat           = models.IntegerField()
    s_chair_seat           = models.IntegerField()
    sulov_seat             = models.IntegerField()
    total                  = models.IntegerField()
    
class MonTrains(models.Model):
    train_name            = models.CharField(max_length = 50)
    factors               = models.DecimalField(max_digits = 4, decimal_places = 2)
    train_id              = models.IntegerField(primary_key = True)
    departure_time        = models.TimeField()
    offday                = models.CharField(max_length = 10)
    stopages               = models.CharField(max_length = 5000)
    ac_b_seat              = models.IntegerField()
    ac_s_seat              = models.IntegerField()
    f_b_seat               = models.IntegerField()
    f_s_seat               = models.IntegerField()
    snigdha_seat           = models.IntegerField()
    s_chair_seat           = models.IntegerField()
    sulov_seat             = models.IntegerField()
    total                  = models.IntegerField()
    
class TueTrains(models.Model):
    train_name            = models.CharField(max_length = 50)
    factors               = models.DecimalField(max_digits = 4, decimal_places = 2)
    train_id              = models.IntegerField(primary_key = True)
    departure_time        = models.TimeField()
    offday                = models.CharField(max_length = 10)
    stopages               = models.CharField(max_length = 5000)
    ac_b_seat              = models.IntegerField()
    ac_s_seat              = models.IntegerField()
    f_b_seat               = models.IntegerField()
    f_s_seat               = models.IntegerField()
    snigdha_seat           = models.IntegerField()
    s_chair_seat           = models.IntegerField()
    sulov_seat             = models.IntegerField()
    total                  = models.IntegerField()
    
class WedTrains(models.Model):
    train_name            = models.CharField(max_length = 50)
    factors               = models.DecimalField(max_digits = 4, decimal_places = 2)
    train_id              = models.IntegerField(primary_key = True)
    departure_time        = models.TimeField()
    offday                = models.CharField(max_length = 10)
    stopages               = models.CharField(max_length = 5000)
    ac_b_seat              = models.IntegerField()
    ac_s_seat              = models.IntegerField()
    f_b_seat               = models.IntegerField()
    f_s_seat               = models.IntegerField()
    snigdha_seat           = models.IntegerField()
    s_chair_seat           = models.IntegerField()
    sulov_seat             = models.IntegerField()
    total                  = models.IntegerField()
    
class ThuTrains(models.Model):
    train_name            = models.CharField(max_length = 50)
    factors               = models.DecimalField(max_digits = 4, decimal_places = 2)
    train_id              = models.IntegerField(primary_key = True)
    departure_time        = models.TimeField()
    offday                = models.CharField(max_length = 10)
    stopages               = models.CharField(max_length = 5000)
    ac_b_seat              = models.IntegerField()
    ac_s_seat              = models.IntegerField()
    f_b_seat               = models.IntegerField()
    f_s_seat               = models.IntegerField()
    snigdha_seat           = models.IntegerField()
    s_chair_seat           = models.IntegerField()
    sulov_seat             = models.IntegerField()
    total                  = models.IntegerField()
    
class FriTrains(models.Model):
    train_name            = models.CharField(max_length = 50)
    factors               = models.DecimalField(max_digits = 4, decimal_places = 2)
    train_id              = models.IntegerField(primary_key = True)
    departure_time        = models.TimeField()
    offday                = models.CharField(max_length = 10)
    stopages               = models.CharField(max_length = 5000)
    ac_b_seat              = models.IntegerField()
    ac_s_seat              = models.IntegerField()
    f_b_seat               = models.IntegerField()
    f_s_seat               = models.IntegerField()
    snigdha_seat           = models.IntegerField()
    s_chair_seat           = models.IntegerField()
    sulov_seat             = models.IntegerField()
    total                  = models.IntegerField()

class Choices(models.Model):
    ac_b                  = models.DecimalField(max_digits = 4, decimal_places = 2)
    ac_s                  = models.DecimalField(max_digits = 4, decimal_places = 2)
    f_b                   = models.DecimalField(max_digits = 4, decimal_places = 2)
    f_s                   = models.DecimalField(max_digits = 4, decimal_places = 2)
    snigdha               = models.DecimalField(max_digits = 4, decimal_places = 2)
    s_chair               = models.DecimalField(max_digits = 4, decimal_places = 2)
    sulov                 = models.DecimalField(max_digits = 4, decimal_places = 2)
