from hasher.database.hashesDao import hashesDao
import json
import traceback
import logging
from rest_framework import status
from bson.json_util import dumps
import hashlib
import base62
from datetime import datetime
from django.shortcuts import redirect
log = logging.getLogger(__name__)

class hashService:

    hashesDao = hashesDao()
  
    @classmethod
    def generateUrlId(cls, url ,domain):
        try:
            
            hashed_url = hashlib.sha256(url.encode()).hexdigest()   
             # Convert hash value to bytes
            hash_bytes = bytes.fromhex(hashed_url)
    
            # Encode bytes using base62 encoder
            encoded_value = base62.encode(hash_bytes)
            
            data = {
                "urlId" : encoded_value[:6],
                "hash" : hashed_url,
                "url" : url,
                'createdAt': datetime.now()
            }
            result = hashesDao.addUrlId(encoded_value[:6] , data)
               
            if result:
                # Return first 6 characters of the encoded value
                return "https://{domainname}/en/" + encoded_value[:6]    
             
        except Exception as e:
            exceptionTrace = traceback.format_exc()
            message = f"Failure while generating unique url ID" \
                      f"exceptionTrace: {exceptionTrace}" \
                      f" Exception: {str(e)}"
        return None
    
    @classmethod
    def doesHashExist(cls,hash):
        result = hashesDao.getHashValue(hash)
        if result:
            return True , result["urlId"]
        return False , None 
    
    @classmethod
    def redirect_to_original_url(request, urlId):
        try:
            result = hashesDao.getOriginalUrl(urlId)
            if result:
                originalUrl = result["url"]
                return redirect(originalUrl)
        except Exception as e:
            exceptionTrace = traceback.format_exc()
            message = f"Failure while finding url" \
                      f"exceptionTrace: {exceptionTrace}" \
                      f" Exception: {str(e)}"
        return None