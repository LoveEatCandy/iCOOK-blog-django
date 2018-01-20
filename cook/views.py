from django.shortcuts import render,get_object_or_404,render_to_response
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic.base import View
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from .models import Articles,UserFavorate,Comment,UserReply


def index(request):
    last_articles_list=Articles.objects.order_by('-a_time')[:3]
    hot_articles_list=Articles.objects.order_by('-a_shouchang')[:5]
    if request.user.is_authenticated:
        count = request.user.to_who.filter(readed=False).count()
    else:
        count = None
    return render(request,'cook/index.html',{'last_articles_list':last_articles_list,
                                            'count':count,
                                            'hot_articles_list':hot_articles_list})

def recipes(request,foodstyle):
    if foodstyle == 'all':
        all_articles=Articles.objects.all()
    else:
        all_articles = Articles.objects.filter(a_type=foodstyle)
    pr_ordering = request.GET.get('order_by','')
    if pr_ordering == '-a_shouchang':
        ordering = pr_ordering
    else:
        ordering = ''
    if ordering:
        all_articles=all_articles.order_by(ordering)
    pages = Paginator(all_articles,8)
    page = request.GET.get('page','1')
    page1,page2,i=0,0,0
    pagex = int(page)
    if pages.num_pages <= 5:
        page1 = 1
    else:
        maxp = pages.num_pages
        if pagex <= 3:
            page2 = 3
            i=range(1,6)
        elif pagex >3 and pagex+2>=maxp:
            page2 = 1
            i=range(maxp-4,maxp+1)
        else:
            page2 = 2
            i=range(pagex-2,pagex+3)
    if pages.num_pages > 5:
        t = 1
    else:
        t = 2
    try:
        contacts = pages.get_page(page)
    except PageNotAnInteger:
        contacts = pages.get_page(1)
    except EmptyPage:
        contacts = pages.get_page(pages.num_pages)
    if request.user.is_authenticated:
        count = request.user.to_who.filter(readed=False).count()
    else:
        count = None
    return render(request,'cook/recipes.html',{'all_articles':contacts,'page1':page1,'page2':page2,'i':i,'foodstyle':foodstyle,'t':t,'ordering':ordering,'count':count})

def search(request):
    if 'search' in request.POST:
        ths=request.POST['search']
        if request.user.is_authenticated:
            count = request.user.to_who.filter(readed=False).count()
        else:
            count = None
        if not ths:
            search_error='请输入您想搜索的内容。'
        else:
            searchings=Articles.objects.filter(Q(a_name__icontains=ths)|Q(a_type__icontains=ths)|Q(a_words__icontains=ths))
            if not searchings:
                search_error='对不起，没有找到您要搜索的内容。'
            else:
                return render(request,'cook/search.html',{'searchings':searchings,'count':count})
        return render(request,'cook/search.html',{'search_error':search_error,'count':count})


def single(request,article_id):
    ar=get_object_or_404(Articles,pk=article_id)
    has_fav = False
    count = None
    if request.user.is_authenticated:
        count = request.user.to_who.filter(readed=False).count()
        if UserFavorate.objects.filter(user=request.user,fav_id= ar.id):
            has_fav = True
    comments = ar.comment_set.all().order_by('-time')
    return render(request,'cook/single.html',{'ar':ar,'has_fav':has_fav,'comments':comments,'count':count})


def about(request):
    if request.user.is_authenticated:
        count = request.user.to_who.filter(readed=False).count()
    else:
        count = None
    return render(request,'cook/about.html',{'count':count})


class FavorateView(View):
    #收藏
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)

        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type='application/json')
        exist_records = UserFavorate.objects.filter(user=request.user,fav_id= int(fav_id))
        ar = get_object_or_404(Articles, pk=fav_id)
        if exist_records:
            ar.a_shouchang -= 1
            ar.save()
            exist_records.delete()
            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorate()
            if int(fav_id) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.save()
                ar.a_shouchang += 1
                ar.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')


class AddCommentView(View):
    def post(self,request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        article_id = request.POST.get('ar_id',0)
        comments = request.POST.get('comments','')
        user = request.user
        if int(article_id)>0 and comments:
            article = Articles.objects.get(id=article_id)
            comment = Comment()
            comment.article = article
            comment.comment_text = comments
            comment.user = user
            comment.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"评论失败"}', content_type='application/json')


class AddReply1View(View):
    def post(self,request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        c_id = request.POST.get('c_id',0)
        comments = request.POST.get('comments','')
        user = request.user
        if int(c_id)>0 and comments:
            comment = Comment.objects.get(id=c_id)
            to_who = comment.user
            reply1 = UserReply()
            reply1.comment = comment
            reply1.reply_text = comments
            reply1.from_who = user
            reply1.to_who = to_who
            reply1.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"评论失败"}', content_type='application/json')


class AddReply2View(View):
    def post(self,request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        c_id = request.POST.get('c_id',0)
        comments = request.POST.get('comments','')
        user = request.user
        if int(c_id)>0 and comments:
            reply = UserReply.objects.get(id=c_id)
            to_who = reply.from_who
            comment = reply.comment
            reply1 = UserReply()
            reply1.comment = comment
            reply1.reply_text = comments
            reply1.from_who = user
            reply1.to_who = to_who
            reply1.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"评论失败"}', content_type='application/json')


class DeleteCommentView(View):
    def post(self,request):
        comment_id = request.POST.get('comment_id','')
        if comment_id:
            comment = Comment.objects.filter(id=comment_id)
            if comment:
                for a in comment:
                    a.delete()
                    return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class DeleteReplyView(View):
    def post(self,request):
        reply_id = request.POST.get('reply_id','')
        if reply_id:
            reply = UserReply.objects.filter(id=reply_id)
            if reply:
                for a in reply:
                    a.delete()
                    return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


@login_required(login_url='login/')
def person(request):
    user = request.user
    favs = UserFavorate.objects.filter(user=user)
    all_fav_id = (x.fav_id for x in favs)
    all_reply = user.to_who.all().order_by('-time')
    all_fav = Articles.objects.filter(id__in=all_fav_id)
    for reply in all_reply:
        reply.readed = True
        reply.save()

    pages = Paginator(all_fav,6)
    page = request.GET.get('page','1')
    page1,page2,i=0,0,0
    pagex = int(page)
    if pages.num_pages <= 5:
        page1 = 1
    else:
        maxp = pages.num_pages
        if pagex <= 3:
            page2 = 3
            i=range(1,6)
        elif pagex >3 and pagex+2>=maxp:
            page2 = 1
            i=range(maxp-4,maxp+1)
        else:
            page2 = 2
            i=range(pagex-2,pagex+3)
    if pages.num_pages > 5:
        t = 1
    else:
        t = 2
    try:
        contacts = pages.get_page(page)
    except PageNotAnInteger:
        contacts = pages.get_page(1)
    except EmptyPage:
        contacts = pages.get_page(pages.num_pages)
    return render(request,'cook/person.html',{'all_fav':contacts,'page1':page1,'page2':page2,'i':i,'t':t,'all_reply':all_reply})


def page_not_found(request,exception):
    #404
    response = render_to_response('cook/404.html', {})
    response.status_code = 404
    return response


def page_error(request,exception):
    #500
    response = render_to_response('cook/500.html', {})
    response.status_code = 500
    return response
