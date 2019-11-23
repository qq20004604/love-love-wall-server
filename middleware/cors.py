#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from django.utils.deprecation import MiddlewareMixin


class Cors(MiddlewareMixin):
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '127.0.0.1'
        return response
