#coding=utf8
from django.db import models

class Weixin_Userinfo(models.Model):
    uid = models.CharField('用户id',max_length=255, unique=True)
    username = models.CharField('用户名',max_length=400,blank=True)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)
    updatetime = models.DateTimeField('更新时间', auto_now=True)
    class Meta:
        db_table = u'weixin_userinfo'

class Weixin_Message(models.Model):
    user=models.ForeignKey(Weixin_Userinfo,to_field='uid')
    message = models.TextField('用户发送的信息')
    createtime = models.DateTimeField('创建时间', auto_now_add=True)
    class Meta:
        db_table = u'weixin_message'

class Company(models.Model):
    name = models.CharField('发行公司名称',max_length=100)
    class Meta:
        db_table = 'company'

MOVIE_STATUS_CHOICE = (
    ('1', '已上线'),
    ('0', '已下线'),
)

class Movie(models.Model):
    title = models.CharField('影片名称', max_length=100)
    nickname = models.CharField('别名', max_length = 100,blank=True)
    directors = models.CharField('导演们', max_length=200,blank=True)
    actors = models.CharField('演员们', max_length=200,blank=True)
    mins = models.CharField('片长', max_length=100,blank=True)
    pubdate = models.DateField('影片发布日期')
    age = models.CharField('影片年代',max_length=100,blank=True)
    score = models.CharField('评分', max_length=20,blank=True)
    plots = models.TextField('剧情',blank=True)
    poster_image_url = models.CharField('海报图片地址', max_length=500,blank =True)
    outid = models.CharField('外链id', max_length=32, unique=True)
    index = models.IntegerField('排序', max_length=5, default=0)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)
    status = models.CharField('状态', max_length=50, choices=MOVIE_STATUS_CHOICE, default='1')
    filmtype = models.CharField('影片类型', max_length=100,blank =True)
    certification = models.CharField('影片分级', max_length=200,blank =True)
    language = models.CharField('影片语言', max_length=100,blank =True)
    area = models.CharField('地区', max_length=50,blank =True)
    companys = models.ManyToManyField(Company,db_table='movies_companys', blank=True)

    def __unicode__(self):
        return self.title
    class Meta:
        db_table = u'movie'
        verbose_name = "影片"
        verbose_name_plural = "影片"

class Movie_Trailers(models.Model):
    image_url = models.CharField('预告片图片地址', max_length=500)
    video_url = models.CharField('预告片视频地址', max_length=500)
    movie = models.ForeignKey(Movie, to_field='outid')
    class Meta:
        db_table = u'movie_trailers'
        verbose_name = '预告片信息'
        verbose_name_plural = '预告片信息'

def get_trailer_path(instance,name):
    return 'm/%d/trailers/%s'% (instance.parent.id,name)

class Movie_Bar_Trailers(models.Model):
    parent = models.ForeignKey(Movie)
    image_url_spider = models.CharField('预告片图片地址', max_length=500,blank=True)
    image_url = models.ImageField('预告片图片',upload_to=get_trailer_path, blank=True, null=True)
    video_url = models.CharField('预告片视频地址',max_length = 500)
    class Meta:
        db_table = 'movie_bar_trailers'
        verbose_name = u"添加预告片相关信息"
        verbose_name_plural = u"添加预告片相关信息"



class Movie_Stills(models.Model):
    image_url = models.CharField('剧照图片地址', max_length=500)
    source = models.CharField('来源', max_length=45, default='mtime')
    movie = models.ForeignKey(Movie, to_field='outid')
    class Meta:
        db_table = u'movie_stills'
        verbose_name = '剧照图片'
        verbose_name_plural = '剧照图片'

def get_still_path(instance,name):
    return 'm/%d/stills/%s'% (instance.parent.id,name)

class Movie_Bar_Stills(models.Model):
    parent = models.ForeignKey(Movie) #todo movie
    image_url_spider = models.CharField('预告片图片地址', max_length=500,blank=True)
    source = models.CharField('来源',max_length=45,default='lyk') # todo rename source
    img = models.ImageField('图片',upload_to=get_still_path, blank=True, null=True)#os.path.abspath(os.path.dirname(__file__)))
    class Meta:
        db_table = 'movie_bar_stills'
        verbose_name = u"添加剧照图片"
        verbose_name_plural = u'添加剧照图片'

LYK_MOVIE_POSTER_TYPE_CHOICES = (
    (0, '竖版'),
    (1, '横版'),
)

class Movie_Posters(models.Model):
    image_url = models.CharField('海报图片地址', max_length=500)
    source = models.CharField('来源', max_length=45, default='mtime')
    type = models.IntegerField('海报图片横竖类型', choices=LYK_MOVIE_POSTER_TYPE_CHOICES, default=0)
    movie = models.ForeignKey(Movie, to_field='outid')

    def __unicode__(self):
        return self.movie.title
    class Meta:
        db_table = u'movie_posters'
        verbose_name = "影片海报"
        verbose_name_plural = "影片海报"

def get_poster_path(instance,name):
    return 'm/%d/posters/%s'% (instance.parent.id,name)

class Movie_Bar_Posters(models.Model):
    parent = models.ForeignKey(Movie)
    source = models.CharField('来源',max_length=45,default='lyk')
    type = models.IntegerField('海报版式',max_length=20,choices=LYK_MOVIE_POSTER_TYPE_CHOICES)
    img = models.ImageField('海报图片',upload_to=get_poster_path, blank=True, null=True)#os.path.abspath(os.path.dirname(__file__)))
    image_url_spider = models.CharField('海报图片', max_length=500,blank=True)
    class Meta:
        db_table = 'movie_bar_posters'
        verbose_name = u"添加海报图片"
        verbose_name_plural = u'添加海报图片'

class Movie_Cinecisms(models.Model):
    username = models.CharField('评论人名称', max_length=500)
    region = models.CharField('评论发布地', max_length=500)
    pubtime = models.DateTimeField('评论发布时间', auto_now_add=True)
    content = models.CharField('评论内容', max_length=500)
    movie = models.ForeignKey(Movie, to_field='outid')
    class Meta:
        db_table = u'movie_cinecisms'

LYK_MEDIA_SCORESOURCE_CHOICES = (
    (0, u'网友'),
    (1, u'专业观影团'),
)

class MediaChannel(models.Model):
    medianame = models.CharField('评分媒体名称', max_length=50)
    scoresource = models.IntegerField('评分来源群体', choices=LYK_MEDIA_SCORESOURCE_CHOICES, default=0)
    mediaicon = models.ImageField('评分媒体iconurl', upload_to='icon/%Y/%m/%d', blank=True, null=True, max_length=500)

    def __unicode__(self):
        return u'%s(%s)' % (self.medianame,getLYK_MEDIA_SCORESOURCE_CHOICES_VAULE(self.scoresource))
    class Meta:
        db_table = u'mediachannel'
        verbose_name = "影片评分媒体"
        verbose_name_plural = "影片评分媒体"

def getLYK_MEDIA_SCORESOURCE_CHOICES_VAULE(key):
    for LYK_MEDIA_SCORESOURCE_CHOICE in LYK_MEDIA_SCORESOURCE_CHOICES:
        if LYK_MEDIA_SCORESOURCE_CHOICE[0] == key:
            return LYK_MEDIA_SCORESOURCE_CHOICE[1]

class Movie_Score(models.Model):
    score = models.CharField('分数', max_length=20)
    mediachannel = models.ForeignKey(MediaChannel)
    movie = models.ForeignKey(Movie)

    def __unicode__(self):
        return self.mediachannel.medianame
    class Meta:
        db_table = u'movie_score'
        verbose_name = "影片评分"
        verbose_name_plural = "影片评分"
        unique_together=("mediachannel", "movie")

class Movie_News_List(models.Model):
    title = models.CharField('题目', max_length=100)
    url = models.CharField('外链接地址', max_length=500)
    source = models.CharField('来源', max_length=100,blank=True)
    pubtime = models.DateTimeField('发布时间', max_length=100,blank=True)
    img_url = models.CharField('图片地址', max_length=100,blank=True)
    content = models.TextField('内容',blank=True)
    index = models.IntegerField('排序', max_length=5, default=0)
    movie = models.ForeignKey(Movie)

    def __unicode__(self):
        return self.title
    class Meta:
        db_table = u'movie_news_list'
        verbose_name = "电影报道"
        verbose_name_plural = "电影报道"

class City(models.Model):
    cityid = models.CharField('城市id', max_length=100, unique=True)
    cityname = models.CharField('城市名称', max_length=100)
    center_longitude = models.DecimalField('中心点经度坐标', max_digits=12, decimal_places=6)
    center_latitude = models.DecimalField('中心点纬度坐标', max_digits=12, decimal_places=6)

    def __unicode__(self):
        return self.cityname
    class Meta:
        db_table = u'city'
        verbose_name = "城市"
        verbose_name_plural = "城市"

LYK_CINEMA_ONSALE_CHOICES = (
    (0, '不可售票'),
    (1, '可售票'),
)

BUSINESS_CHOICES =(
    (0,'非营业'),
    (1,'营业')

)
class Equipment(models.Model):
    """胶片格式"""
    type = models.CharField('胶片格式',max_length=100)
    def __unicode__(self):
        return self.type
    class Meta:
        db_table = 'equipment'
        verbose_name = "设备"
        verbose_name_plural = "设备"

class Circuit(models.Model):
    '院线'
    name = models.CharField('院线名称',max_length=100)
    class Meta:
        db_table = 'circuit'
        verbose_name = '院线'
        verbose_name_plural = '院线'

class Cinema(models.Model):
    name = models.CharField('影院名称', max_length=200)
    score = models.CharField('影院打分', max_length=20,blank=True)
    address = models.CharField('影院地址', max_length=400,blank=True)
    longitude = models.DecimalField('经度坐标', max_digits=12, decimal_places=6)
    latitude = models.DecimalField('纬度坐标', max_digits=12, decimal_places=6)
    telephone = models.CharField('联系电话', max_length=100,blank=True)
    description = models.TextField('影院描述',blank=True)
    roadline = models.CharField('乘车路线', max_length=400,blank=True)
    outid = models.CharField('外链id', max_length=32, unique=True)
    locationstr = models.CharField('省市区拼音', max_length=200)
    onsale = models.IntegerField('是否可以售票', choices=LYK_CINEMA_ONSALE_CHOICES, default=0)
    index = models.IntegerField('排序', max_length=5, default=0,blank=True)
    longitude_baidu = models.DecimalField('百度经度坐标', max_digits=12, decimal_places=6,blank=True)
    latitude_baidu = models.DecimalField('百度纬度坐标', max_digits=12, decimal_places=6,blank=True)
    businesshours = models.CharField('营业时间', max_length=50,blank=True)
    weburl = models.CharField('官网地址', max_length=400,blank=True)
    weibourl = models.CharField('官方微博',max_length=400,blank=True)
    introduction = models.TextField('影院介绍',blank=True)
    city = models.ForeignKey(City, to_field='cityid')
    onbusiness = models.IntegerField('是否营业',choices=BUSINESS_CHOICES,default=1)
    worktelephone = models.CharField('工作电话',max_length=100,blank=True)
    circuit = models.ForeignKey(Circuit,blank=True)

    def __unicode__(self):
        return self.name
    class Meta:
        db_table = u'cinema'
        verbose_name = "影院"
        verbose_name_plural = "影院"



class CinemaFeatureType(models.Model):
    type =  models.CharField('影院特色类型', max_length=100)
    def __unicode__(self):
        return self.type
    class Meta:
        db_table = u'cinemafeaturetype'
        verbose_name = "影院特色类型"
        verbose_name_plural = "影院特色类型"

class Cinema_Features(models.Model):
    cinema = models.ForeignKey(Cinema)
    cinemafeaturetype = models.ForeignKey(CinemaFeatureType)
    content = models.CharField('内容',max_length=600)
    class Meta:
        db_table = u'cinema_features'
        verbose_name = "影院特色"
        verbose_name_plural = "影院特色"

def get_cinema_image_path(instance,name):
    if instance.islogo == 1:
        return 'c/%d/%s'% (instance.cinema.id,name)
    return 'c/%d/images/%s'% (instance.cinema.id,name)

class Cinema_Images(models.Model):
    image_url = models.CharField('影院图片地址', max_length=500)
    img = models.ImageField('影院图片',upload_to=get_cinema_image_path, blank=True, null=True)
    islogo = models.IntegerField('是否为logo', default=0)
    cinema = models.ForeignKey(Cinema, to_field='outid')
    class Meta:
        db_table = u'cinema_images'

class Filmsession(models.Model):
    showtime = models.DateTimeField('放映时间', blank=True)
    price = models.CharField('现价', max_length=10, blank=True)
    price_ori = models.CharField('原价', max_length=10, blank=True)
    language_version = models.CharField('语言版本', max_length=20, blank=True)
    screening_mode = models.CharField('屏幕模式', max_length=20, blank=True)
    date = models.DateField('排场日期-用于抓取排重')
    movie = models.ForeignKey(Movie, to_field='outid')
    cinema = models.ForeignKey(Cinema, to_field='outid')
    hall_num = models.CharField('影厅号', max_length=100, blank=True)
    city = models.ForeignKey(City, to_field='cityid')
    endtime = models.DateTimeField('结束时间',blank=True)
    class Meta:
        db_table = u'filmsession'
        verbose_name = '影片排场'
        verbose_name_plural = '影片排场'

FILMSESSION_HALL_BYCBK_CHOICES =(
    (0,'非影院后台上传'),
    (1,'影院后台上传')
)

class Filmsession_hall(models.Model):
    showtime = models.DateTimeField('放映时间', null=True)
    mins = models.CharField('片长',max_length=50,blank=True)
    price = models.CharField('现价', max_length=10, null=True, default='')
    price_ori = models.CharField('原价', max_length=10, null=True, default='')
    language_version = models.CharField('语言版本', max_length=20, null=True)
    screening_mode = models.CharField('屏幕模式', max_length=20, null=True)
    date = models.DateField('排场日期-用于抓取排重')
    movie = models.ForeignKey(Movie, to_field='outid')
    cinema = models.ForeignKey(Cinema, to_field='outid')
    hall_num = models.CharField('厅号', max_length=100, null=True)
    city = models.ForeignKey(City, to_field='cityid')
    endtime = models.DateTimeField('结束时间',null=True)
    bycbk = models.IntegerField('是否营业',choices=FILMSESSION_HALL_BYCBK_CHOICES,default=1)
    class Meta:
        db_table = u'filmsession_hall'
        verbose_name = '影片排场'
        verbose_name_plural = '影片排场'

class Movie_Will_City(models.Model):
    movie = models.ForeignKey(Movie, to_field='outid')
    city = models.ForeignKey(City, to_field='cityid')

    def __unicode__(self):
        return self.movie.title
    class Meta:
        db_table = u'movie_will_city'
        verbose_name = "即将上映影片和城市关联关系"
        verbose_name_plural = "即将上映影片和城市关联关系"

class Area(models.Model):
    cityid = models.CharField('城市id', max_length=100)
    cityname = models.CharField('城市名称', max_length=100)
    districtid = models.CharField('城区id', max_length=100, unique=True)
    districtname = models.CharField('城区名称', max_length=100)
    class Meta:
        db_table = u'area'

class DistrictCinema(models.Model):
    district = models.ForeignKey(Area, to_field='districtid')
    cinema = models.OneToOneField(Cinema, to_field='outid')
    class Meta:
        db_table = u'districtcinema'

class ClientUser(models.Model):
    username = models.CharField('用户名', max_length=100, null=True)
    age = models.CharField('年龄', max_length=100, null=True)
    gender = models.CharField('性别', max_length=100, null=True)
    password = models.CharField('密码', max_length=100, null=True)
    portrait_imgurl = models.CharField('头像地址', max_length=400, null=True)
    prefix = models.CharField('随机前缀', max_length=6)
    class Meta:
        db_table = u'clientuser'

LYK_CLIENT_PLATFORM = (
    (0, 'iphone'),
    (1, 'android'),
)

LYK_CLIENT_STATUS = (
    (0, '下线'),
    (1, '上线'),
)

class ClientVersion(models.Model):
    title = models.CharField('版本更新名称', max_length=20)
    content = models.CharField('版本更新内容', max_length=400)
    size = models.CharField('版本文件大小', max_length=15)
    client_version = models.CharField('版本号', max_length=12)
    platform = models.IntegerField('客户端平台', choices=LYK_CLIENT_PLATFORM)
    dl_url = models.FileField('下载地址', upload_to='client/dl', blank=True, null=True, max_length=500)
    dl_url2 = models.CharField('下载地址2', max_length=400, blank=True)
    status = models.IntegerField('状态', choices=LYK_CLIENT_STATUS, default=0)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)

    def __unicode__(self):
        return self.title
    class Meta:
        db_table = u'clientversion'
        verbose_name = "客户端版本"
        verbose_name_plural = "客户端版本"

class ClientLogFile(models.Model):
    createtime = models.DateTimeField('创建时间', auto_now_add=True)
    file_url = models.FileField('下载地址', upload_to='client/log', blank=True, null=True, max_length=500)

    def __unicode__(self):
        return self.file_url.url
    class Meta:
        db_table = u'clientlogfile'
        verbose_name = "客户端日志"
        verbose_name_plural = "客户端日志"

class UserPhoneNumber(models.Model):
    phonenumber = models.CharField('手机号', max_length=100)
    clientuser = models.ForeignKey(ClientUser)
    class Meta:
        db_table = u'userphonenumber'

class ClientDevice(models.Model):
    mac = models.CharField('MAC地址', max_length=100)
    device_name = models.CharField('设备名', max_length=50)
    device_version = models.CharField('设备版本', max_length=50)
    device_model = models.CharField('设备型号', max_length=50)
    screen_size = models.CharField('屏幕尺寸', max_length=15)
    client_version =  models.CharField('客户端版本', max_length=15)
    clientuser = models.ForeignKey(ClientUser)
    class Meta:
        db_table = u'clientdevice'

class Condition4Cinema(models.Model):
    key = models.CharField('URL中key值', max_length=5)
    name = models.CharField('条件名称', max_length=20)
    city = models.ForeignKey(City, to_field='cityid')

    def __unicode__(self):
        return self.name
    class Meta:
        db_table = u'condition4cinema'
        verbose_name = "影院筛选条件"
        verbose_name_plural = "影院筛选条件"

LYK_ACTIVITY_OP_CHOICES = (
    (0, '打开URL'),
    (1, '进入影片页'),
    (2, '进入影院页'),
    (3, '进入排场页'),
    (4, '进入活动列表页'),
)

LYK_ACTIVITY_ICON_CHOICES = (
    (0, '首映'),
    (1, '抢票'),
    (2, '团购'),
    (3, 'APP推荐'),
    (4, '特惠'),
)

LYK_ACTIVITY_STATUS_CHOICES = (
    (0, '下线'),
    (1, '即将上线'),
    (2, '上线'),
)

LYK_ACTIVITY_PINTYPE_CHOICES = (
    (0, '黑色无图标'),
    (1, '蓝色有图标'),
    (2, '红色有图标'),
)
class ActivityType(models.Model):
    name = models.CharField('活动类型名称',max_length=200,unique=True)
    introduction = models.TextField('活动类型说明')
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'activitytype'
        verbose_name = "活动类型"
        verbose_name_plural = '活动类型'
G_CHOICES=(
    (0,'运营组'),
    (1,'影院组'),
)

LYK_ACTIVITY_WM_CHOICES = (
    (0, '都显示'),
    (1, '网站显示'),
    (2, '手机显示'),
)

LYK_ACTIVITY_LISTTYPE_CHOICES = (
    (0, '默认'),
    (1, '显示在主题列表'),
    (2, '显示在优惠列表'),
    (3, '不显示在主题列表'),
    (4, '不显示在优惠列表'),
)

class Activity(models.Model):
    title = models.CharField('活动标题', max_length=100)
    image_url = models.CharField('活动图片', max_length=400,blank=True)
    img_url = models.ImageField('活动图片',upload_to = 'activity/img/')
    introduction = models.CharField('活动广告语', max_length=400)
    description = models.TextField('活动详情')
    starttime = models.DateTimeField('开始时间')
    endtime = models.DateTimeField('结束时间')
    optype = models.IntegerField('操作类型', choices=LYK_ACTIVITY_OP_CHOICES)
    data = models.CharField('操作数据', max_length=500)
    activitytype = models.ForeignKey(ActivityType,verbose_name = '活动类型')
    icontype = models.IntegerField('活动类型', choices=LYK_ACTIVITY_ICON_CHOICES)
    iconname = models.CharField('活动icon名称', max_length=4)
    iconurl = models.CharField('活动iconURL', max_length=400)
    iconcolor = models.CharField('活动icon色值RGB', max_length=20)
    status = models.IntegerField('活动状态', choices=LYK_ACTIVITY_STATUS_CHOICES)
    url = models.CharField('活动URL', max_length=400)
    outid = models.CharField('外链id', max_length=45)
    index = models.IntegerField('排序', max_length=5, default=0)
    citys = models.ManyToManyField(City,db_table=u'activitys_citys')
    signup_starttime = models.DateTimeField('报名开始时间',blank=True)
    signup_endtime = models.DateTimeField('报名结束时间',blank=True)
    ownertype = models.IntegerField('组类型',choices = G_CHOICES)
    webormobile = models.IntegerField('网站手机显示类型', choices=LYK_ACTIVITY_WM_CHOICES, default=0)
    img_compress_url = models.CharField('活动图片URL-压缩后', max_length=400)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)
    updatetime = models.DateTimeField('更新时间', auto_now=True)
    listtype = models.IntegerField('列表类型', choices=LYK_ACTIVITY_LISTTYPE_CHOICES, default=0)

    def __unicode__(self):
        return self.title
    class Meta:
        db_table = u'activity'
        verbose_name = "活动"
        verbose_name_plural = "活动"

class Activity_Movie(models.Model):
    activity = models.ForeignKey(Activity)
    movie = models.ForeignKey(Movie)
    optype = models.IntegerField('操作类型', choices=LYK_ACTIVITY_OP_CHOICES)

    def __unicode__(self):
        return ''.join([self.activity.title, '-', self.movie.title])
    class Meta:
        db_table = u'activitys_movies'
        verbose_name = "对应影片的活动"
        verbose_name_plural = "对应影片的活动"

class Activity_Cinema(models.Model):
    activity = models.ForeignKey(Activity)
    cinema = models.ForeignKey(Cinema)
    optype = models.IntegerField('操作类型', choices=LYK_ACTIVITY_OP_CHOICES)
    pintype = models.IntegerField('展现类型', choices=LYK_ACTIVITY_PINTYPE_CHOICES)

    def __unicode__(self):
        return ''.join([self.activity.title, '-', self.cinema.name])
    class Meta:
        db_table = u'activitys_cinemas'
        verbose_name = "对应影院的活动"
        verbose_name_plural = "对应影院的活动"

class Application(models.Model):
    title = models.CharField('应用名称', max_length=100)
    image_url = models.CharField('应用icon', max_length=400)
    introduction = models.CharField('应用简介', max_length=400)
    download_url = models.CharField('应用下载地址', max_length=400)
    createtime = models.DateTimeField('创建时间')
    movies = models.ManyToManyField(Movie,db_table=u'applications_movies')
    cinemas = models.ManyToManyField(Cinema,db_table=u'applications_cinemas')
    citys = models.ManyToManyField(City,db_table=u'applications_citys')
    class Meta:
        db_table = u'application'

LYK_ORDER_PAY_STATUS_CHOICES = (
    (0, '未支付'),
    (1, '已支付'),
)

# 用于15分钟失效状态标识
LYK_ORDER_STATUS_CHOICES = (
    (0, '有效'),
    (1, '失效'), # 订单生成超时， 同一用户生成第二个订单时，前面的未支付并有效的订单改成失效
)

class TicketOrder(models.Model):
    createtime = models.DateTimeField('创建时间')
    updatetime = models.DateTimeField('更新时间')
    ticketcount = models.IntegerField('购票数量')
    totalprice = models.CharField('总购票价格', max_length=20)
    seatinfos = models.CharField('座位号', max_length=400)
    phonenum = models.CharField('接收取票码手机号', max_length=20)
    cdkey = models.CharField('兑换码', max_length=100)
    pay_status = models.IntegerField('订单支付状态', choices=LYK_ORDER_PAY_STATUS_CHOICES)
    status = models.IntegerField('订单状态', choices=LYK_ORDER_STATUS_CHOICES)
    filmsession = models.ForeignKey(Filmsession_hall)
    clientuser = models.ForeignKey(ClientUser)
    class Meta:
        db_table = u'ticketorder'

class BookSeatChannel(models.Model):
    cname = models.CharField('渠道名称', max_length=100, default=u'乐影客')
    ckey = models.CharField('渠道KEY', max_length=100, default='leyingke')
    cinemas = models.ManyToManyField(Cinema, db_table='channels_cinemas')
    filmsessions = models.ManyToManyField(Filmsession_hall, db_table='channels_filmsessions')
    class Meta:
        db_table = u'bookseatchannel'

LYK_FAVORITE_TYPE_CHOICES = (
    (0, '影院'),
    (1, '影片'),
    (2, '活动'),
)

LYK_FAVORITE_STATUS_CHOICES = (
    (1, '加关注'),
    (-1, '取消关注'),
)

class Favorite(models.Model):
    ftype = models.IntegerField('关注类型', choices=LYK_FAVORITE_TYPE_CHOICES)
    data = models.CharField('数据ID', max_length=100)
    status = models.IntegerField('关注状态', choices=LYK_FAVORITE_STATUS_CHOICES)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)
    updatetime = models.DateTimeField('更新时间', auto_now=True)
    clientuser = models.ForeignKey(ClientUser)
    class Meta:
        db_table = u'favorite'

ACTIVITY_SESSION_ONLINE_STATUS_CHOICE = (
    (1, '上线'),
    (0, '下线'),
)

ACTIVITY_SESSION_FULL_STATUS_CHOICE = (
    (1, '已满员'),
    (0, '未满员'),
)

class Activity_Session(models.Model):
#    activity = models.ForeignKey(Activity)
#    cinema = models.ForeignKey(Cinema)
    activity_cinema = models.ForeignKey(Activity_Cinema)
    showtime = models.DateTimeField('放映时间', blank=True)
    price = models.FloatField('价格', blank=True)
    baseusernum = models.IntegerField('参与用户基数-手动修改', max_length=5, default=0)
    payusernum = models.IntegerField('参与用户数', max_length=5, default=0)
    onlinestatus = models.IntegerField('在线状态', choices=ACTIVITY_SESSION_ONLINE_STATUS_CHOICE, default=0)
    fullstatus = models.IntegerField('满员状态', choices=ACTIVITY_SESSION_FULL_STATUS_CHOICE, default=0)
    maxusernum = models.IntegerField('最大参与用户数', max_length=5, default=100)
    class Meta:
        db_table = u'activity_session'

USERACTIVITY_PAY_STATUS_CHOICE = (
    (1, '已支付'),
    (0, '未支付'),
)

class UserActivity(models.Model):
    clientuser = models.ForeignKey(ClientUser, blank=True)
    phonenum = models.CharField('手机号', max_length=100, blank=True)
    activity = models.ForeignKey(Activity, blank=True)
    activity_session = models.ForeignKey(Activity_Session, blank=True)
    city = models.ForeignKey(City, blank=True)
    activity_movie = models.ForeignKey(Activity_Movie, blank=True)
    activity_cinema = models.ForeignKey(Activity_Cinema, blank=True)
    paystats = models.IntegerField('支付状态', choices=USERACTIVITY_PAY_STATUS_CHOICE, default=0)
    cdkey = models.TextField('兑换码')
    createtime = models.DateTimeField('创建时间', auto_now_add=True)
    updatetime = models.DateTimeField('更新时间', auto_now=True)
    ticketnum = models.IntegerField('购买票数', default=0)
    exchangedcdkey = models.TextField('已兑换的兑换码')
    class Meta:
        db_table = u'useractivity'

class UserActivity_Exchangedcdkey(models.Model):
    useractivity = models.ForeignKey(UserActivity, blank=True)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)
    exchangedcdkey = models.CharField('已兑换的兑换码', max_length=100, blank=True)
    class Meta:
        db_table = u'useractivity_exchangedcdkey'

def get_manager_path(instance,name):
    return 'activity/icon/%d/%s'% (instance.parent.id,name)


class Activity_Bar_Manager(models.Model): #
    parent = models.ForeignKey(ActivityType)
    title = models.CharField('图片名',max_length=30)
    img = models.ImageField('图片',upload_to=get_manager_path)#os.path.abspath(os.path.dirname(__file__)))
    class Meta:
        db_table = u"activity_bar_manager"

class UploadFilmSessionLog(models.Model):
    identify = models.CharField('标识',max_length = 100)
    upload_time = models.DateTimeField('创建时间', auto_now_add=True)
    ticket_platform = models.CharField('票务平台', max_length=100)
    show_time = models.CharField('排片日期',max_length=100)
    status = models.CharField('状态',max_length=100,default='未提交')
    class Meta:
        db_table = 'uploadfilmsessionlog'
        verbose_name = u"排场信息上传log表"
        verbose_name_plural = u'排场信息上传log表'

class AppManager(models.Model):
    name = models.CharField('名称', max_length=100)
    advertisement = models.TextField('广告语',blank=True)
    introduction = models.TextField('介绍',blank=True)
    attachment = models.FileField('下载包文件地址',upload_to = 'app/upload',blank=True)
    movies = models.ManyToManyField(Movie)
    cinemas = models.ManyToManyField(Cinema)
    platform = models.CharField('支持平台',max_length=100,blank=True)
    status = models.CharField('状态',max_length=100,default= '上线')
    index = models.IntegerField('排序',max_length=10,default=0)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'App管理'
        db_table = u'appmanager'
        verbose_name_plural = 'App管理'

class AppPicture(models.Model):
    appmanager = models.ForeignKey(AppManager)
    poster_pic = models.ImageField('海报图片',upload_to = 'app/poster/',blank=True)
    client_pic = models.ImageField('客户端图标',upload_to = 'app/client/',blank=True)
    web_pic = models.ImageField('网站图标',upload_to = 'app/web/',blank=True)
    class Meta:
        db_table = 'apppicture'
        verbose_name = u'App图片信息'
        verbose_name_plural = u'App图片信息'

class FilmsessionFile(models.Model): # todo 组id
    identify = models.CharField('标识',max_length = 100)
    showtime = models.DateTimeField('放映时间', null=True)
    price = models.IntegerField('现价', null=True)
    price_ori = models.IntegerField('原价', null=True)
    language_version = models.CharField('语言版本', max_length=20, null=True)
    screening_mode = models.CharField('屏幕类型', max_length=20, null=True)
    date = models.DateField('排场日期-用于抓取排重')
    movie = models.ForeignKey(Movie, to_field='outid')
    cinema = models.ForeignKey(Cinema, to_field='outid')
    hall_num = models.CharField('影厅号', max_length=100, null=True)
    city = models.ForeignKey(City, to_field='cityid')
    showdate = models.CharField('放映日期',max_length=100)
    start = models.CharField('放映时间',max_length=100,blank=True)
    end = models.CharField('结束时间',max_length=100,blank=True)
    mins = models.CharField('片长',max_length=50)
    class Meta:
        db_table = u'filmsessionfile'
        verbose_name = '影片排场备份'
        verbose_name_plural ='影片排场备份'

class Movie_News_List(models.Model):
    title = models.CharField('题目', max_length=100)
    url = models.CharField('外链接地址', max_length=500)
    source = models.CharField('来源', max_length=100, blank=True)
    pubtime = models.DateTimeField('发布时间', max_length=100, blank=True)
    img_url = models.CharField('图片地址', max_length=100, blank=True)
    content = models.TextField('内容', blank=True)
    index = models.IntegerField('排序', max_length=5, default=0)
    movie = models.ForeignKey(Movie)

    def __unicode__(self):
        return self.title
    class Meta:
        db_table = u'movie_news_list'
        verbose_name = "电影报道"
        verbose_name_plural = "电影报道"

class IP_City(models.Model):
    ip = models.CharField('IP地址', max_length=32)
    cityid = models.CharField('城市id', max_length=100)
    class Meta:
        db_table = u'ip_city'

G_CHOICES =(
    (0,'影院组'),
    (1,'院线经理'),
    (2,'KPI组'),
    (3,'小区组'),
    (4,'大区组'),
    (5,'全国组')
)

class Group(models.Model):
    name = models.CharField('用户组名',max_length=100)
    type = models.IntegerField('类别',max_length=5,choices=G_CHOICES)
    cinemas = models.ManyToManyField(Cinema)
    parent = models.ForeignKey('self')
    class Meta :
        db_table ='group'

class CBKUser(models.Model):
    username = models.CharField('用户名', max_length=30, unique=True)
    email = models.EmailField('邮箱', blank=True)
    phonenumber = models.CharField('电话号码',max_length=100)
    password = models.CharField('密码', max_length=128)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)
    updatetime = models.DateTimeField('更新时间', auto_now=True)
    group = models.ForeignKey(Group)
    class Meta:
        db_table = 'cbkuser'

class HallFeatrue(models.Model):
    type = models.CharField('影厅特色',max_length=100)
    index = models.IntegerField('排序',default=1)
    class Meta:
        db_table = 'hallfeature'

class Hall(models.Model):
    name =models.CharField('影厅名称',max_length=100)
    seat_num = models.IntegerField('座位数',default=0)
    cinema = models.ForeignKey(Cinema)
    class Meta:
        db_table = 'cinemahall'

class Hall_Type_ref(models.Model):
    hall = models.ForeignKey(Hall)
    halltype = models.ForeignKey(HallFeatrue)
    content = models.CharField('内容',max_length=100,blank=True)
    class Meta:
        db_table = 'hall_type_ref'

SEAT_TYPE_CHOICE = (
    (0,'通道'),
    (1,'座位'),
    (2,'空座位')
)
class Seat(models.Model):
    name = models.CharField('座位',max_length=100)
    col = models.IntegerField('列')
    vol = models.IntegerField('行')
    type = models.IntegerField('类型',choices=SEAT_TYPE_CHOICE)
    hall = models.ForeignKey(Hall)
    class Meta:
        db_table = 'seat'

USE_STATUS_CHOICE = (
    (1,"平台可用"),
    (0,"平台不可用"),
)
class Platform(models.Model):
    name = models.CharField('平台名称',max_length=100)
    status = models.IntegerField('是否可用',choices=USE_STATUS_CHOICE,default=0)
    remark = models.TextField("备注")
    index = models.IntegerField('排序', default=1)
    class Meta:
        db_table = 'platform'

class Platform_Cinema_ref(models.Model):
    platform = models.ForeignKey(Platform)
    cinema = models.ForeignKey(Cinema)
    class Meta:
        db_table = 'platform_cinema_ref'
class Book_Office(models.Model):
    date = models.DateField('考勤日期')
    cinema = models.ForeignKey(Cinema)
    movie = models.ForeignKey(Movie)
    session_count = models.IntegerField('排场数',blank=True,null=True)
    person_time = models.IntegerField('人次',blank=True,null=True)
    bookoffice = models.DecimalField('票房', max_digits=14,decimal_places=2,blank=True,null=True)
    zzb_session_count = models.IntegerField('zzb排场数',blank=True,null=True)
    zzb_person_time = models.IntegerField('zzb人次',blank=True,null=True)
    zzb_bookoffice = models.DecimalField('zzb票房', max_digits=14,decimal_places=2,blank=True,null=True)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)
    updatetime = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table='book_office'
        verbose_name = '票房'
        verbose_name_plural = '票房'

class Hall_Equipment(models.Model):
    hall = models.ForeignKey(Hall)
    equipment = models.ForeignKey(Equipment)
    cinema = models.ForeignKey(Cinema)
    class Meta:
        db_table = 'hall_equipment'
MALE_CHOICE = (
    (2,'备用'),
    (1,"男性"),
    (0,"女性"),
)
POSITION_CHOICE = (
    (1,'总经理'),
    (0,'排片负责人'),
)
class Cinema_Worker(models.Model):
    name = models.CharField('姓名',max_length=200)
    mobile = models.CharField('移动电话',max_length=200,blank=True)
    telephone = models.CharField('固定电话',max_length=200,blank=True)
    email = models.EmailField('邮箱',blank=True)
    qqmsn = models.CharField('qq or msn',max_length=200,blank=True)
    gender = models.IntegerField('性别',choices=MALE_CHOICE,default=1)
    birthday = models.DateField('生日',blank=True, null=True)
    weibo = models.URLField('微博',blank=True)
    position = models.IntegerField('职位',choices=POSITION_CHOICE)
    cinema = models.ForeignKey(Cinema)
    class Meta:
        db_table = 'cinema_worker'

class Cinema_ZZB(models.Model):
    zzb_id = models.CharField('zzb对应表',max_length=100)
    cinema = models.ForeignKey(Cinema,blank=True)
    zzb_cinema_name = models.CharField("专资办-影院名称",blank=True,max_length=100)
    zzb_circuit_name = models.CharField("专资办-院线名称",blank=True,max_length=100)
    def __unicode__(self):
        return self.zzb_cinema_name
    class Meta:
        db_table = 'cinema_zzb'

class Filmsession_hall_bak(models.Model):
    showtime = models.DateTimeField('放映时间', null=True)
    mins = models.CharField('片长',max_length=50,blank=True)
    price = models.CharField('现价', max_length=10, null=True, default='')
    price_ori = models.CharField('原价', max_length=10, null=True, default='')
    language_version = models.CharField('语言版本', max_length=20, null=True)
    screening_mode = models.CharField('屏幕模式', max_length=20, null=True)
    date = models.DateField('排场日期-用于抓取排重')
    movie = models.ForeignKey(Movie, to_field='outid')
    cinema = models.ForeignKey(Cinema, to_field='outid')
    hall_num = models.CharField('厅号', max_length=100, null=True)
    city = models.ForeignKey(City, to_field='cityid')
    endtime = models.DateTimeField('结束时间',null=True)
    bycbk = models.IntegerField('是否营业',choices=FILMSESSION_HALL_BYCBK_CHOICES,default=1)
    class Meta:
        db_table = u'filmsessionbakhall'
        verbose_name = '影片排场'
        verbose_name_plural = '影片排场'

class Book_Office_ZZB(models.Model):
    date = models.DateField('考勤日期')
    cinema = models.ForeignKey(Cinema)
    total_session_count = models.IntegerField('zzb_total排场数',blank=True,null=True)
    total_person_time = models.IntegerField('zzb_total人次',blank=True,null=True)
    total_bookoffice = models.DecimalField('zzb_total票房', max_digits=14,decimal_places=2,blank=True,null=True)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)
    updatetime = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table='book_office_zzb'
        verbose_name = '专资办总票房'
        verbose_name_plural = '专资办总票房'

class TaoBao_Cinema(models.Model):
    tb_cinema_id = models.CharField('淘宝影院id', max_length=32)
    tb_cinema_name = models.CharField('淘宝影院名称', max_length=100)
    tb_cinema_url = models.CharField('淘宝影院url', max_length=400)
    tb_cinema_seat_url = models.CharField('淘宝影院在线选座url', max_length=400, null=True, blank=True)
    tb_cinema_coupon_url = models.CharField('淘宝影院买兑换券url', max_length=400, null=True, blank=True)
    city_pinyin = models.CharField('城市拼音', max_length=100)
    cinema = models.OneToOneField(Cinema, null=True)
    class Meta:
        db_table = u'taobao_cinema'

