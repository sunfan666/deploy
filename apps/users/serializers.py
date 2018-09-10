from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from .tasks import useradd, mail

from utils.gitlab_api import gl

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化类
    """

    class Meta:
        model = User
        fields = ("id", "username", "name", "phone", "email", "is_active")

    def to_group_response(self, group_queryset):
        ret = []
        # 将组信息序列化
        for group in group_queryset:
            ret.append({
                'id': group.id,
                'name': group.name
            })
        return ret

    def to_representation(self, instance):
        role = self.to_group_response(instance.groups.all())
        ret = super(UserSerializer, self).to_representation(instance)
        ret["role"] = role
        return ret

    def create(self, validated_data):
        validated_data["is_active"] = True
        validated_data["password"] = "12345678"
        instance = super(UserSerializer, self).create(validated_data=validated_data)
        instance.email = "{}{}".format(instance.username, settings.DOMAIN)
        instance.set_password(validated_data["password"])

        # 创建gitlab账户
        useradd.delay(validated_data['username'],validated_data['password'],instance.email,validated_data['name'])
        mail.delay("通知",
                       validated_data['username'],
                       settings.EMAIL_FROM,
                       ['787696331@qq.com'],
                       )
        # res = gl.users.create({'username': validated_data['username'], 'password':validated_data['password'], 'email': instance.email, 'name': validated_data['name']})
        # print(res)
        instance.save()
        return instance

    # def update(self, instance, validated_data):
    #     print(validated_data)
    #     password = validated_data.pop("password", None)
    #     self.Meta.model.objects.filter(id=instance.id).update(**validated_data)
    #     if password:
    #         print("1111")
    #         instance.set_password(password)
    #         instance.save()
    #     return instance


class Groupserializer(serializers.ModelSerializer):
    """
    group序列化类,拿到组内成员个数并序列化输出
    """

    def to_permission_response(self, permission_queryset):
        ret = []
        # 将角色权限信息序列化
        for permission in permission_queryset:
            ret.append({
                'id': permission.id,
                'name': permission.name,
                'codename': permission.codename,
            })
        return ret

    def to_members_response(self, members_queryset):
        ret = []
        # 将角色用户信息序列化
        for member in members_queryset:
            ret.append({
                'id': member.id,
                'username': member.username,
                'name': member.name,
                'phone': member.phone
            })
        return ret

    def to_representation(self, instance):
        members = self.to_members_response(instance.user_set.all())
        number = instance.user_set.count()
        power = self.to_permission_response(instance.permissions.all())
        ret = super(Groupserializer, self).to_representation(instance)
        ret["members"] = members
        ret["number"] = number
        ret["power"] = power
        return ret

    class Meta:
        model = Group
        fields = ("id", "name")


# class ContentTypeSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = ContentType
#         fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):
    # content_type = ContentTypeSerializer()

    class Meta:
        model = Permission
        fields = ("id", "name", "codename")