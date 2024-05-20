from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import CommunityForm, TemplateFieldForm
from .models import Community
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def homepage(request):
    return render(request, "homepage.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Registration successful. You can now login.")
        return redirect("user_login")
    else:
        return render(request, "register.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            request.session["username"] = username
            return redirect("homepage")
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html")
    else:
        return render(request, "login.html")


def user_logout(request):
    logout(request)
    return render(request, "logout.html")


def communities(request):
    if "username" in request.session:
        communities = Community.objects.all()
        return render(request, "communities.html", {"communities": communities})
    else:
        return redirect("user_login")


def create_community(request):
    if "username" not in request.session:
        return redirect("user_login")

    if request.method == "POST":
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            try:
                community.created_by = User.objects.get(
                    username=request.session["username"]
                )
            except ObjectDoesNotExist:
                messages.error(request, "User does not exist.")
                return redirect("user_login")
            community.save()
            return redirect("communities")
    else:
        form = CommunityForm()

    return render(request, "create_community.html", {"form": form})


def community_detail(request, community_id):
    community = get_object_or_404(Community, id=community_id)

    if request.method == "POST":
        form = TemplateFieldForm(request.POST)
        if form.is_valid():
            field = form.cleaned_data
            community.template.fields.append(field)
            community.template.save()
    else:
        form = TemplateFieldForm()
    return render(
        request, "community_detail.html", {"community": community, "form": form}
    )


def follow_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if request.user not in community.followers.all():
        community.followers.add(request.user)
    else:
        community.followers.remove(request.user)
    return redirect("community_detail", community_id=community_id)
