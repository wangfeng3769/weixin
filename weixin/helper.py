#coding=utf8
import datetime
from django.db.models import Count
from weixin.models import Weixin_Userinfo, Weixin_Message, Filmsession_hall, Movie_Bar_Posters, Activity, Movie
import time

def __imageUrl2SizeByLYK(movie_id, type, url, size):
    if 'gewara.cn' in url or 'mtime.cn' in url or 'mtime.com' in url:
        url_pref = '%s%s' % ('', movie_id)
        if 's' == size:
            if 'gewara.cn' in url:
                filename = ''.join(['s_', __getFileName(url)])
            else:
                filename = __getFileName(__imageUrl2SmallByMtime(url))
        elif 'l' == size:
            if 'gewara.cn' in url:
                filename = __getFileName(url)
            else:
                filename = __getFileName(__imageUrl2LargeByMtime(url))
        else:
            filename = __getFileName(url)

        if 'poster' == type:
            filename = '%scompress_%s' % ('/', filename)
        if 'posters' == type:
            filename = '%scompress_%s' % ('/posters/', filename)
        if 'stills' == type:
            filename = '%scompress_%s' % ('/stills/', filename)
        if 'trailers' == type:
            filename = '%scompress_%s' % ('/trailers/', filename)

        return ''.join([url_pref, filename])
    elif '' in url:
        if 's' == size:
            url = url.replace('', 'www.leyingke.com/media')
            return '%s?width=220' % url
    return url

def __getFileName(url):
    suff = url.split('.')[-1]
    filename = url.split('/')[-1].replace(''.join(['.', suff]), '')
    return ''.join([filename, '.', suff])

def __imageUrl2SmallByMtime(url):
    return __imageUrl2SizeByMtime(url, '220X350')

def __imageUrl2SizeByMtime(url, size):
    if url.find('_') > -1:
        prefix = url[0: url.rfind('_')]
    else:
        prefix = url[0: url.rfind('.')]
    suffix = url.split('.')[-1]
    return ''.join([prefix, '_', size, '.', suffix])
def __imageUrl2LargeByMtime(url):
    return __imageUrl2SizeByMtime(url, '640X960')
def __imageUrl2SizeByMtime(url, size):
    if url.find('_') > -1:
        prefix = url[0: url.rfind('_')]
    else:
        prefix = url[0: url.rfind('.')]
    suffix = url.split('.')[-1]
    return ''.join([prefix, '_', size, '.', suffix])
def __activity_imageurl(activity):
    if activity.image_url.startswith('http://') or activity.image_url.startswith('/'):
        return activity.image_url
    elif activity.img_url:
        return '%s' % activity.img_url
    return ''

def __activity_image_compress_url(activity):
    if activity.image_url.startswith('http://') or activity.image_url.startswith('/'):
        return activity.image_url
    elif activity.img_compress_url:
        return '%s' % activity.img_compress_url
    elif activity.img_url:
        return '%s' % activity.img_url
    else:
        return ''

text_reply ="""
<xml>
<ToUserName><![CDATA[{touser}]]></ToUserName>
<FromUserName><![CDATA[{fromuser}]]></FromUserName>
<CreateTime>{createtime}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{content}]]></Content>
<FuncFlag>0</FuncFlag>
</xml>
"""

music_reply = """
<xml>
<ToUserName><![CDATA[{touser}]]></ToUserName>
<FromUserName><![CDATA[{fromuser}]]></FromUserName>
<CreateTime>{createTime}</CreateTime>
<MsgType><![CDATA[music]]></MsgType>
<Music>
<Title><![CDATA[{title}]]></Title>
<Description><![CDATA[DESCRIPTION]]></Description>
<MusicUrl><![CDATA[MUSIC_Url]]></MusicUrl>
<HQMusicUrl><![CDATA[HQ_MUSIC_Url]]></HQMusicUrl>
</Music>
<FuncFlag>0</FuncFlag>
</xml>
"""
pic_text="""
<xml>
    <ToUserName><![CDATA[{to}]]></ToUserName>
    <FromUserName><![CDATA[{fromuser}]]></FromUserName>
    <CreateTime>{createtime}</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    {article}
    <FuncFlag>1</FuncFlag>
</xml>
"""
def userinfo_add(msg):
    try:
        Weixin_Userinfo.objects.filter(uid=msg['FromUserName'])
    except Exception:
        Weixin_Userinfo.objects.create(username=msg['FromUserName'])

def to_unicode(value):
    if isinstance(value, unicode):
        return value
    if isinstance(value, basestring):
        return value.decode('utf-8')
    if isinstance(value, int):
        return str(value)
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return value
def __movie_Horizon_Poster(movie):
    horizon_poster_list = movie.movie_bar_posters_set.filter(type=1).all()
    if horizon_poster_list:
        return __imageUrl2SizeByLYK(movie.id, 'posters', horizon_poster_list[0].image_url_spider or 'http:%s' % horizon_poster_list[0].img, 'l')
    return __imageUrl2SizeByLYK(movie.id, 'poster', movie.poster_image_url, 'l')


def judge_text(msg):
    if msg['Content'] == 'Hello2BizUser'or msg['Content'] == '0':
        content = u'欢迎关注，我们将为你提供最新而且实用的观影信息!\n1.先看看最火的影片。\n2.找个影院去看电影。\n3.有优惠吗？\n4.很无聊不知道干什么。\n0.任何时候回复0，都将回到这里。'
        response_content = dict(content = content,touser = msg['FromUserName'],fromuser = msg['ToUserName'],createtime = str(int(time.time())))
        userinfo_add(msg)
        # print to_unicode(text_reply).format(**response_content)
        return to_unicode(text_reply).format(**response_content)
    elif msg['Content'] == '1':
        # print 1
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        tomorrow = datetime.date.today() + oneday
        movies = Movie.objects.filter(filmsession__date__in=[today, tomorrow]).annotate(num_filmsessions=Count('filmsession'), ).order_by('-num_filmsessions')[0:5]
        items=''
        i=1
        for movie in movies:
            title = movie.title
            plot = to_unicode(movie.plots)[0:20]
            if i==1:
                img = __movie_Horizon_Poster(movie)
            else:
                img = __imageUrl2SizeByLYK(movie.id, 'poster', movie.poster_image_url, 's')
            items += """<item>
                    <Title><![CDATA[%s]]></Title>
                    <Description><![CDATA[%s]]></Description>
                    <PicUrl><![CDATA[%s]]></PicUrl>
                    <Url><![CDATA[%s]]></Url>
                </item>""" %(title,to_unicode(plot),img,'http://weixin.leyingke.com/')
            i+=1
        article = """<ArticleCount>%s</ArticleCount>
                    <Articles>
                     %s
                    </Articles> """%(len(movies),items)
        send_info = dict(article = to_unicode(article),to = msg['FromUserName'],fromuser = msg['ToUserName'],createtime = str(int(time.time())))
        # print to_unicode(pic_text).format(**send_info)
        return to_unicode(pic_text).format(**send_info)
    elif msg['Content'] == '3':
        now = datetime.datetime.now()
        activitys=Activity.objects.filter(starttime__lte=now, endtime__gte=now, status=2).order_by('-updatetime')[0:5]
        items = ''
        for ac in activitys:
            ac_title = ac.title
            des = ac.description[:20]
            img = __activity_image_compress_url(ac)
            items += """
                <item>
                    <Title><![CDATA[%s]]></Title>
                    <Description><![CDATA[%s]]></Description>
                    <PicUrl><![CDATA[%s]]></PicUrl>
                    <Url><![CDATA[%s]]></Url>
                </item>""" %(ac_title,to_unicode(des),img,'http://weixin.leyingke.com/')
        article = """
                    <ArticleCount>%s</ArticleCount>
                    <Articles>
                     %s
                    </Articles> """%(len(activitys),items)
        send_info = dict(article = to_unicode(article),to = msg['FromUserName'],fromuser = msg['ToUserName'],createtime = str(int(time.time())))
        return to_unicode(pic_text).format(**send_info)

    elif msg['Content'] == '4':
        content = u'陪唱，你敢唱我就敢接……！'
        reply_info = dict(touser=msg['FromUserName'],fromuser=msg['ToUserName'],createtime=str(int(time.time())),content=content)
        return to_unicode(text_reply).format(**reply_info)
    elif msg['Content'] == '2':
        content = u'此服务在开发之中，暂时不能使用。'
        reply_info = dict(touser=msg['FromUserName'],fromuser=msg['ToUserName'],createtime=str(int(time.time())),content=content)
        return to_unicode(text_reply).format(**reply_info)
    else:
        content = u'欢迎关注，我们将为你提供最新而且实用的观影信息!\n1.先看看最火的影片。\n2.找个影院去看电影。\n3.有优惠吗？\n4.很无聊不知道干什么。\n0.任何时候回复0，都将回到这里。'
        reply_info = dict(touser=msg['FromUserName'],fromuser=msg['ToUserName'],createtime=str(int(time.time())),content=content)
        # print reply_info
        return to_unicode(text_reply).format(**reply_info)

def judge_event(msg):
    # print 'judge_event'
    if msg['Event'] == 'subscribe':
        content = u'欢迎关注，我们将为你提供最新而且实用的观影信息!\n1.先看看最火的影片。\n2.找个影院去看电影。\n3.有优惠吗？\n4.很无聊不知道干什么。\n0.任何时候回复0，都将回到这里。'
        reply_info = dict(touser=msg['FromUserName'],fromuser=msg['ToUserName'],createtime=str(int(time.time())),content=content)
        # print reply_info
        return to_unicode(text_reply).format(**reply_info)
    elif msg['Event'] == 'unsubscribe':
        pass

def weixiningo_add(msg):
    try:
        Weixin_Message.objects.create(user_id=msg['fFromUserName'],message=msg['Content'])
    except Exception,e:
        print e
