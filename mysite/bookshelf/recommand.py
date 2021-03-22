from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.db import connection
from bookshelf import recAlg as ra

def recomBook(request):
    try:
        uid = request.session["uinfo"]
    except Exception as e:
        print("Not login")
        return render(request,'index.html')

    req_type = request.GET.get('type')
    uid = request.session['uinfo']
    
    print(req_type)
    print("===== Rocommendation Algorithm =====")
    if req_type == '0':
        # Coming from the previous page, the recommendation algorithm needs to be called
        uid = request.session['uinfo']
        print('='*30)
        print(uid)
        reco = ra.recommender()
        books = reco.recommend(user_Id=int(uid))
        # print("===== recommend =====")
        # print(books)
        request.session['books'] = books
        context={
            "book":books[0],
        }
        print(books[0])
        return render(request,"recom-1.html",context=context)
    elif req_type == '2':
        # Click seeAlso to trigger, need to query session to get recommended information
        books = request.session['books']
        context={
            "book1":books[1],
            "book2":books[2],
            "book3":books[3],
        }
        return render(request,"recom-2.html",context=context)
    elif req_type == '1':
        # Click Introduction to trigger, you need to query session to get recommended information
        books = request.session['books']
        print(books[0])
        context={
            "book":books[0],
        }
        # print(books[0])
        return render(request,"recom-1.html",context=context)
    return HttpResponse("error")
    



