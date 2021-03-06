from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import filters
# Create your views here.
from rest_framework import viewsets
from .serializers import *
from .models import *
from .permissions import *

import collections


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserList(generics.ListCreateAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer

class UserProfileView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        profile = UserProfile.objects.all()
        serializer = UserProfileSerializer(profile, many=True)
        return Response(serializer.data)


class UserProfileDetailView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def get_object(self, pk):
        return UserProfile.objects.get(pk=pk)

    def patch(self, request, pk, format=None):
        profile_object = self.get_object(pk)
        serializer = UserProfileSerializer(
            profile_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseView(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Course.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ['department', 'number', 'name', ]
    serializer_class = CourseSerializer

    # def get(self, request, format = None):
    #     course = Course.objects.all()
    #     serializer = CourseSerializer(course, many = True)
    #     return Response(serializer.data)

    # def post(self, request, format = None):
    #     serializer = CourseSerializer(data = request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get_object(self, pk):
        return Course.objects.get(pk=pk)

    def get(self, request, pk, format=None):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        course = self.get_object(pk)
        userpk = request.data['userpk']
        user_remove = User.objects.get(pk=userpk)
        updatedcourse = course.user.remove(user_remove)
        serializer = CourseSerializer(updatedcourse)
        events = EventforCourseView().get_object(pk=pk).filter(participants__pk=userpk)
        for event in events:
            EventDetailView().remove(userpk=userpk, pk=event.pk)
        return Response(serializer.data)


class EnrolledDetailView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get_object(self, pk):
        return Course.objects.filter(user__pk=pk)

    def get(self, request, pk, format=None):
        course = self.get_object(pk).all()
        serializer = CourseSerializer(course, many=True)
        return Response(serializer.data)


class EventView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get_object(self, pk):
        return Event.objects.get(pk=pk)

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        event = self.get_object(pk)
        print(request.data)
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['participants'] = request.data['participants']
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        userpk = request.data['userpk']
        user_remove = User.objects.get(pk=userpk)
        updatedevent = event.participants.remove(user_remove)
        serializer = EventSerializer(updatedevent)
        return Response(serializer.data)

    def remove(self, userpk, pk, format=None):
        event = self.get_object(pk)
        user_remove = User.objects.get(pk=userpk)
        updatedevent = event.participants.remove(user_remove)
        serializer = EventSerializer(updatedevent)
        return Response(serializer.data)


class EventforCourseView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get_object(self, pk):
        return Event.objects.filter(course_focus__pk=pk)

    def get(self, request, pk, format=None):
        event = self.get_object(pk).all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)


class EventforStudentView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get_object(self, pk):
        return Event.objects.filter(participants__pk=pk)

    def get(self, request, pk, format=None):
        event = self.get_object(pk).all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)


class EventforOrganizerView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get_object(self, eventpk):
        event = Event.objects.get(pk=eventpk)
        return event

    def get(self, request, userpk, eventpk, format=None):
        event = self.get_object(eventpk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def delete(self, request, userpk, eventpk, format=None):
        event = self.get_object(eventpk)
        event.delete()
        return Response(status=status.HTTP_200_OK)


class EventCreateView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, userpk, coursepk, format=None):
        event = request.data

        event['course_focus'] = coursepk
        event['user'] = userpk
        course = CourseDetailView().get_object(pk=coursepk)
        organizer = User.objects.get(pk=userpk)
        serializer = EventSerializer(data=event, partial = True)
        if serializer.is_valid():
            serializer.validated_data['course_focus'] = course
            serializer.validated_data['organizer'] = organizer
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllMessageList(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return (
            self.request.user.sent_message.all() | self.request.user.received_message.all()
        ).order_by('-timestamp')


class MessageView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get_object(self, pk):
        return Message.objects.filter(sender__pk=pk) | Message.objects.filter(receivers__pk=pk)

    def get(self, request, pk, format=None):
        messages = self.get_object(pk).all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConversationListView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get_tuple_key(self, message):
        group = [message.sender.username]
        receivers = message.receivers.all()
        for r in receivers:
            group.append(r.username)
        return tuple(sorted(group))

    def get(self, request, pk, format=None):
        print('user:', request.user)

        messages = (Message.objects.filter(
            sender__pk=pk) | Message.objects.filter(receivers__pk=pk)).order_by('-timestamp')
        ret = []
        unique_convos = set()
        for m in messages:
            key = self.get_tuple_key(m)
            if key not in unique_convos:
                unique_convos.add(key)
                ret.append(m)
        serializer = MessageSerializer(ret, many=True)
        return Response(serializer.data)


class TwoWayConvoView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, pka, pkb, format=None):
        print('user:', request.user)
        messages = Message.objects.filter(sender__pk=pka).filter(
            receivers__username=pkb) | Message.objects.filter(sender__username=pkb).filter(receivers__pk=pka)
        messages = messages.order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class AllUsers(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        data = serializer.data
        ret = []
        for d in data:
            ret.append(d["username"])
        return Response(ret)


class SendMessage(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MessageSerializerForSending


'''
    def post(self, request, format=None):
        serializer = MessageSerializerForSending(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''


class Username_to_pk(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, username, format=None):
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        print(serializer.data["pk"])
        return Response(serializer.data["pk"])
