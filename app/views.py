from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import *

from sqlite3 import *
error_field = ''

def index(request):
    data = {}

    conn = connect('main.sql')
    c = Cursor(conn)

    c.execute('SELECT * FROM sqlite_master where type="table";')
    tables = c.fetchall()
    
    user_tables = []
    for table in tables:
        if table[1].split('_')[0] == request.user.username:
                        
            fields = []
            c.execute(f'PRAGMA table_info({table[1]})')
            dt=c.fetchall()
            for i in dt:
                fields.append(i[1])

            values = []
            c.execute(f'SELECT * FROM {table[1]}')
            values = c.fetchall()

            data[table[1]] = {'fields':fields, 'values':values}

    conn.commit()
    conn.close()
    
    if request.method == 'POST':
        query = request.POST.get('query', '')

        conn = connect('main.sql')
        c = Cursor(conn)

        try:
            c.execute(query)

            conn.commit()
            conn.close()

            return redirect('error')
        except Exception as e:
            error_field = e
            return redirect('error')

    return render(request, 'index.html', context={'data':data})

def error(request):
    global error_field

    return render(request, 'error.html', {'error': error_field})

def create(request):   
    global error_field 
    if request.method == 'POST':
        table_name = request.POST.get('table_name', '')
        fields = request.POST.get('fields', '')

        conn = connect('main.sql')
        c = Cursor(conn)

        try:
            c.execute(f"CREATE TABLE {request.user.username}_{table_name} ({fields})")

            conn.commit()
            conn.close()

            return redirect('error')
        except Exception as e:
            error_field = e
            return redirect('error')

        

    return render(request, 'create.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('home')

