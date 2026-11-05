import logging
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import Word, Wordtype
from ..serializers import WordSerializer, WordCustomSerializer, WordRawSerializer, WordFlatSerializer, \
    WordtypeSerializer

logger = logging.getLogger('django')

#
#
# Function Based Views with decorators
# !!! The browsable API only works with Response not with JsonResponse
# GET /api/functionbased/words/
# GET /api/functionbased/words/?wordtype=3
# GET /api/functionbased/words/?wordtype=3&level=1
# add to __init__.py
#
#


@api_view(['GET', 'POST'])
def word_list(request):
    if request.method == 'GET':
        wordtype_filter = request.query_params.get('wordtype')
        level_filter = request.query_params.get('level')
        if wordtype_filter is not None and level_filter is not None:
            logger.info('Applied two filters')
            # AND Filter
            words = Word.objects.filter(wordtype=wordtype_filter, level=level_filter).select_related(
                'wordtype').all()
        elif wordtype_filter is not None:
            logger.info('Applied wordtype_filter')
            words = Word.objects.filter(wordtype=wordtype_filter).select_related(
                'wordtype').all()
        elif level_filter is not None:
            logger.info('Applied level_filter')
            words = Word.objects.filter(level=level_filter).select_related(
                'wordtype').all()
        else:
            logger.info('Applied no filter')
            # lazy load data
            # words = Word.objects.all()
            # eager load data table with select_related, Chaining select_related is possible
            words = Word.objects.select_related('wordtype').all()

        # serialize a list (Many=True)
        #serializer = WordCustomSerializer(words, many=True)
        #serializer = WordRawSerializer(words, many=True)
        serializer = WordSerializer(words, many=True)
        # return, in order to allow non-dict objects to be serializes set the safe param to False
        # variant flat list
        # The browsable API only works with Response not with JsonResponse
        #return JsonResponse(serializer.data, safe=False)
        # variant named list
        # The browsable API only works with Response not with JsonResponse
        #return JsonResponse({"words": serializer.data}, safe=False)
        return Response(serializer.data)
    if request.method == 'POST':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    # or 400
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

#
#
# Function Based Views with id as path parameter
# !!! The browsable API only works with Response not with JsonResponse
#
#
@api_view(['GET', 'PUT', 'DELETE'])
def word_details(request, id):
    try:
        #word = Word.objects.select_related('wordtype').get(pk=id)
        word = Word.objects.get(pk=id)
    except Word.DoesNotExist:
        # If get() doesn’t find any object, it raises a Model. DoesNotExist exception:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # using WordFlatSerializer with lazy load
    if request.method == 'GET':
        serializer = WordFlatSerializer(word)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = WordFlatSerializer(word, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        word.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # or 400
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

#
#
# wordtype_list
#
#
@api_view(['GET'])
def wordtype_list(request):
    if request.method == 'GET':
        # lazy load data
        wordtypes = Wordtype.objects.all()
        serializer = WordtypeSerializer(wordtypes, many=True)
        return Response(serializer.data)
    # or 400
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

#
#
# wordtype_details
#
#
@api_view(['GET', 'PUT', 'DELETE'])
def wordtype_details(request, id):
    try:
        wordtype = Wordtype.objects.get(pk=id)
    except Wordtype.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WordtypeSerializer(wordtype)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = WordtypeSerializer(wordtype, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # check: Cannot delete some instances of model 'Wordtype' because they are referenced through
        # restricted foreign keys
        wordtype.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # or 400
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)