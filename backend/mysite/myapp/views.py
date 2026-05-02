from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item

@csrf_exempt
def manage_items(request):
    if request.method == "GET":
        items = list(Item.objects.values())
        return JsonResponse(items, safe=False)
    
    if request.method == "POST":
        data = json.loads(request.body)
        item = Item.objects.create(name=data['name'], price=data['price'], stock=data['stock'])
        return JsonResponse({"id": item.id, "message": "Created"}, status=201)

@csrf_exempt
def delete_item(request, pk):
    if request.method == "DELETE":
        Item.objects.get(pk=pk).delete()
        return JsonResponse({"message": "Deleted"})