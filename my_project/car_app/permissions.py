from rest_framework import permissions
from rest_framework.permissions import BasePermission


class CheckCRUD(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
          return True
        return obj.seller == request.user


class CheckAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
          return True
        return request.user.role == 'admin'


class CheckBuyer(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
          return True
        return request.user.role == 'buyer'

