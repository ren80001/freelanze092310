from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager


SKILLS = (
    ('1', 'Webデザイナー'),
    ('2', 'PG(フロントサイド)'),
    ('3', 'PG(サーバーサイド)'),
    ('4', 'デザイナー'),
    ('5', 'フォトグラファー'),
    ('6', 'イラストレーター'),
    ('7', 'ライター'),
    ('8', 'ブロガー'),
)

AREAS = (
    ('1', 'オンライン'),
    ('2', '北海道'),
    ('3', '青森県'),
    ('4', '岩手県'),
    ('5', '宮城県'),
    ('6', '秋田県'),
    ('7', '山形県'),
    ('8', '福島県'),
    ('9', '茨城県'),
    ('10', '栃木県'),
    ('11', '群馬県'),
    ('12', '埼玉県'),
    ('13', '千葉県'),
    ('14', '東京都'),
    ('15', '神奈川県'),
    ('16', '新潟県'),
    ('17', '富山県'),
    ('18', '石川県'),
    ('19', '福井県'),
    ('20', '山梨県'),
    ('21', '長野県'),
    ('22', '岐阜県'),
    ('23', '静岡県'),
    ('24', '愛知県'),
    ('25', '三重県'),
    ('26', '滋賀県'),
    ('27', '京都府'),
    ('28', '大阪府'),
    ('29', '兵庫県'),
    ('30', '奈良県'),
    ('31', '和歌山県'),
    ('32', '鳥取県'),
    ('33', '島根県'),
    ('34', '岡山県'),
    ('35', '広島県'),
    ('36', '山口県'),
    ('37', '徳島県'),
    ('38', '香川県'),
    ('39', '愛媛県'),
    ('40', '高知県'),
    ('41', '福岡県'),
    ('42', '佐賀県'),
    ('43', '長崎県'),
    ('44', '熊本県'),
    ('45', '大分県'),
    ('46', '宮崎県'),
    ('47', '鹿児島県'),
    ('48', '沖縄県'),
)

REQUESTS = (
    ('1', '応相談'),
    ('2', '無料'),
    ('3', '〜10,000円'),
    ('4', '10,000円〜'),
    ('5', '50,000円〜'),
    ('6', '100,000円〜'),
    ('7', '500,000円〜'),

)

class UserManager(BaseUserManager):
    """ユーザーマネージャー."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """メールアドレスでの登録を必須にする"""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """is_staff(管理サイトにログインできるか)と、is_superuer(全ての権限)をFalseに"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """スーパーユーザーは、is_staffとis_superuserをTrueに"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル."""

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    nick_name = models.CharField(_('ニックネーム'), max_length=30, blank=False)
    image = models.ImageField(('トップ画像'), upload_to='media/', blank=True)  # 画像はあとで解決する
    twitter = models.URLField(('Twitterアカウント'), blank=True)
    instagram = models.URLField(('Instagramアカウント'), max_length=150, blank=True)
    skill = models.CharField(('スキル'), max_length=150, choices=SKILLS, blank=True)
    area = models.CharField(('活動範囲'), max_length=150, choices=AREAS, blank=False)
    request_fee = models.CharField(('依頼料'), max_length=20, choices=REQUESTS, blank=False)
    portfolio = models.CharField(('ポートフォリオ'), max_length=150, blank=True)
    self_introduction = models.CharField(_('自己PR'), max_length=500, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        """username属性のゲッター

        他アプリケーションが、username属性にアクセスした場合に備えて定義
        メールアドレスを返す
        """
        return self.email