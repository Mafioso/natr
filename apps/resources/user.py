from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_current_user(request):
	user = request.user
	return Response({
		'id': user.id,
		'email': user.email,
		'first_name': user.first_name,
		'last_name': user.last_name,
		'counters': user.get_counters()
	})