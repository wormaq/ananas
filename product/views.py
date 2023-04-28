from django.shortcuts import render
from rest_framework.generics import ListAPIView
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer, ProductFilterSerializer
from user.permissions import IsVendorPermission, IsOwnerOrReadOnly
from django_filters import rest_framework as filters


# class ProductListAPIView(APIView):
#     permission_classes = [permissions.AllowAny]
#
#     def get(self, request):
#         all_product = Product.objects.all()
#         serializer = ProductSerializer(all_product, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = ('category', 'name')


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filterset_class(self.request.GET, queryset=queryset).qs


# class ProductFilter(django_filters.FilterSet):
#     def get(self, request):
#         # product = Product.objects.filter()
#         serializer = ProductFilterSerializer()
#         return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        all_category = Category.objects.all()
        serializer = CategorySerializer(all_category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductCreateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = Product.objects.create(
                vendor_id=request.data['vendor'],
                category_id=request.data['category'],
                name=request.data['name'],
                description=request.data['description'],
                price=request.data['price']
            )
            product.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryCreateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = Category.objects.create(
                name=request.data['name'],
            )
            category.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def delete(self, request, id):
        product = self.get_object(id)
        serializer = ProductSerializer(product)
        product.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class CategoryDeleteAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, id):
        try:
            return Category.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def delete(self, request, id):
        category = self.get_object(id)
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class ProductUpdateAPIView(APIView):
    permission_classes = [IsVendorPermission, IsOwnerOrReadOnly]

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def put(self, request, id):
        snippet = self.get_object(id)
        serializer = ProductSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryUpdateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, id):
        try:
            return Category.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def put(self, request, id):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = self.get_object(id)
            category = Category.objects.update(
                name=request.data['name'],
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id):
        product = self.get_object(id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)





