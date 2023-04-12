from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAuthor(BasePermission):
    # def has_permission(self, request: Request, view: APIView) -> bool:
    #     return super().has_permission(request, view)

    # wycina dostęp do konkretnego modelu
    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        if request.method == 'DELETE':
            return obj.owner == request.user

        return True


class IsStaff(BasePermission):
    # wycina dostęp do jednej lub wielu metod HTTP
    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user and request.user.is_staff


class HasAddProductPermission(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.has_perm('products.add_product')
