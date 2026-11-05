from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from spanishtrainer_api.models import Word, Wordtype, Category, WordCategory, User
from spanishtrainer_api.permissions import IsContentUser, IsContentAdmin
from spanishtrainer_api.serializers import WordFlatSerializer, WordSerializer, WordtypeSerializer, \
    CategorySerializer, WordCategorySerializer, ContentUserRegisterSerializer
from spanishtrainer_api.filters import WordFilter

# --------------------------------------------------------------------------------------------------
#
# Views for Register User
# The password is hashed in the serializer
#
# --------------------------------------------------------------------------------------------------
class ContentUserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ContentUserRegisterSerializer


# --------------------------------------------------------------------------------------------------
#
# Views for Word / WordList
#
# --------------------------------------------------------------------------------------------------
# One class for GET and POST using ListCreateAPIView and one URL
# GET /api/generic/words/
# POST /api/generic/words/
class WordListCreateAPIView(generics.ListCreateAPIView):
    queryset = Word.objects.all()
    serializer_class = WordFlatSerializer
    # define filter directly without FilterSet
    #filterset_fields = ['level', 'wordtype']
    filterset_class = WordFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    #search_fields = ['=es', '=de']
    search_fields = ['es', 'de']
    ordering_fields = ['id', 'es', 'de', 'level', 'wordtype', 'seqnumber']
    # example: ?search=Buen
    # example: ?search=Hola
    # example: ?search=Hallo
    # example: ?ordering=de

    # override
    def get_permissions(self):
        if self.request.method == 'GET':
            print("GET WordListCreateAPIView...")
            self.permission_classes = [AllowAny]
        else:
            # IsAuthenticated, IsAdminUser, etc
            # if not Authenticated: HTTP 403 Forbidden
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

# Variant: Get a list of Words with ListAPIView and a GET Request
# GET /api/generic/words/
class WordListAPIView(generics.ListAPIView):
    queryset = Word.objects.all()
    serializer_class = WordFlatSerializer

# Variant: Create a single Word with CreateAPIView and a POST Request
# with a special path in urls.py (not recommended)
# POST /api/generic/words/create
class WordCreateAPIView(generics.CreateAPIView):
    model = Word
    serializer_class = WordFlatSerializer
    # override some method
    def create(selfself, request, *args, **kwargs):
        print(request.data)
        return super().create()

# Variant: RetrieveAPIView for GET /api/generic/words/34
class WordDetailAPIView(generics.RetrieveAPIView):
    # Flat Loading
    #queryset = Word.objects.all()
    # Eager Loading / select_related 1:n, chaining if more than on
    queryset = Word.objects.select_related('wordtype')
    # Eager Loading / prefetch_related m:n
    #queryset = Word.objects.prefetch_related('categories').all()
    serializer_class = WordSerializer
    # change lookup fields from default <int:pk> to <int:id>
    lookup_url_kwarg = "id"

# Variant: RetrieveUpdateDestroyAPIView for GET, PUT, PATCH, DELETE with id path parameter
# GET /api/generic/words/34
# DELETE /api/generic/words/34
# PUT/PATCH /api/generic/words/34
class WordDetailRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    # change lookup fields from default <int:pk> to <int:id>
    lookup_url_kwarg = "id"

    # IsAuthenticatedOrReadOnly:
    # Allow read - only access to anonymous users and full access to authenticated users.
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated, IsContentAdmin]
        return super().get_permissions()

    # override get_permissions
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         print("get_permissions: AllowAny")
    #         self.permission_classes = [AllowAny]
        # else:
        #     print("get_permissions: IsAuthenticated, IsContentUser")
        #     self.permission_classes = [IsAuthenticated, IsContentUser]

        # elif self.request.user.is_authenticated:
        #     print("user is authenticated")
        #     user = self.request.user
        #     # debug info
        #     print("user is in groups:")
        #     for group in user.groups.all():
        #         print(group)
        #     # Check whether the user is in the ContentUser group
        #     if user.groups.filter(name="ContentUser").exists():
        #         print("User is in group!")
        #     else:
        #         print("User is not in group!")
        #         raise PermissionDenied('User is authenticated but not allowed to write, update or delete data in this table')
        # else:
        #     print("user is not authenticated and request is not GET")
        #     raise PermissionDenied('User is not authenticated and not allowed to write, update or delete data in this table')
        # return super().get_permissions()

    # override to get QuerySet, for GET some related data is returned
    def get_queryset(self):
        if self.request.method == 'GET':
            # Eager Loading / select_related 1:n, chaining if more than on
            # queryset = Word.objects.select_related('wordtype')
            # Eager Loading / prefetch_related m:n
            # queryset = Word.objects.prefetch_related('categories').all()
            return Word.objects.select_related('wordtype')
        else:
            # Flat/Lazy Loading (no related tables)
            return Word.objects.all()

    # override to get Serializer
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WordSerializer
        else:
            return WordFlatSerializer


# --------------------------------------------------------------------------------------------------
#
# Views for Wordtype / WordtypeList
#
# --------------------------------------------------------------------------------------------------
# GET /api/generic/wordtypes/
class WordTypeListAPIView(generics.ListAPIView):
    queryset = Wordtype.objects.all()
    serializer_class = WordtypeSerializer


# --------------------------------------------------------------------------------------------------
#
# Views for Category / CategoryList
#
# --------------------------------------------------------------------------------------------------
# unused (GET /api/generic/categorys/)
class CategoryFlatListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# GET /api/generic/categorys/
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer

# GET /api/generic/categorys/
class CategoryDetailRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_url_kwarg = "categoryid"

# Get a list of Words with ListAPIView from a one Category (lookup_url_kwarg=categoryid)
# GET /api/generic/categorys/1/words
class CategoryWordListAPIView(generics.ListAPIView):
    lookup_url_kwarg = "categoryid"
    serializer_class = WordCategorySerializer

    def get_queryset(self):
        catId = self.kwargs["categoryid"]
        # print(self.kwargs["categoryid"])
        # print(self.kwargs[self.lookup_url_kwarg])
        return Word.objects.filter(categories=catId).prefetch_related('categories')

# (Add an existing word to an existing category)
# unused (POST /api/generic/categorys/1/words/78)
class AddWordToCategoryCreateAPIView(generics.CreateAPIView):
    lookup_fields = ('categoryid', 'wordid')
    # This will return to you true/false values
    # wordExists = Word.objects.filter(id='name').exists()
    # categoryExists = Category.objects.filter(id='name').exists()
    # no body data, cause objects already exists
    model = None
    serializer_class = WordCategorySerializer

    def get_object(self, queryset=None):
        catId = self.kwargs["categoryid"]
        wordId = self.kwargs["wordid"]
        print(catId)
        print(wordId)
        return None

#
#
# HTTP POST without entity body
# Add an existing word to an existing category
# POST /api/generic/categorys/1/words/78
#
@api_view(['POST'])
def addWordToCategory(request, categoryid, wordid):
    # try:
    wordExists = Word.objects.filter(id=wordid).exists()
    categoryExists = Category.objects.filter(id=categoryid).exists()
    if wordExists and categoryExists:
        word = Word.objects.get(pk=wordid)
        category = Category.objects.get(pk=categoryid)
        instance = WordCategory(word=word, category=category, seqnumber=0)
        instance.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # except:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
