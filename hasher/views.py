from rest_framework.decorators import api_view , permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import JsonResponse
from hasher.services.hashService import hashService

@api_view(['POST'])
def shortenedUrlOperation(request):
    response = dict()
    
    if request.method == 'POST':
        requestBody = JSONParser().parse(request)
        if "url" not in requestBody or "domain" not in requestBody:
            response["message"] = "Invalid request"
            return JsonResponse(response , status = status.HTTP_400_BAD_REQUEST)
        
        shortUrl = hashService.generateUrlId(requestBody["url"]  , requestBody["domain"])
        response["data"] = shortUrl
        return JsonResponse(response , status = status.HTTP_201_CREATED)
  
@api_view(['GET'])
def originalUrlOperation(request , urlId):
    response = dict()
    
    if request.method == 'GET':
        result = hashService.redirect_to_original_url(urlId)
        if not result:
            response["message"] = "Invalid request"
            return JsonResponse(response , status = status.HTTP_400_BAD_REQUEST)
        
    