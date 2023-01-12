import datetime,jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from Split.models import Transaction
from .serializers import RegisterSerializer, TransactionSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()

class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }

        token = jwt.encode(payload,'secret',algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data={
            'jwt':token
        }

        return response


class UserView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        serializer = RegisterSerializer(user)
        return Response(serializer.data)
    
class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data={
            'message':'success'
        }

        return response

# get all user
class Get_UsersView(APIView):
    def get(self,request):
        jwt = JWTAuthentication()
        user,token = jwt.authenticate(request)
        users = User.objects.all()
        serializer = RegisterSerializer(users,many=True)
        return Response(serializer.data)


class Add_TransactionView(APIView):
    def post(self,request):
        jwt = JWTAuthentication()
        user,token = jwt.authenticate(request)
        # if it gives user is unauthorised give the msg to the user on html page
        
        serializer_transaction = TransactionSerializer(data=request.data)
        serializer_transaction.is_valid(raise_exception=True)
        serializer_transaction.save(paid_by=user) 

        return Response(serializer_transaction.data)


class Delete_TransactionView(APIView):
    def delete(self,request,id):
        jwt = JWTAuthentication()
        user,token = jwt.authenticate(request)
        transaction = Transaction.objects.filter(id=id).first()
        if transaction is None:
            raise AuthenticationFailed('Transaction not found')
        if transaction.paid_by.id != user.id:
            raise AuthenticationFailed('You are not allowed to delete this transaction')
        transaction.delete()
        return Response('Transaction deleted successfully')


class Update_TransactionView(APIView):
    def post(self,request,id):
        jwt = JWTAuthentication()
        user,token = jwt.authenticate(request)
        transaction = Transaction.objects.filter(id=id).first()
        if transaction is None:
            raise AuthenticationFailed('Transaction not found')
        if transaction.paid_by.id != user.id:
            raise AuthenticationFailed('You are not allowed to update this transaction')
        serializer_transaction = TransactionSerializer(data=request.data)
        serializer_transaction.is_valid(raise_exception=True)
        # update the transaction with the new data 'amount','title','split_between_users'
        transaction.amount = serializer_transaction.validated_data['amount']
        transaction.title = serializer_transaction.validated_data['title']
        transaction.split_between_users.set(serializer_transaction.validated_data['split_between_users'])
        transaction.save()

        # return the updated transaction
        serializer_transaction = TransactionSerializer(transaction)
        return Response(serializer_transaction.data)


class Get_TransactionsView(APIView):
    def get(self,request):
        jwt = JWTAuthentication()
        user,token = jwt.authenticate(request)
        transactions = Transaction.objects.filter(paid_by=user)
        serializer = TransactionSerializer(transactions,many=True)
        return Response(serializer.data)


class Get_TransactionInfoView(APIView):
    def get(self,request):
        jwt = JWTAuthentication()
        user,token = jwt.authenticate(request)

        user = User.objects.filter(id=user.id).first()
        transactions_by_user = Transaction.objects.filter(paid_by=user)
        transactions_in_split_between_users = Transaction.objects.filter(split_between_users=user)
        net = 0
        receiving_amount = 0
        paying_amount = 0
        friend_dairy = {}

        for transaction in transactions_by_user:
            for friend in transaction.split_between_users.all():

                if friend.pk not in friend_dairy:
                    friend_dairy[friend.pk] = 0
                amount_from_friend_for_this_transaction = transaction.amount/(transaction.split_between_users.count()+1)
                friend_dairy[friend.pk] += amount_from_friend_for_this_transaction
                receiving_amount += amount_from_friend_for_this_transaction

        for transaction in transactions_in_split_between_users:
            users_part_in_this_transaction = transaction.amount/(transaction.split_between_users.count()+1)
            payer_for_this_transaction = transaction.paid_by

            if payer_for_this_transaction.pk not in friend_dairy:
                friend_dairy[payer_for_this_transaction.pk] = 0
            friend_dairy[payer_for_this_transaction.pk] -= users_part_in_this_transaction
            paying_amount += users_part_in_this_transaction
            
        net = receiving_amount-paying_amount
        data = {
            'net':net,
            'receiving_amount':receiving_amount,
            'paying_amount':paying_amount,
            'friend_dairy':friend_dairy
                }
        return Response(data)
        
        
        