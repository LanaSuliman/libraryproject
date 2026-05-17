from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import Book, Student, Publisher, Author, Student2,Product
from .forms import BookForm, StudentForm, Student2Form,ProductForm
from django.db.models import Q, Count, Sum, Avg, Max, Min, OuterRef, Subquery
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

def lab9_task1(request):
    books = Book.objects.all()

    total_quantity = Book.objects.aggregate(total=Sum('quantity'))['total']

    for book in books:
        if total_quantity:
            book.availability_percentage = round((book.quantity / total_quantity) * 100, 2)
        else:
            book.availability_percentage = 0

    return render(request, 'bookmodule/lab9_task1.html', {'books': books})

def lab9_task2(request):
    publishers = Publisher.objects.values('name', 'location').annotate(
        total_stock=Sum('book__quantity')
    )

    return render(request, 'bookmodule/lab9_task2.html', {'publishers': publishers})
def lab9_task3(request):
    publisher_groups = Publisher.objects.values('name', 'location').distinct()

    publishers = []

    for publisher in publisher_groups:
        oldest_book = Book.objects.filter(
            publisher__name=publisher['name'],
            publisher__location=publisher['location'],
            pubdate__isnull=False
        ).order_by('pubdate').first()

        publishers.append({
            'name': publisher['name'],
            'location': publisher['location'],
            'oldest_book_title': oldest_book.title if oldest_book else 'No book',
            'oldest_book_date': oldest_book.pubdate if oldest_book else 'No date'
        })

    return render(request, 'bookmodule/lab9_task3.html', {'publishers': publishers})

def lab9_task4(request):
    publishers = Publisher.objects.values('name', 'location').annotate(
        average_price=Avg('book__price'),
        min_price=Min('book__price'),
        max_price=Max('book__price')
    )

    return render(request, 'bookmodule/lab9_task4.html', {'publishers': publishers})

def lab9_task5(request):
    publishers = Publisher.objects.values('name', 'location').annotate(
        highly_rated_books=Count('book', filter=Q(book__rating__gte=4)),
        total_quantity=Sum('book__quantity', filter=Q(book__rating__gte=4))
    )

    return render(request, 'bookmodule/lab9_task5.html', {'publishers': publishers})
def lab9_task6(request):
    publishers = Publisher.objects.values('name', 'location').annotate(
        books_count=Count(
            'book',
            filter=Q(book__price__gt=50, book__quantity__lt=5, book__quantity__gte=1)
        )
    )

    return render(request, 'bookmodule/lab9_task6.html', {'publishers': publishers})
def list_books_lab9_part1(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/lab9_part1_listbooks.html', {'books': books})
def add_book_lab9_part1(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        price = request.POST.get("price")
        edition = request.POST.get("edition")
        quantity = request.POST.get("quantity")

        Book.objects.create(
            title=title,
            author=author,
            price=price,
            edition=edition,
            quantity=quantity
        )

        return redirect("list_books_lab9_part1")

    return render(request, "bookmodule/lab9_part1_addbook.html")
def edit_book_lab9_part1(request, id):
    book = Book.objects.get(id=id)

    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.price = request.POST.get("price")
        book.edition = request.POST.get("edition")
        book.quantity = request.POST.get("quantity")

        book.save()

        return redirect("list_books_lab9_part1")

    return render(request, "bookmodule/lab9_part1_editbook.html", {"book": book})

def delete_book_lab9_part1(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect("list_books_lab9_part1")
def list_books_lab9_part2(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/lab9_part2_listbooks.html', {'books': books})
def add_book_lab9_part2(request):
    if request.method == "POST":
        form = BookForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("list_books_lab9_part2")
    else:
        form = BookForm()

    return render(request, "bookmodule/lab9_part2_addbook.html", {"form": form})

def edit_book_lab9_part2(request, id):
    book = Book.objects.get(id=id)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            form.save()
            return redirect("list_books_lab9_part2")
    else:
        form = BookForm(instance=book)

    return render(request, "bookmodule/lab9_part2_editbook.html", {"form": form, "book": book})

def delete_book_lab9_part2(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect("list_books_lab9_part2")


def list_students(request):
    students = Student.objects.all()
    return render(request, 'bookmodule/lab11/list_students.html', {'students': students})


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('list_students')
    else:
        form = StudentForm()

    return render(request, 'bookmodule/lab11/student_form.html', {'form': form})


def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect('list_students')
    else:
        form = StudentForm(instance=student)

    return render(request, 'bookmodule/lab11/student_form.html', {'form': form})


def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.delete()
        return redirect('list_students')

    return render(request, 'bookmodule/lab11/delete_student.html', {'student': student})

def list_students2(request):
    students = Student2.objects.all()
    return render(request, 'bookmodule/lab11/list_students2.html', {'students': students})
def add_student2(request):
    if request.method == 'POST':
        form = Student2Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_students2')
    else:
        form = Student2Form()
    return render(request, 'bookmodule/lab11/student2_form.html', {'form': form})
def edit_student2(request, id):
    student = get_object_or_404(Student2, id=id)

    if request.method == 'POST':
        form = Student2Form(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect('list_students2')
    else:
        form = Student2Form(instance=student)
    return render(request, 'bookmodule/lab11/student2_form.html', {'form': form})
def delete_student2(request, id):
    student = get_object_or_404(Student2, id=id)
    if request.method == 'POST':
        student.delete()
        return redirect('list_students2')
    return render(request, 'bookmodule/lab11/delete_student2.html', {'student': student})
def list_products(request):
    products = Product.objects.all()
    return render(request, 'bookmodule/lab11/list_products.html', {'products': products})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('list_products')
    else:
        form = ProductForm()

    return render(request, 'bookmodule/lab11/product_form.html', {'form': form})