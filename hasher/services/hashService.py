from hasher.database.hashesDao import hashesDao
from django.http import HttpResponseRedirect
import json
import traceback
import logging
from rest_framework import status
from bson.json_util import dumps
import hashlib
from datetime import datetime
from django.shortcuts import redirect
log = logging.getLogger(__name__)
from django.http import JsonResponse
class hashService:

    hashesDao = hashesDao()
  
    @classmethod
    def generateUrlId(cls, url ,domain):
        try:
            
            hashed_url = hashlib.sha256(url.encode()).hexdigest()
            hashed_url = hashed_url.encode('ASCII')  
            salt = hashed_url[:32]  # Generate a random salt
            
            # Derive a key using PBKDF2 with 3 iterations and SHA-256 as the hash function
            key = hashlib.pbkdf2_hmac('sha256', hashed_url, salt, 3 , 3)

            # Print the derived key in hexadecimal format
            urlId = key.hex()
            
            data = {
                "urlId" : urlId,
                "hash" : hashed_url,
                "url" : url,
                'createdAt': datetime.now()
            }
            result = cls.hashesDao.addUrlId(data , urlId)
            
            if result:
                # return {domain} + urlId here you can choose any domain which you want for your system ,
                # do keep the same url in urls.py
                return "http://127.0.0.1:8000/en/" + urlId    
             
        except Exception as e:
            exceptionTrace = traceback.format_exc()
            message = f"Failure while generating unique url ID" \
                      f"exceptionTrace: {exceptionTrace}" \
                      f" Exception: {str(e)}"
            print("ERROR" , message)
        return None
    
    @classmethod
    def doesHashExist(cls,hash):
        result = cls.hashesDao.getHashValue(hash)
        if result:
            return True , result["urlId"]
        return False , None 
    
    @classmethod
    def redirect_to_original_url(cls,urlId):
        try:
            result = cls.hashesDao.getOriginalUrl(urlId)
            
            if result:
                originalUrl = result["url"]
                return redirect(originalUrl)
        except Exception as e:
            response = dict()
            exceptionTrace = traceback.format_exc()
            message = f"Failure while finding url" \
                      f"exceptionTrace: {exceptionTrace}" \
                      f" Exception: {str(e)}"
            response["message"] = "Invalid request"
            return JsonResponse(response , status = status.HTTP_400_BAD_REQUEST)
        