from django.shortcuts import render, redirect
from django.contrib import messages
import psycopg2

# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # email = request.POST.get('email')
        
        try:
            conn = psycopg2.connect(
                dbname="swe573db",
                user="swe573user",
                password="swe573password",
                host="swe573-postgres",
                port="5432"
            )
            cursor = conn.cursor()
            
            # Check if username already exists
            cursor.execute("SELECT * FROM swe573app_user WHERE username = %s", (username,))
            if cursor.fetchone() is not None:
                messages.error(request, 'Username already exists.')
                return redirect('register')
            
            # Insert new user into the database
            cursor.execute("INSERT INTO swe573app_user (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            
            # Optionally, you can log the user in automatically after registration
            messages.success(request, 'Registration successful. You can now login.')
            return redirect('user_login')
        except psycopg2.Error as e:
            print("Error connecting to PostgreSQL database:", e)
            messages.error(request, 'Error registering user.')
            return redirect('register')
        finally:
            if conn is not None:
                conn.close()
    else:
        return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            conn = psycopg2.connect(
                dbname="swe573db",
                user="swe573user",
                password="swe573password",
                host="swe573-postgres",
                port="5432"
            )
            cursor = conn.cursor()
            
            # Check if username and password match
            cursor.execute("SELECT * FROM swe573app_user WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            if user is not None:
                messages.success(request, 'Login successful.')
                request.session['username'] = username
                # Optionally, you can set session variables to maintain user authentication
                return redirect('homepage')
            else:
                messages.error(request, 'Invalid username or password.')
                return render(request, 'login.html')
        except psycopg2.Error as e:
            print("Error connecting to PostgreSQL database:", e)
            messages.error(request, 'Error logging in.')
            return redirect('login')
        finally:
            if conn is not None:
                conn.close()
    else:
        return render(request, 'login.html')
    
def user_logout(request):
    if 'username' in request.session:
        del request.session['username']
    return render(request, 'logout.html')