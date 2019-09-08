from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from .models import Song,UserInterest,Review
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.core.paginator import Paginator,EmptyPage,InvalidPage,PageNotAnInteger

from django.db.models import Q
from django.db.models import Avg

# Create your views here.

import re, math
from random import sample
import numpy as np
import pandas as pd

from collections import Counter
WORD = re.compile(r'\w+')

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            '''current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('song/acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()'''
            context={
                'msg':'You have been registered.Please confirm your account by logging to your email account.',
                'form': SignupForm()
            }
            return render(request,'song/register.html',context)
    else:
        form = SignupForm()
    return render(request, 'song/register.html', {'form': form})

def activate(request, uidb64, token):
    songs= Song.objects.all().order_by('?')
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        context={
            'msg':'Thank you for connecting with us. We are delighted to see you.',
        }
        return render(request,'song/index.html',context)
    else:
        return HttpResponse('Activation link is invalid!')

@login_required
def dashboard(request):    
    searchKey= request.GET.get('search')
    if searchKey is not None:
        list= Song.objects.filter(Q(name__icontains=searchKey)).order_by('?')
    else:
        list= Song.objects.all().order_by('?')
        searchKey=""
    paginator= Paginator(list,15)
    page= request.GET.get('page')
    try:
        songs= paginator.page(page)
    except PageNotAnInteger:
        songs= paginator.page(1)
    except EmptyPage:
        songs= paginator.page(paginator.num_pages)
    context={
        'page': page,
        'searchKey':searchKey,
        'songs': songs,
    }
    return render(request,'song/dashboard.html',context)

def index(request):
    return render(request,'song/index.html')

def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def myfilterid(mytag,mysong):
    song_id = []
    cosine_value = []
    vec1 = text_to_vector(mytag)
    for m in mysong:
        song_id.append(m.id)
        cosine_value.append(get_cosine(vec1,text_to_vector(m.tag)))
    index = list(range(0,len(song_id)))
    df = pd.DataFrame({'id':song_id,'cosine_value':cosine_value},index=index)
    df = df[(df['cosine_value']>0.4)]
    mysongid = df['id'].values
    mysongid = mysongid.tolist()
    return mysongid

@login_required
def recommend(request,id):
    songs= Song.objects.all()
    song = songs.get(id=id)
    current_song_tag = song.tag
    similar_song = Song.objects.filter(tag__contains=current_song_tag).exclude(name=song)
    u = User.objects.get(id=request.user.id)
    reviews = Review.objects.filter(song=song)
    averageRating = reviews.aggregate(Avg('rating'))
    if averageRating['rating__avg'] is None:
        averageRating['rating__avg']=0
    hasUserRated = Review.objects.filter(user=u,song=song).count()
    for x in current_song_tag.split(','):
        user = UserInterest(user=u,tag=x,song=song)
        user.save()
    try:
        user_tag  = UserInterest.objects.filter(user_id=request.user.id)
        user_tags = ""
        for t in user_tag:
            user_tags  = user_tags+" "+t.tag
        recommended_song_id = myfilterid(user_tags,songs)
        resongs = Song.objects.filter(id__in=recommended_song_id).order_by('?').exclude(name=song)[:8]
    except:
        pass
    context={
            'song':song,
            'resongs':resongs,
            'similar_song':similar_song,
            'reviews':reviews,
            'averageRating':averageRating['rating__avg'],
            'hasUserRated':hasUserRated
        }
    return render(request,'song/recommend.html',context)

@login_required
def rate(request,id):    
    if request.method == 'POST':
        obj = Review()
        obj.user = User.objects.get(id=request.user.id)
        
        songs= Song.objects.all()
        obj.song = songs.get(id=id)
        obj.rating = request.POST.get("rating")
        obj.review = request.POST.get("review")
        obj.save()
    return HttpResponseRedirect('/recommend/'+id+'/play')

