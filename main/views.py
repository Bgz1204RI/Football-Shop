from django.shortcuts import render

def about(request):
    context = {
        "app_name": "Football Shop",     # your app’s name
        "student_name": "Bagas Zharif",  # replace with your real name
        "student_class": "CS 2024"       # replace with your class
    }
    return render(request, "about.html", context)
