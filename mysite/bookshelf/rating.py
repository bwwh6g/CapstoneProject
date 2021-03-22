from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.db import connection
import csv
import os

def getRatingPage(request):
    if request.method == 'GET':
        try:
            uid = request.session["uinfo"]
        except Exception as e:
            print("Not login yet")
            return render(request,'index.html')
        # if uid == "":
        #     return render(request,'index.html')
        # else:
        #     print("session UId=",uid)
        
        return render(request,"rating.html")
    else:
        print("===== getRatingPage:The current request is not a get method!=====")
        return render(request,"error.html")

def getRatingBooks(request):
    if request.method == 'POST':
        isbn = request.POST.get('isbn')
        print("==== getRatingBooks: ====")
        print("isbn:",isbn)
        rs = getBookInfo(isbn)
        if len(rs) == 0:  # Invalid isbn
            return JsonResponse("",safe=False)
        else:      
            book = {
                'isbn':rs[0][0],
                'title':rs[0][1],
                'author':rs[0][2],
                'y-o-p':rs[0][3],
                'publisher':rs[0][4],
                'cover_url':rs[0][5],
                
            }
            return JsonResponse(book)
    else:
        print("===== getRatingBooks:The current request is not a post method!=====")
        return JsonResponse('error')

def getBookInfo(isbn):
    print(type(isbn))
    cursor = connection.cursor()
    get_book_sql = "select * from bookinfo where isbn = %s"
    
    cursor.execute(get_book_sql,isbn)
    rs = cursor.fetchall()
    print(len(rs))
    if len(rs)==0:
        print('Wrong isbn\n')
        return ""
    else:
        print("title:",rs[0])  # 600551
    return rs



def saveRating(request):
    isbn = request.POST.get('isbn')
    rating = request.POST.get('rating')
    uid = request.session['uinfo']
    path =  os.path.join(os.path.dirname(__file__),'Data/datasets/ratings3.csv')
    # Append mode, data is written into the csv file
    try:
        with open(path,"a+",newline='\n') as file:
            csv_file = csv.writer(file,delimiter=';')
            data = [uid,isbn,rating]
            # data = ['12345','gafouwsgfoa','10']
            csv_file.writerow(data)

        file.close()
        print("===== Write rating successfully =====")
        print(uid,isbn,rating)
        return JsonResponse("")
    except Exception as e:
        print(e)
        return HttpResponse("error")

def logout(request):
    # return render "index.html"
    request.session.clear()
    #print(request.session['uinfo'])
    '''
    If you add the output, it will report an error
    KeyError at /logout
    'uinfo'
    '''
    return render(request,'index.html')