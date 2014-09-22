from rest_framework import viewsets

from .models import *

class ReportViewSet(viewsets.ModelViewSet):
    model = Report

class ReadingViewSet(viewsets.ModelViewSet):
    model = Reading

class ValuesViewSet(viewsets.ModelViewSet):
    model = Values
