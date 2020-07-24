from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from django.core.exceptions import ValidationError


from accounts.api.serializer import RegistrationSerializer
from accounts.models import Account



def validate_email(email):
	account = None
	try:
		account = Account.objects.get(email=email)
	except Account.DoesNotExist:
		return None
	if account != None:
		return email

def validate_username(username):
	account = None
	try:
		account = Account.objects.get(username=username)
	except Account.DoesNotExist:
		return None
	if account != None:
		return username




@api_view(['POST',])
def registration_view(request):

	if request.method == 'POST':
		data = {}
		email = request.data.get('email', '0').lower()
		if validate_email(email) != None:
			data['error_message'] = 'That email is already in use.'
			data['response'] = 'Error'
			return Response(data)

		username = request.data.get('username', '0')
		if validate_username(username) != None:
			data['error_message'] = 'That username is already in use.'
			data['response'] = 'Error'
			return Response(data)

		serializer = RegistrationSerializer(data = request.data)
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'user registered succesfully'
			data['username'] = account.username
			data['email'] = account.email
		
		else:
			data = serializer.errors
		return Response(data)

		# account = serializer.save()
		# data['response'] = 'user registered succesfully'
		# data['username'] = account.username
		# data['email'] = account.email

		return Response(data)



