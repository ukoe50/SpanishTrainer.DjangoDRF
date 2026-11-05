import logging
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import *
from ..serializers import *

logger = logging.getLogger('django')

#
#
# Class-based Views (using APIView)
# can be easily converted from functionbased views
# with seperate classes for List and Details
# GET /api/classbased/words/
# GET /api/classbased/words/23
# add to __init__.py
#

class WordList(APIView):
    def get(self, request):
        words = Word.objects.all()
        serializer = WordFlatSerializer(words, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WordFlatSerializer(data=request.data, many=False)
        if serializer.is_valid():
            print(f"word not found, create new")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def createWithSoftCheck(self, request):
        serializer = WordFlatSerializer(data=request.data, many=False)
        # response = HttpResponse(content="", status=303)
        # response["Location"] = "http://example.com/redirect/here/"
        if serializer.is_valid():
            # check with 'like' if word exists already with same wordtype (not using unique constraint from database)
            print(f"Checking incoming word: {serializer.data['de']} with wordtype {serializer.data['wordtype']}")
            # execute WHERE de LIKE '%someting%'
            # __contains for having the case sensitivity
            # __icontains to ignore case sensitivity
            # first()¶
            # Returns the first object matched by the queryset, or None if there is no matching object
            wordExisting = Word.objects.filter(de__contains=serializer.data['de'], wordtype=serializer.data['wordtype']).first()
            # wordEsExisting = Word.objects.get(es__contains=serializer.data['es'])
            if wordExisting is None:
                print(f"word not found, create new")
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(f"first word found: {wordExisting.de} with matching wordtype: {wordExisting.wordtype.id}")
                wordExistingSerializer = WordFlatSerializer(wordExisting)
                return Response(wordExistingSerializer.data, status=status.HTTP_303_SEE_OTHER)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WordDetail(APIView):
    def get(self, request, id):
        # very short variant
        #word = get_object_or_404(Word, pk=id)
        try:
            # return some additional related data
            word = Word.objects.select_related('wordtype').get(pk=id)
        except Word.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WordSerializer(word)
        # this will cause an error here:
        #print(serializer.is_valid())  # False
        #print(serializer.errors)
        return Response(serializer.data)

    def put(self, request, id):
        #word = get_object_or_404(Word, pk=id)
        try:
            word = Word.objects.get(pk=id)
        except Word.DoesNotExist:
             return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = WordFlatSerializer(word, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        word = get_object_or_404(Word, pk=id)
        word.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)