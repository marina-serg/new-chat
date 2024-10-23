from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect, reverse

from .forms import GroupForm, InviteUserForm
from .models import Group, User, Message


@login_required
def home_view(request):
    groups = Group.objects.all().annotate(last_message=Subquery(
        Message.objects.filter(group=OuterRef('pk')).order_by('-timestamp').values('content')[:1]))
    group_info = []
    for group in groups:
        if group.members.all().contains(request.user):
            unread_count = group.unread_messages_count(request.user)
            group_info.append({
                'group': group,
                'unread_count': unread_count
            })
        elif group.invited_users.all().contains(request.user):
            group_info.append({
                'group': group,
                'unread_count': 0
            })
        elif group.exited_users.all().contains(request.user):
            group_info.append({
                'group': group,
                'unread_count': 0
            })

    user = request.user
    context = {
        "groups": groups,
        "user": user,
        "group_info": group_info

    }
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.save()
            group.add_user_to_group(request.user)
            return redirect(reverse('group', args=[group.uuid]))
    else:
        form = GroupForm()

    context = {
        "groups": groups,
        "user": user,
        "group_info": group_info,
        'form': form
    }

    return render(request, template_name="chat/home.html", context=context)


@login_required
def group_chat_view(request, uuid):
    group = get_object_or_404(Group, uuid=uuid)
    if request.user not in group.members.all():
        return HttpResponseForbidden("You are not a member of this group. Kindly use the join button")

    messages = group.message_set.all()
    events = group.event_set.all()
    message_and_event_list = [*messages, *events]
    sorted_message_event_list = sorted(message_and_event_list, key=lambda x: x.timestamp)
    success_messages = []
    group_members = group.members.all()
    invite_form = InviteUserForm()
    group_form = GroupForm(instance=group)

    if request.method == "POST":
        if 'email' in request.POST:
            invite_form = InviteUserForm(request.POST)
            if invite_form.is_valid():
                email = invite_form.cleaned_data['email']
                try:
                    user_to_invite = User.objects.get(email=email)
                    group.invited_users.add(user_to_invite)
                    group.save()
                    success_messages.append('Пользователь успешно приглашен.')

                except User.DoesNotExist:
                    invite_form.add_error('email', 'Пользователь с таким email не найден.')
        else:
            group_form = GroupForm(request.POST, request.FILES, instance=group)
            if group_form.is_valid():
                group_form.save()

    context = {
        "message_and_event_list": sorted_message_event_list,
        "group_members": group_members,
        "invite_form": invite_form,
        'group_uuid': uuid,
        'group_name': group.name,
        'group_form': group_form,
        'group': group,
        'success_messages': success_messages,
    }

    for message in messages:
        message.users_read.add(request.user)

    return render(request, "chat/groupchat.html", context)


@login_required
def clear_chat(request, group_uuid):
    if request.method == 'POST':
        group = Group.objects.get(uuid=group_uuid)
        if request.user in group.members.all():
            group.message_set.all().delete()
    return redirect(group.get_absolute_url())
