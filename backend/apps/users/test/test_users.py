from re import S
from unittest.mock import patch
from django.http import JsonResponse

from apps.users.models import User
from apps.users.serializers import UserResponseSerializer, UserSerializer
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status

class TestUserModel(APITestCase):

    @patch('apps.users.models.User.objects')
    def setUp(self, mockUser):
        sampleuser_1 = User.objects.create(tpk_firebaseid="testid",
                        tpk_name="test",
                        tpk_email="test_email@test.com")

    @patch('apps.users.models.User.objects.get')
    @patch('apps.parkersauth.permissions.isuserloggedin.IsUserLoggedIn.has_permission')
    def test_get(self, mockPerm, mockUser):
        mockUser.return_value = User.objects.create(tpk_firebaseid="testid",
                                tpk_name="test",
                                tpk_email="test_email@test.com")
        response = self.client.get('/users')

        # assert response code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get data from DB
        all_users = User.objects.all()
        # serialize, convert to json and compare against response.
        serializer = UserSerializer(data=all_users, many=True)
        if serializer.is_valid():
            users_json = JsonResponse(serializer.data, safe=False)
            self.assertJSONEqual(users_json, response.content)


    @patch('apps.parkersauth.permissions.isuserloggedin.IsUserLoggedIn.has_permission')
    @patch('apps.users.models.User.objects.get')
    def test_get_one(self, mockUser, mockPerm):
        testuser_3 = User.objects.create(tpk_firebaseid="testid", tpk_name="test", tpk_email="test_email@test.com") 
        mockUser.return_value = testuser_3

        response = self.client.get('/users/testid')
        single_user = User.objects.get(tpk_email="test_email@test.com")
        serializer = UserResponseSerializer(data=single_user, many=False)
        if serializer.is_valid():
            user_json = JsonResponse(serializer.data, safe=False)
            self.assertJSONEqual(user_json, response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('apps.parkersauth.permissions.isuserloggedin.IsUserLoggedIn.has_permission')     
    def test_get_one_notfound(self, mockPerm):
        response = self.client.get('/users/testid')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_post(self):
    #     resp = self.client.post("/users/", {'tpk_firebaseid': "PutUser_1"}, format='json')
    #     self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
    
    # def test_post_bad_request(self):
    #     resp = self.client.post("/users/", {'tpk_firebaseidinvalidkey': "PutUser_1"}, format='json')
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('apps.users.services.firebase.get_user_profile_bytoken')
    def test_put(self, mockService):
        mockService.return_value = {"users":[{'localId':'PutUser_1',"providerUserInfo":[{"rawId": "invalidToken",  
                                    "email": "test@test.com", "displayName": 
                                    "test", "photoUrl": "test"}]}]}
        resp = self.client.put("/users/register/PutUser_1", {"tpk_firebaseid": "token"}, format='json')
        self.assertEqual('{"tpk_name": "test", "tpk_email": "test@test.com", "tpk_photoUrl": "test", "tpk_firebaseid": "PutUser_1"}', str(resp.content, 'utf-8'))
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
    
    @patch('apps.users.services.firebase.get_user_profile_bytoken')
    def test_put_tokenauthentication_failed(self, mockService):
        mockService.return_value = {"users":[{'localId':'invalidToken',"providerUserInfo":[{"rawId": "invalidToken",  
                                    "email": "test@test.com", "displayName": 
                                    "test", "photoUrl": "test"}]}]}
        resp = self.client.put("/users/register/5", {"tpk_firebaseid": "PutUser_1"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
    
    @patch('apps.users.models.User.objects.filter')
    @patch('apps.users.services.firebase.get_user_profile_bytoken')
    def test_put_duplicate_user(self, mockService, mockUsers):
        mockService.return_value = {"users":[{'localId':'PutUser_1',"providerUserInfo":[{"rawId": "PutUser_1",  
                                    "email": "test@test.com", "displayName": 
                                    "test", "photoUrl": "test"}]}]}
        mockUsers.return_value = {"tpk_email": "test", "tpk_isdeleted": False}
        resp = self.client.put("/users/register/PutUser_1", {"tpk_firebaseid": "token"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)
    
    def test_put_bad_request(self):
       resp = self.client.put("/users/register/5", {'tpk_firebaseid_inavlidkey': "PutUser_1"}, format='json')
       self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('apps.parkersauth.permissions.isuserloggedin.IsUserLoggedIn.has_permission') 
    def test_delete(self, mockPerm):
        testuser_3 = User.objects.create(tpk_firebaseid="testid", tpk_name="test", tpk_email="test_email@test.com") 
        resp = self.client.delete('/users/test_email@test.com')
        updated_testuser_3 = User.objects.get(tpk_email="test_email@test.com")
        self.assertTrue(updated_testuser_3.tpk_isdeleted)
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)

    @patch('apps.parkersauth.permissions.isuserloggedin.IsUserLoggedIn.has_permission') 
    def test_get_nonexistent_user(self, mockPerm):
        resp = self.client.delete('/users/123456')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
