from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CommunityForm, TemplateFieldForm
from .models import Community
from django.core.exceptions import ObjectDoesNotExist


def homepage(request):
    if "username" in request.session:
        user = User.objects.get(username=request.session["username"])
        followed_communities = user.following.all()
    else:
        followed_communities = []

    return render(
        request, "homepage.html", {"followed_communities": followed_communities}
    )


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
        communities = Community.objects.filter(is_active=True)
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
                user = User.objects.get(username=request.session["username"])
                community.created_by = user
            except ObjectDoesNotExist:
                messages.error(request, "User does not exist.")
                return redirect("user_login")
            community.save()
            community.followers.add(user)  # Add the creator to the followers list
            return redirect("communities")
    else:
        form = CommunityForm()

    return render(request, "create_community.html", {"form": form})


from .forms import DescriptionForm, TemplateFieldForm


def community_detail(request, community_id):
    community = get_object_or_404(Community, id=community_id)

    if request.method == "POST":
        form = TemplateFieldForm(request.POST)
        description_form = DescriptionForm(request.POST)

        if form.is_valid():
            field = form.cleaned_data
            community.template.fields.append(field)
            community.template.save()

        if description_form.is_valid() and request.user in community.moderators.all():
            new_description = description_form.cleaned_data.get("description")
            if new_description is not None:
                community.description = new_description
                community.save()

    else:
        form = TemplateFieldForm()
        description_form = DescriptionForm(
            initial={"description": community.description}
        )

    return render(
        request,
        "community_detail.html",
        {"community": community, "form": form, "description_form": description_form},
    )


def follow_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if request.user not in community.followers.all():
        community.followers.add(request.user)
    else:
        community.followers.remove(request.user)
    return redirect("community_detail", community_id=community_id)


@login_required
def edit_description(request, community_id):
    community = Community.objects.get(id=community_id)

    if request.method == "POST":
        if request.user in community.moderators.all():
            new_description = request.POST.get("description")
            if new_description is not None:
                community.description = new_description
                community.save()
            return redirect("community_detail", community_id=community.id)

    return render(request, "edit_description.html", {"community": community})


@login_required
def make_moderator(request, community_id, user_id):
    community = get_object_or_404(Community, id=community_id)
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST" and request.user in community.moderators.all():
        community.moderators.add(user)
        community.save()

    return redirect("community_detail", community_id=community.id)


@login_required
def remove_moderator(request, community_id, user_id):
    community = get_object_or_404(Community, id=community_id)
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST" and request.user == community.created_by:
        community.moderators.remove(user)
        community.save()

    return redirect("community_detail", community_id=community.id)


@login_required
def delete_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)

    if request.method == "POST" and request.user == community.created_by:
        community.is_active = (
            False  # Set is_active to False instead of deleting the community
        )
        community.save()

    return redirect("community_detail", community_id=community.id)


@login_required
def activate_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)

    if request.method == "POST" and request.user == community.created_by:
        community.is_active = True
        community.save()

    return redirect("community_detail", community_id=community.id)
