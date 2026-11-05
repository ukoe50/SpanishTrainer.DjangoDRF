from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from spanishtrainer_api.managers import MyUserManager

DBSCHEMA_NAME = 'est.'

# TODOS:
# Unique de field in Word Table
# Get the articles out of the Word table or a way to handle articles (WordType:Substantive)
# Full Text Search before inserting Words


#
# User
# If you’re starting a new project, you can set up a custom user model that behaves identically
# to the default user model by subclassing AbstractUser
# Also, register the model in the app’s admin.py
#
class User(AbstractUser):
    objects = MyUserManager()

#
# Wordtype
# adjective, verb, etc
#
class Wordtype(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name_en = models.CharField(max_length=50, unique=True)
    name_de = models.CharField(max_length=50, unique=True)
    name_es = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = DBSCHEMA_NAME + "wordtype"

    def __str__(self):
        return self.name_en

#
# Category (relation m:n to Words)
# self-referential foreign key: parent
#
class Category(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name_en = models.CharField(max_length=50, unique=True)
    name_de = models.CharField(max_length=50, unique=True)
    name_es = models.CharField(max_length=50, unique=True)
    # The related_name attribute specifies the name of the reverse relation
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    seqnumber = models.IntegerField(blank=True, null=True)
    level = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = DBSCHEMA_NAME + "category"

    # @property
    def isChild(self):
         return self.parent is not None

#
# Sentence
# django > 3.0 - have built-in support for Enums
#
class Sentence(models.Model):
    id = models.AutoField(primary_key=True)
    es = models.CharField(max_length=200)
    de = models.CharField(max_length=200)
    level = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = DBSCHEMA_NAME + "sentence"

#
# Word (relation m:n to Category)
# a word can be in multiple categories
# the wordtype_id column is generated automatically
# UPDATE word_es_de
# SET seqnumber=null
# WHERE seqnumber=''
#
class Word(models.Model):
    id = models.AutoField(primary_key=True)
    es = models.CharField(max_length=50)
    de = models.CharField(max_length=50)
    plural_es = models.CharField(max_length=50, blank=True, null=True)
    plural_de = models.CharField(max_length=50, blank=True, null=True)
    # Prevent deletion of the referenced object by raising RestrictedError
    wordtype = models.ForeignKey(Wordtype, on_delete=models.RESTRICT, null=True)
    level = models.SmallIntegerField(blank=True, null=True)
    genus = models.CharField(max_length=1, blank=True, null=True)
    # blank=True for int-type, in SQLLite this is a possible, not recommended!
    seqnumber = models.IntegerField(blank=True, null=True)
    verbstem = models.CharField(max_length=50, blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True)
    categories = models.ManyToManyField(Category, through='WordCategory')
    sentences = models.ManyToManyField(Sentence, through='WordSentence')

    class Meta:
        db_table = DBSCHEMA_NAME + "word"

#
# word_category (Bridgetable)
#
class WordCategory(models.Model):
    pk = models.CompositePrimaryKey("word_id", "category_id")
    word = models.ForeignKey(Word, on_delete=models.CASCADE, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    seqnumber = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = DBSCHEMA_NAME + "word_category"

#
# sentence_category (Bridgetable)
#
class SentenceCategory(models.Model):
    pk = models.CompositePrimaryKey("sentence_id", "category_id")
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    seqnumber = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = DBSCHEMA_NAME + "sentence_category"

#
# Lang
# with country icon as BinaryField
# is a special field to store raw binary data. It can be assigned bytes, bytearray, or memoryview
#
class Lang(models.Model):
    id = models.SmallAutoField(primary_key=True)
    code_639_1 = models.CharField(max_length=2)
    name_en = models.CharField(max_length=50)
    name_de = models.CharField(max_length=50)
    name_es = models.CharField(max_length=50)
    icon = models.BinaryField(blank=True, null=True)

    class Meta:
        db_table = DBSCHEMA_NAME + "lang"

#
# LookupGrouped
# static common multi language fields, for example group=Personalpronouns
#
class LookupGroup(models.Model):
    id = models.AutoField(primary_key=True)
    lang = models.CharField(max_length=2, blank=False, null=False)
    group = models.CharField(max_length=50, blank=False, null=False)
    field = models.CharField(max_length=50, blank=True, null=True)
    content = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = DBSCHEMA_NAME + "lookup_group"

#
# Verb
#
# class Verb(models.Model):
#     es_infinitive = models.CharField(max_length=50)
#     de_infinitive = models.CharField(max_length=50)
#     level = models.SmallIntegerField(blank=True, null=True)
#
#     class Meta:
#         db_table = 'verb'

#
# Tense
# for example: present, past, future
#
class Tense(models.Model):
    id = models.AutoField(primary_key=True)
    name_en = models.CharField(max_length=50)
    name_de = models.CharField(max_length=50)
    name_es = models.CharField(max_length=50)

    class Meta:
        db_table = DBSCHEMA_NAME + "tense"

#
# Conjugation
#
# class Conjugation(models.Model):
#     id = models.AutoField(primary_key=True)
#     lang = models.CharField(max_length=2, blank=False, null=False)
#     verb = models.ForeignKey(Word, on_delete=models.RESTRICT, null=False)
#     tense = models.ForeignKey(Tense, on_delete=models.RESTRICT, null=False)
#     field = models.CharField(max_length=50, default="")
#     regular = models.BooleanField(blank=True, null=True)
#     rule = models.CharField(max_length=50, blank=True, null=True)
#     content = models.CharField(max_length=100, blank=True, null=True)
#
#     class Meta:
#         db_table = DBSCHEMA_NAME + "conjugation"


#
# Rule
#
class Rule(models.Model):
    id = models.AutoField(primary_key=True)
    name_en = models.CharField(max_length=50)
    name_de = models.CharField(max_length=50)
    name_es = models.CharField(max_length=50)
    comment = models.CharField(max_length=200)

    class Meta:
        db_table = DBSCHEMA_NAME + "rule"

#
# VerbPresent
#
class VerbPresent(models.Model):
    id = models.AutoField(primary_key=True)
    lang = models.CharField(max_length=2, blank=False, null=False)
    verb = models.ForeignKey(Word, on_delete=models.RESTRICT, null=False)
    tense = models.ForeignKey(Tense, on_delete=models.RESTRICT, null=False)
    #field = models.CharField(max_length=50, default="")
    regular = models.BooleanField(blank=True, null=True)
    rule = models.ForeignKey(Rule, on_delete=models.RESTRICT, null=True)
    sing1 = models.CharField(max_length=50, blank=True, null=True)
    sing2 = models.CharField(max_length=50, blank=True, null=True)
    sing3 = models.CharField(max_length=50, blank=True, null=True)
    plural1 = models.CharField(max_length=50, blank=True, null=True)
    plural2 = models.CharField(max_length=50, blank=True, null=True)
    plural3 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = DBSCHEMA_NAME + "verb_present"


#
# UserBook
#
class UserBook(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=2, blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # username = models.CharField(max_length=50, blank=True, null=True)
    # userid = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = DBSCHEMA_NAME + "user_book"

#
# UserBookContent
#
class UserBookContent(models.Model):
    id = models.AutoField(primary_key=True)
    userbook = models.ForeignKey(UserBook, on_delete=models.RESTRICT, null=False)
    word = models.ForeignKey(Word, on_delete=models.RESTRICT, null=True)
    sentence = models.ForeignKey(Sentence, on_delete=models.RESTRICT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    repetitionCount = models.IntegerField(blank=True, null=True)
    markedforreptition = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    seqnumber = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = DBSCHEMA_NAME + "user_book_content"


#
# PracticeState
#
# class PracticeState(models.Model):
#     id = models.AutoField(primary_key=True)
#     userbook = models.ForeignKey(UserBook, on_delete=models.RESTRICT, null=False)
#     word = models.ForeignKey(Word, on_delete=models.RESTRICT, null=True)
#     sentence = models.ForeignKey(Sentence, on_delete=models.RESTRICT, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     practiceState =
#
#     class Meta:
#         db_table = DBSCHEMA_NAME + "practicestate"

#
# WordSentence (Bridgetable)
#
class WordSentence(models.Model):
    pk = models.CompositePrimaryKey("word_id", "sentence_id")
    word = models.ForeignKey(Word, on_delete=models.CASCADE, null=False)
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, null=False)
    seqnumber = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = DBSCHEMA_NAME + "word_sentence"