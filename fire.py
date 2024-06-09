#FIrebase backened as service
import firebase_admin
from firebase_admin import credentials

#Fetch service account key JSON file contents
cred = credentials.Certificate("path/to/serviceAccountKey.json")

#Init app with service account, grant admin privleges 
firebase_admin.initialize_app(cred, {
    'databaseURL':'https://carfinder-a7372-default-rtdb.firebaseio.com/' 
    })

#Save 
