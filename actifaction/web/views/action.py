# -*- coding: utf8 -*-
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from api.models import Action, UserProfile
from web.forms.action_forms import ActionForm
from web.processors.action import create_or_update_action
from django.http import HttpResponseRedirect


def main_page(request):
	return render_to_response('pages/index.html')


def index(request):
	all_actions = Action.objects.all()
	context = {
		'actions': all_actions
	}
	return render_to_response(
		'pages/index.html',
		context,
        context_instance=RequestContext(request))


@login_required
def view_all_actions(request):
	all_actions = Action.objects.all()
	context = {'actions': all_actions}
	return render_to_response("pages/action_index.html", context, context_instance=RequestContext(request))


@login_required
def add_action(request):
    action_form = ActionForm()

    if request.method =="POST":
        action_form = ActionForm(data=request.POST)
    if action_form.is_valid():
        action_data = {"organizer_id" : request.user.id}
        action_data.update(action_form.cleaned_data)
        action = create_or_update_action(**action_data)
        action_id = action.id
        return HttpResponseRedirect(reverse('web.view_action', args=[action_id]))
    context = {"form": action_form}
    return render_to_response("pages/create_action.html", context, context_instance=RequestContext(request))

@login_required
def view_action(request, action_id):
	action = get_object_or_404(Action, pk=action_id)
	organizer = UserProfile.objects.get(user__pk=action.organizer.id)
	context = {'action': action, 'organizer': organizer}
	return render_to_response("pages/view_action.html", context, context_instance=RequestContext(request))

@login_required
def edit_action(request):
     #action = get_object_or_404(Action,pk=action_id)
    #context = {'action' : action}
    #return render_to_response("pages/view_action.html", context, context_instance=RequestContext(request))
    pass

@login_required
def submit_action(request):
	pass

@login_required
def join_action(request):
	pass


