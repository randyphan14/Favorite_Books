from django.shortcuts import render, redirect
from appy.models import User, Book, Review, Author
from django.contrib import messages
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request,"index.html")

def addUser(request):
    # this is the route that processes the new show

    errors = User.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        decoded_hash = hashed.decode('utf-8')

        user = User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=decoded_hash)
        print(user)
        # request.session['u_id'] = user.id
        # request.session['u_fname'] = user.first_name

        request.session['u_id'] = user.id
       
        return redirect('/books')

def checkOldUser(request):
    # this is the route that processes the new show
    user_list = User.objects.filter(email=request.POST['email'])
    if not user_list:
        messages.error(request, "Invalid credentials!")
        return redirect('/')
   
    user = user_list[0]
    request.session['u_id'] = user.id
   
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        

        return redirect('/books')
        # return render(request,"success.html", context)
    else:
        messages.error(request, "Invalid credentials!")
        return redirect('/')

def successful(request):
    context = {
        "books": Book.objects.all(),
        "reviews": Review.objects.all().order_by("-created_at")[:3],
        "user": User.objects.get(id = request.session['u_id']),
    }
    return render(request,"success.html", context)

def clear(request):
    request.session.clear()
    return redirect("/")

def addBookPage(request):
    context = {
        "authors": Author.objects.all()
    }
    return render(request,"addBook.html", context)

def addBook(request):
    if request.method == 'POST':
        new_book = Book.objects.create(title = request.POST['title'])
        new_author = Author.objects.create(name = request.POST['author'])
        this_book = new_book
        this_author = new_author
        this_author.books.add(this_book)

        # if (request.POST['add_author'] != 0):
        #     new_author = Author.objects.get(id  = request.POST['add_author'])
        #     new_book.author.add(new_author)
        # else:
        #     new_author = Author.objects.create(name = request.POST['author'], book = new_book)

        Review.objects.create(
            desc = request.POST['desc'], 
            rating = request.POST['rate'], 
            created_by = User.objects.get(id = request.session['u_id']),
            reviewed_book = new_book)
    return redirect(f'/book/{new_book.id}')

def addReview(request, val):
    if request.method == 'POST':
        Review.objects.create(
            desc = request.POST['desc'], 
            rating = request.POST['rate'], 
            created_by = User.objects.get(id = request.session['u_id']),
            reviewed_book = Book.objects.get(id = val))
    return redirect(f'/book/{val}')

def showBook(request, val):
    context = {
        "book": Book.objects.get(id = val),
        "user": User.objects.get(id = request.session['u_id']),
        "reviews": Review.objects.all(),
        "authors": Author.objects.filter(books = Book.objects.get(id = val)),
    }
    return render(request,"book.html", context)

def showUser(request, val):
    length = len(Review.objects.filter(created_by = User.objects.get(id = val)))
    context = {
        "books": Book.objects.all(),
        "reviews": Review.objects.filter(created_by = User.objects.get(id = val)),
        "user": User.objects.get(id = val),
        "length": length,
    }
    return render(request,"user.html", context)

def deleteReview(request, val):
    user = User.objects.get(id = request.session['u_id'])
    book = Review.objects.get(id = val).reviewed_book.id
    review = Review.objects.get(id = val)
    review.delete()
    return redirect(f'/book/{book}')
