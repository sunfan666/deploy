from rest_framework import serializers                                 
from .models import Publish, Author, Book


class PublishSerializer(serializers.ModelSerializer):      
    class Meta: 
        model = Publish                                                  
        fields = "__all__"       

    # def create(self, validated_data):
    #     print(validated_data)
    #     instance = self.Meta.model.objects.create(**validated_data)
    #     return instance
    #
    # def update(self, instance, validated_data):
    #     print(instance)
    #     print(instance.id)
    #     print(validated_data)
    #     self.Meta.model.objects.filter(id=instance.id).update(**validated_data)
    #     return instance


class AuthorSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Author
        fields = "__all__"

    # def create(self, validated_data):
    #     instance = self.Meta.model.objects.create(**validated_data)
    #     return instance
    #
    # def update(self, instance, validated_data):
    #     self.Meta.model.objects.filter(id=instance.id).update(**validated_data)
    #     return instance


class BookSerializer(serializers.ModelSerializer):
    #publisher = PublishSerializer()         # 默认显示PublishSerializer定义的所有列
    #authors = AuthorSerializer(many=True)   # 默认显示AuthorSerializer所有的列

    class Meta:
        model = Book 
        fields = "__all__"

    def to_author_response(self, author_queryset):
        ret = []
        # 多对多的结果是一个列表对象，需要遍历对象，将需要序列化的内容提出来即可
        for author in author_queryset:
            ret.append({
                'id': author.id,
                'name': author.name,
                'email': author.email
            })
        return ret

    def to_representation(self, instance):
        #print(instance)
        publisher_obj = instance.publisher
        #print(publisher_obj)
        authors = self.to_author_response(instance.authors.all())
        author_queryset = instance.authors.all()
        #print(author_queryset)
        #print(authors)

        ret = super(BookSerializer, self).to_representation(instance)
        ret["publisher"] = {
            "id": publisher_obj.id,
            "name": publisher_obj.name,
            "address": publisher_obj.address,
        },
        ret["authors"] = authors
        return ret

    # def create(self, validated_data):
    #     print(validated_data)
    #     author_list = validated_data.pop('authors', [])
    #     print(author_list)
    #     print(validated_data)
    #     instance = self.Meta.model.objects.create(**validated_data)
    #     # author和book是多对多关系，添加数据时需要单独处理
    #     instance.authors.set(author_list)
    #     return instance
    #
    # def update(self, instance, validated_data):
    #     print(validated_data)
    #     author_list = validated_data.pop('authors', [])
    #     print(author_list)
    #     self.Meta.model.objects.filter(id=instance.id).update(**validated_data)
    #     # 多对多添加的两种写法
    #     instance.authors.set(author_list)
    #     return instance


