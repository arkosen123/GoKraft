from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view



from accounts.api.serializer import RegistrationSerializer

@api_view(['POST',])
def registration_view(request):

	if request.method == 'POST':
		serializer = RegistrationSerializer(data = request.data)
		data = {}
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'user registered succesfully'
			data['username'] = account.username
			data['email'] = account.email
		
		else:
			data = serializer.errors
		return Response(data)




