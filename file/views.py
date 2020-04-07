#!/usr/bin/env python
# encoding: utf-8

from django.shortcuts import render

# Create your views here.
import zlib
import time, io
import zipfile
from rest_framework import generics
from file.models import File
from file.serializers import FileSerializer
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                        BucketAlreadyExists)
from argparse import ArgumentError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class SetPagination(PageNumberPagination):
    """
    customize pagination
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        data = {"page": self.page.number, "count": self.page.paginator.count,
                "page_size": self.get_page_size(self.request), "total_pages": self.page.paginator.num_pages,
                "datas": data}
        return Response(OrderedDict([
            ('code', "000000"),
            ('message', "success"),
            ('data', data)
        ]))

class FileViewSet(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    lookup_field = 'id'
    pagination_class = SetPagination

    def post(self, request, *args, **kwargs):
        begin_time = time.time()
        files = request.FILES.getlist('path')
        print(files)
        # file_list = []
        # # file_list = [File(name=f.name.rstrip('"'), path=f) for f in files]
        # for f in files:
        #     file_list.append(File(name=f.name.rstrip('"'), path=f))
        # File.objects.bulk_create(file_list)
        # print(time.time()-begin_time)
    
    def create(self, data, *args, **kwargs):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def get_queryset(self):
    #     return self.queryset.filter(id__in=[13350,13351])
from mysite.MinIOStorage import MinioStorage
import io,os
import zipfile
import tempfile
import urllib.request as ur
from django.http import FileResponse
import datetime
# from django.core.servers.basehttp import FileWrapper
class file_download(generics.ListAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return serializer.data

    def get(self, request, *args, **kwargs):
        # name = request.query_params['name']
        # a = MinioStorage().open(name)
        # queryset = self.filter_queryset(self.get_queryset())
        # page = self.paginate_queryset(queryset)
        # serializer = self.get_serializer(page, many=True)
        download_urls = self.list(request, *args, **kwargs)
        # download_urls = serializer.data
        # print(download_urls)
        # 创建BytesIO
        s = io.BytesIO()
        # 创建一个临时文件夹用来保存下载的文件
        temp = tempfile.TemporaryDirectory()
        # 使用BytesIO生成压缩文件
        zip = zipfile.ZipFile(s, 'w')
        for i in download_urls:
            # f_name = "{}.pdf".format(i['name'])
            local_path = os.path.join(temp.name, i['name'])
            # 下载文件
            ur.urlretrieve(i['path'], local_path)
            # 把下载文件的写入压缩文件
            zip.write(local_path, i['name'])
        # 关闭文件
        zip.close()
        # 指针回到初始位置，没有这一句前端得到的zip文件会损坏
        s.seek(0)
        # s = self.contract_download(download_urls)
        return FileResponse(s, as_attachment=True, filename='%s.zip'.format(datetime.datetime.now().strftime("%Y-%m-%d")), content_type='application/zip')

    def contract_download(self, download_urls):
        '''
        downloads_urls 要批量下载并且压缩的文件
        '''
        # 创建BytesIO
        s = io.BytesIO()
        # 创建一个临时文件夹用来保存下载的文件
        temp = tempfile.TemporaryDirectory()
        # 使用BytesIO生成压缩文件
        zip = zipfile.ZipFile(s, 'w')
        for i in download_urls:
            # f_name = "{}.pdf".format(i['name'])
            local_path = os.path.join(temp.name, i['name'])
            # 下载文件
            ur.urlretrieve(i['path'], local_path)
            # 把下载文件的写入压缩文件
            zip.write(local_path, f_name)
        # 关闭文件
        zip.close()
        # 指针回到初始位置，没有这一句前端得到的zip文件会损坏
        s.seek(0)
        # 用FileWrapper类来迭代器化一下文件对象，实例化出一个经过更适合大文件下载场景的文件对象，实现原理相当与把内容一点点从文件中读取，放到内存，下载下来，直到完成整个下载过程。这样内存就不会担心你一下子占用它那么多空间了。
        # wrapper = FileWrapper(s)
        # response = HttpResponse(s, content_type='application/zip')
        # response['Content-Disposition'] = 'attachment; filename={}.zip'.format(datetime.datetime.now().strftime("%Y-%m-%d"))
        # return response
        return s



