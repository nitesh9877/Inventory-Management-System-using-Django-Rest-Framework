from django.shortcuts import get_object_or_404
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Item
from .serializers import ItemSerializer

# Utility function to generate JWT token for a user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Register the user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # User created successfully
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors

# Login view
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Authenticate the user
    user = authenticate(username=username, password=password)

    if user is not None:
        # Generate JWT token
        return Response(get_tokens_for_user(user))
    else:
        return Response({"detail": "Invalid credentials"}, status=400)

# CRUD API views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    serializer = ItemSerializer(item)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_items(request):
    items = Item.objects.all()  # Retrieve all items from the database
    serializer = ItemSerializer(items, many=True)  # Serialize the queryset
    return Response(serializer.data, status=status.HTTP_200_OK)  # Return the serialized data

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    serializer = ItemSerializer(item, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return Response({'message': 'Item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)  
