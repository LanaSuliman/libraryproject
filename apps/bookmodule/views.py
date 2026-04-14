from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Student
from django.db.models import Q, Count, Sum, Avg, Max, Min

def index(request):
    return render(request, "bookmodule/index.html")


def index_lab3(request):
    name = request.GET.get("name") or "world!"
    return render(request, "bookmodule/index.html", {"name": name})


def index2(request, val1=0):
    return HttpResponse("value1 = " + str(val1))


def index2_text(request, val1=""):
    return HttpResponse("error, expected val1 to be integer")


def list_books(request):
    return render(request, "bookmodule/list_books.html")


def aboutus(request):
    return render(request, "bookmodule/aboutus.html")


def viewbook(request, bookId):
    return render(request, "bookmodule/one_book.html")


def viewbook_lab3(request, bookId):
    book1 = {'id': 123, 'title': 'Continuous Delivery', 'author': 'J. Humble and D. Farley'}
    book2 = {'id': 456, 'title': 'Secrets of Reverse Engineering', 'author': 'E. Eilam'}

    targetBook = None
    if book1['id'] == bookId:
        targetBook = book1
    if book2['id'] == bookId:
        targetBook = book2

    context = {'book': targetBook}
    return render(request, "bookmodule/show.html", context)


def html5_links(request):
    return render(request, "bookmodule/html5/links.html")


def html5_formatting(request):
    return render(request, "bookmodule/html5/text/formatting.html")


def html5_listing(request):
    return render(request, "bookmodule/html5/listing.html")


def html5_tables(request):
    return render(request, "bookmodule/html5/tables.html")


def __getBooksList():
    book1 = {'id': 12344321, 'title': 'Continuous Delivery', 'author': 'J.Humble and D. Farley'}
    book2 = {'id': 56788765, 'title': 'Reversing: Secrets of Reverse Engineering', 'author': 'E. Eilam'}
    book3 = {'id': 43211234, 'title': 'The Hundred-Page Machine Learning Book', 'author': 'Andriy Burkov'}
    return [book1, book2, book3]


def search_books(request):
    if request.method == "POST":
        string = request.POST.get('keyword', '').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')

        books = __getBooksList()
        newBooks = []

        for item in books:
            contained = False

            if isTitle and string in item['title'].lower():
                contained = True

            if not contained and isAuthor and string in item['author'].lower():
                contained = True

            if contained:
                newBooks.append(item)

        return render(request, "bookmodule/bookList.html", {'books': newBooks})
    return render(request, "bookmodule/search.html")


def simple_query(request):
    mybooks = Book.objects.filter(title__icontains='and')
    return render(request, "bookmodule/bookList.html", {'books': mybooks})


def complex_query(request):
    mybooks = Book.objects.filter(
        author__isnull=False
    ).filter(
        title__icontains='and'
    ).filter(
        edition__gte=2
    ).exclude(
        price__lte=100
    )[:10]

    if len(mybooks) >= 1:
        return render(request, "bookmodule/bookList.html", {'books': mybooks})
    else:
        return render(request, "bookmodule/index.html")
def lab8_task1(request):
        books = Book.objects.filter(Q(price__lte=80))
        return render(request, "bookmodule/lab8_task1.html", {'books': books})
def lab8_task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) & (Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, "bookmodule/lab8_task2.html", {'books': books})
def lab8_task3(request):
    books = Book.objects.filter(
        Q(edition__lte=3) & ~(Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, "bookmodule/lab8_task3.html", {'books': books})
def lab8_task4(request):
    books = Book.objects.order_by('title')
    return render(request, "bookmodule/lab8_task4.html", {'books': books})
def lab8_task5(request):
    stats = Book.objects.aggregate(
        total_books=Count('id'),
        total_price=Sum('price'),
        average_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price')
    )
    return render(request, "bookmodule/lab8_task5.html", {'stats': stats})
def lab8_task7(request):
    students_per_city = Student.objects.values('address__city').annotate(total_students=Count('id'))
    return render(request, "bookmodule/lab8_task7.html", {'students_per_city': students_per_city})
