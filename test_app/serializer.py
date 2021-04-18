from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.serializers import Serializer
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class PutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Put
        fields = '__all__'


class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = '__all__'


class ValueHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Value_History
        fields = '__all__'


class HistogramEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Histogram_Entry
        fields = '__all__'


class ViewedHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Viewed_History
        fields = '__all__'


class WatchlistEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist_Entry
        fields = '__all__'


class AnalystSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analyst
        fields = '__all__'


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = '__all__'
