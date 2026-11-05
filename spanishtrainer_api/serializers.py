import logging

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Word, Category, User
from .models import Wordtype

logger = logging.getLogger('django')

#
#
# ContentUserRegisterSerializer
# create logic for User in a specific role
# override creates and validate
# check manually if password is hashed in db!
#
#
class ContentUserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(required=False, max_length=150)
    last_name = serializers.CharField(required=False, max_length=150)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        if attrs.get('first_name') is None:
            attrs['first_name'] = ""
        if attrs.get('last_name') is None:
            attrs['last_name'] = ""
        print("first_name: " + attrs['first_name'])
        print("last_name: " + attrs['last_name'])
        return attrs

    def create(self, validated_data):
        # debug
        print("all group names:")
        for group in Group.objects.all():
            print(group.name)
        group_ContentUser = Group.objects.get(name='ContentUser')
        print("validated_data['first_name']: " + validated_data['first_name'])
        print("validated_data['last_name']: " + validated_data['last_name'])
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        print("user added created and saved:" + user.email)
        group_ContentUser.user_set.add(user)
        print("user added to group:" + group_ContentUser.name)
        return user

#
#
# Word Raw Serializer
# inherit from serializers.Serializer
#
#
class WordRawSerializer(serializers.Serializer):
    # Built-in Validation
    # es = serializers.CharField(max_length=100, min_length=3, required=True)
    # email = serializers.EmailField(required=True)
    id = serializers.IntegerField()
    es = serializers.CharField(max_length=50)
    de = serializers.CharField(max_length=50)

#
#
# Flat Fields ModelSerializer
# with flat data fields
# A ModelSerializer is a shortcut to create serializers for Django models
#
#
class WordFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'es', 'de', 'wordtype', 'level', 'seqnumber', 'genus']

    # Object-Level Validation (override)
    # def validate(self, data):
    #     logger.info('Applied WordFlatSerializer.validate')
    #     if data['es'] != data['de']:
    #         raise serializers.ValidationError("Words do not match.")
    #     return data

    # Custom field validation
    # The validation method needs to be named like so: validate_<field_name>
    def validate_level(self, value):
        if value < 1:
            raise serializers.ValidationError("must be blank or bigger than zero")
        return value

    # Custom field validation
    def validate_seqnumber(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("must be blank, zero or greater than zero")
        return value

#
#
# 1:n Nested ModelSerializer
# with nested/relational data 1:n and including the related object as a nested object in json
#
#
class WordtypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wordtype
        fields = ['id', 'name_en', 'name_de', 'name_es']

class WordSerializer(serializers.ModelSerializer):
    # the data is already loaded with eager load/select_related
    # the relation name 'wordtype' has to match exactly with the model
    wordtype = WordtypeSerializer(many=False)
    class Meta:
        model = Word
        fields = ['id', 'es', 'de', 'wordtype', 'level', 'seqnumber', 'genus']

#
#
# m:n WordCategorySerializer
#
#
class CategoryNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name_en', 'name_de', 'name_es', 'seqnumber', 'level']

class WordCategorySerializer(serializers.ModelSerializer):
    # the data is already loaded with eager load/prefetch_related
    categories = CategoryNestedSerializer(many=True)
    class Meta:
        model = Word
        fields = ['id', 'es', 'de', 'wordtype', 'level', 'seqnumber', 'genus', 'categories']

#
#
# 1:n Overriden Custom ModelSerializer
# Override BaseSerializer can be used to easily support alternative serialization and deserialization styles
# https://www.django-rest-framework.org/api-guide/serializers/#baseserializer
#
#
class WordtypeCustom2Serializer(serializers.BaseSerializer):
    # override variant: return a new object with many fields
    def to_representation(self, instance):
        return {
            'wordtype_name': instance.name_en,
            'wordtype_id': instance.id
        }

class WordtypeCustom1Serializer(serializers.BaseSerializer):
    # override variant: return one field without brackets
    def to_representation(self, instance):
        return instance.name_en

class WordCustomSerializer(serializers.ModelSerializer):
    # the data is already loaded with eager load/select_related
    # the relation name 'wordtype' has to match exactly with the model
    wordtype = WordtypeCustom1Serializer(many=False)
    class Meta:
        model = Word
        fields = ['id', 'es', 'de', 'wordtype', 'level', 'seqnumber', 'genus']

#
#
# WordtypeSerializer
#
#
class WordtypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wordtype
        fields = ['id', 'name_en', 'name_de', 'name_es']

#
#
# Flat CategorySerializer
#
#
class CategoryFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name_en', 'name_de', 'name_es', 'parent', 'seqnumber', 'level', 'isChild']

#
#
# Tree CategorySerializer with nested childs/subCategories
#
#
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name_en', 'name_de', 'name_es', 'parent', 'seqnumber', 'level', 'isChild']

class CategorySerializer(serializers.ModelSerializer):
    parentCategory = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    subcategories = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['parentCategory', 'id', 'name_en', 'name_de', 'name_es', 'parent', 'seqnumber', 'level', 'isChild', 'subcategories']
