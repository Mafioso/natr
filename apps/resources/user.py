from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from auth2.serializers import AccountSerializer
from natr.rest_framework.policies import AuthenticatedPolicy

@api_view(['GET'])
@permission_classes((AuthenticatedPolicy,))
def get_initial_state(request):
	user_ = AccountSerializer(instance=request.user).data
	return Response({
		'current_user': user_
	})