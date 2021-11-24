from django.contrib.auth import logout
from django.http import HttpResponseRedirect


def avaUser(name):
    return name[0:2].upper()