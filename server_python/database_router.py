#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf import settings

DATABASE_MAPPING = settings.DATABASE_APPS_MAPPING


class DatabaseAppsRouter(object):
    """
    A router to control all database operations on models for different
    databases.

    In case an app is not set in settings.DATABASE_APPS_MAPPING, the router
    will fallback to the `default` database.

    Settings example:

    DATABASE_APPS_MAPPING = {'app1': 'db1', 'app2': 'db2'}

    这个路由，针对对不同的数据库，用于操作所有的数据库模型

    如果一个应用没有在 settings 里的 DATABASE_APPS_MAPPING 中配置，那么这个路由将最后被 default 这个数据库来配置

    设置示例（这里指 DATABASE_APPS_MAPPING 属性）：

    DATABASE_APPS_MAPPING = {'app1': 'db1', 'app2': 'db2'}
    """

    def db_for_read(self, model, **hints):
        """"
        Point all read operations to the specific database.
        将所有读取操作，指向对特定的数据库
        """
        if model._meta.app_label in DATABASE_MAPPING:
            return DATABASE_MAPPING[model._meta.app_label]
        return None

    def db_for_write(self, model, **hints):
        """
        Point all write operations to the specific database.
        将所有的写操作，指向特定的数据库
        """
        if model._meta.app_label in DATABASE_MAPPING:
            return DATABASE_MAPPING[model._meta.app_label]
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow any relation between apps that use the same database.
        允许 任何使用相同数据库的应用 的任何关系
        """
        db_obj1 = DATABASE_MAPPING.get(obj1._meta.app_label)
        db_obj2 = DATABASE_MAPPING.get(obj2._meta.app_label)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            else:
                return False
        return None

    # Django 1.7 - Django 1.11
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        print
        db, app_label, model_name, hints
        if db in DATABASE_MAPPING.values():
            return DATABASE_MAPPING.get(app_label) == db
        elif app_label in DATABASE_MAPPING:
            return False
        return None
