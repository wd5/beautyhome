# -*- coding: utf-8 -*-
import  settings, datetime
from django.db.models.loading import get_model
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, TemplateView, View
from apps.users.forms import ProfileForm, RegistrationForm, AddressForm
from apps.users.models import Profile, ProfileAddress
from apps.siteblocks.models import Settings
from apps.orders.models import Order
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth import  authenticate as auth_check, login as auth_login

def send_email_registration(username, password, to_email):
    from django.core.mail import send_mail

    subject = u'Регистрация на сайте – %s' % settings.SITE_NAME
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())

    message = render_to_string('users/registration_email.txt',
            {
            'username': username,
            'password': password,
            'SITE_NAME': settings.SITE_NAME
        })

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])


class RegistrationFormView(FormView):
    form_class = RegistrationForm
    template_name = 'users/registration.html'

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['username'] = data['email']
        reg_form = RegistrationForm(data)
        if reg_form.is_valid():
            new_user = User.objects.create(username=data['username'], email=data['email'])
            new_user.set_password(data['password1'])
            new_user.save()

            profile = Profile.objects.create(user=new_user, name=u'', last_name=u'', third_name=u'',
                b_day=datetime.date(1991, 1, 1), sex=u'female')

            send_email_registration(username=new_user.username, password=data['password1'], to_email=new_user.email)

            user = auth_check(username=request.POST['email'], password=request.POST['password1'])
            try:
                if data['order_id']:
                    try:
                        order = Order.objects.get(id=int(data['order_id']))
                    except:
                        order = False

                    if order:
                        order.profile = profile
                        profile.name = order.first_name
                        profile.last_name = order.last_name
                        profile.phone = order.phone
                        if order.order_carting == 'country':
                            profile.city = order.city
                            profile.address = order.address
                            profile.index = order.index
                            profile.note = order.note
                        profile.save()
                        order.save()
            except:
                pass

            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect('/cabinet/')
            return HttpResponseRedirect('/catalog/')
        else:
            return render_to_response('users/registration.html',
                    {'reg_form': reg_form, 'request': request, 'user': request.user})

    def get(self, request, **kwargs):
        if self.request.user.is_authenticated and self.request.user.id:
            return HttpResponseRedirect(reverse('index'))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(RegistrationFormView, self).get_context_data()
        context['reg_form'] = self.form_class()
        return context

registration_form = RegistrationFormView.as_view()

class ShowProfileForm(FormView):
    form_class = ProfileForm
    template_name = 'users/profile_form.html'

    def get(self, request, **kwargs):
        if self.request.user.is_authenticated and self.request.user.id:
            pass
        else:
            return HttpResponseRedirect(reverse('index'))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ShowProfileForm, self).get_context_data()
        if self.request.user.is_authenticated and self.request.user.id:
            context['profile_form'] = self.form_class(initial={'id': self.request.user.profile.id,
                                                               'name': self.request.user.profile.name,
                                                               'last_name': self.request.user.profile.last_name,
                                                               'user__email': self.request.user.email,
                                                               'phone': self.request.user.profile.phone})
        return context

show_profile_form = ShowProfileForm.as_view()

def GetLoadIds(queryset, loaded_count, split):
    counter = 0
    next_id_loaded_items = ''
    for item in queryset[loaded_count:]:
        counter = counter + 1
        div = counter % loaded_count
        next_id_loaded_items = u'%s,%s' % (next_id_loaded_items, item.id)
        if split:
            if div == 0:
                next_id_loaded_items = u'%s|' % next_id_loaded_items

    if next_id_loaded_items.startswith(',') or next_id_loaded_items.startswith('|'):
        next_id_loaded_items = next_id_loaded_items[1:]
    if next_id_loaded_items.endswith(',') or next_id_loaded_items.endswith('|'):
        next_id_loaded_items = next_id_loaded_items[:-1]
    next_id_loaded_items = next_id_loaded_items.replace('|,', '|')

    next_block_ids = next_id_loaded_items.split('|')[0]
    if next_block_ids != '':
        next_block_ids = next_block_ids.split(',')
        next_block_ids = len(next_block_ids)
        #if loaded_count > next_block_ids:
        #    loaded_count = next_block_ids
        loaded_count = next_block_ids
    else:
        loaded_count = False

    result = u'%s!%s' % (loaded_count, next_id_loaded_items)
    return result


class ShowCabinetView(TemplateView):
    template_name = 'users/show_cabinet.html'

    def get(self, request, **kwargs):
        if self.request.user.is_authenticated and self.request.user.id:
            pass
        else:
            return HttpResponseRedirect(reverse('index'))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ShowCabinetView, self).get_context_data()
        context['division'] = division = self.kwargs.get('division', None) #раздел

        if self.request.user.is_authenticated and self.request.user.id:
            try:
                profile = Profile.objects.get(id=self.request.user.profile.id)
            except:
                profile = False
            if profile:
                if division == 'history':
                    try:
                        loaded_count = int(Settings.objects.get(name='loaded_count').value)
                    except:
                        loaded_count = 5
                    queryset = profile.get_orders()
                    result = GetLoadIds(queryset, loaded_count, False)
                    splited_result = result.split('!')
                    try:
                        remaining_count = int(splited_result[0])
                    except:
                        remaining_count = False
                    next_id_loaded_items = splited_result[1]
                    context['loaded_count'] = remaining_count
                    context['orders'] = profile.get_orders()[:loaded_count]
                    context['next_id_loaded_items'] = next_id_loaded_items
                if division == 'info':
                    context['year_range'] = range(1950, int(datetime.datetime.now().year) + 1)
                    months_choices = []
                    import locale

                    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
                    for i in range(1, 13):
                        months_choices.append((i, datetime.date(2012, i, 1).strftime('%B')))
                    context['month_range'] = months_choices
                    context['day_range'] = range(1, 32)

                if division == 'addresses':
                    context['addresses'] = profile.get_addresses()
                    user_set = User.objects.filter(id=profile.user_id)
                    profile = Profile.objects.get(id=self.request.user.profile.id)
                    context['addresses_form'] = AddressForm(initial={'user': profile.user})
                    context['addresses_form'].fields['user'].queryset = user_set
                if division == 'bonus':
                    pass
                else:
                    pass

        return context

show_cabinet = ShowCabinetView.as_view()

class ItemsLoaderView(View):
    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseRedirect('/')
        else:
            if 'load_ids' not in request.POST or 'm_name' not in request.POST or 'a_name' not in request.POST or 'template' not in request.POST:
                return HttpResponseBadRequest()

            load_ids = request.POST['load_ids']
            template = request.POST['template']
            app_name = request.POST['a_name']
            model_name = request.POST['m_name']
            model = get_model(app_name, model_name)

            try:
                last_class = request.POST['last_class']
            except:
                last_class = False

            load_ids_list = load_ids.split('|')
            block_id = load_ids_list[0]
            load_ids = load_ids.replace(block_id, '')
            block_id = block_id.split(',')
            if load_ids.startswith(',') or load_ids.startswith('|'):
                load_ids = load_ids[1:]
            if load_ids.endswith(',') or load_ids.endswith('|'):
                load_ids = load_ids[:-1]

            try:
                next_ids = load_ids_list[1].split(',')
            except:
                next_ids = False

            if next_ids:
                remaining_count = len(next_ids)
            else:
                remaining_count = -1

            try:
                queryset = model.objects.filter(id__in=block_id)
            except model.DoesNotExist:
                return HttpResponseBadRequest()

            response = HttpResponse()
            load_template = 'items_loader/%s.html' % template
            items_html = render_to_string(
                'items_loader/base_loader.html',
                    {'items': queryset, 'load_template': load_template, 'remaining_count': remaining_count,
                     'load_ids': load_ids, 'last_class': last_class}
            )
            response.content = items_html
            return response

items_loader = ItemsLoaderView.as_view()

class EditUsrInfoView(View):
    def post(self, request, *args, **kwargs):
        type = request.POST['type']
        value = request.POST['value']
        id = request.POST['id']
        try:
            profile = Profile.objects.get(pk=int(id))
        except:
            profile = False

        if profile:
            if type == "name":
                profile_form = ProfileForm({'name': value}, instance=profile)
                try:
                    return HttpResponseBadRequest(u'Имя - %s' % profile_form.errors['name'][0])
                except:
                    profile.save()
                    return HttpResponse(u'Изменения внесены')
            elif type == "last_name":
                profile_form = ProfileForm({'last_name': value}, instance=profile)
                try:
                    return HttpResponseBadRequest(u'Фамилия - %s' % profile_form.errors['last_name'][0])
                except:
                    profile.save()
                    return HttpResponse(u'Изменения внесены')
            elif type == "third_name":
                profile_form = ProfileForm({'third_name': value}, instance=profile)
                try:
                    return HttpResponseBadRequest(u'Отчество - %s' % profile_form.errors['third_name'][0])
                except:
                    profile.save()
                    return HttpResponse(u'Изменения внесены')
            elif type == "day":
                curr_bdate = profile.b_day
                try:
                    new_date = datetime.datetime(curr_bdate.year, curr_bdate.month, int(value))
                except:
                    return HttpResponseBadRequest(u'Дата рождения - Не верная дата')
                profile_form = ProfileForm({'b_day': new_date}, instance=profile)
                try:
                    return HttpResponseBadRequest(u'Дата рождения - %s' % profile_form.errors['b_day'][0])
                except:
                    profile.save()
                    return HttpResponse(u'Изменения внесены')
            elif type == "month":
                curr_bdate = profile.b_day
                try:
                    new_date = datetime.datetime(curr_bdate.year, int(value), curr_bdate.day)
                except:
                    return HttpResponseBadRequest(u'Дата рождения - Не верная дата')
                profile_form = ProfileForm({'b_day': new_date}, instance=profile)
                try:
                    return HttpResponseBadRequest(u'Дата рождения - %s' % profile_form.errors['b_day'][0])
                except:
                    profile.save()
                    return HttpResponse(u'Изменения внесены')
            elif type == "year":
                curr_bdate = profile.b_day
                try:
                    new_date = datetime.datetime(int(value), curr_bdate.month, curr_bdate.day)
                except:
                    return HttpResponseBadRequest(u'Дата рождения - Не верная дата')
                profile_form = ProfileForm({'b_day': new_date}, instance=profile)
                try:
                    return HttpResponseBadRequest(u'Дата рождения - %s' % profile_form.errors['b_day'][0])
                except:
                    profile.save()
                    return HttpResponse(u'Изменения внесены')
            elif type == "sex":
                profile.sex = value
                profile.save()
                return HttpResponse(u'Изменения внесены')
            elif type == "email":
                profile_form = ProfileForm({'user__email': value}, instance=profile)
                try:
                    return HttpResponseBadRequest(u'Email - %s' % profile_form.errors['user__email'][0])
                except:
                    user = profile.user
                    if user.id != 1: # не для админа
                        user.email = value
                        user.username = value
                    else:
                        user.email = value
                    user.save()
                    return HttpResponse(u'Изменения внесены')
            elif type == "phone":
                profile_form = ProfileForm({'phone': value}, instance=profile)
                try:
                    return HttpResponseBadRequest(u'Номер телефона - %s' % profile_form.errors['phone'][0])
                except:
                    profile.save()
                    return HttpResponse(u'Изменения внесены')
            elif type == "is_in_subscribe":
                if value == 'checked':
                    profile.is_in_subscribe = True
                else:
                    profile.is_in_subscribe = False
                profile.save()
                return HttpResponse(u'Изменения внесены')
            else:
                return HttpResponse(u'Не указано поле для изменения')
        else:
            errors = u'Произошла внутренняя ошибка. Не верный идентификатор пользователя.'
            return HttpResponse(errors)

edt_profile_info = csrf_exempt(EditUsrInfoView.as_view())

class CheckAddrForm(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.POST.copy()
            addr_form = AddressForm(data)
            if addr_form.is_valid():
                addr_form.save()
                return HttpResponse('success')
            else:
                addr_form_html = render_to_string(
                    'users/add_addr_modal.html',
                        {'addresses_form': addr_form}
                )
                return HttpResponse(addr_form_html)
        else:
            return HttpResponseBadRequest()

check_addr_modal = csrf_exempt(CheckAddrForm.as_view())

class DelAddrView(View):
    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseRedirect('/')
        else:
            if 'id' not in request.POST:
                return HttpResponseBadRequest()
            else:
                id = request.POST['id']
                try:
                    id = int(id)
                except ValueError:
                    return HttpResponseBadRequest()

            try:
                arddress = ProfileAddress.objects.get(pk=id)
            except ProfileAddress.DoesNotExist:
                return HttpResponseBadRequest()

            arddress.delete()

            return HttpResponse('success')

del_addr = csrf_exempt(DelAddrView.as_view())

