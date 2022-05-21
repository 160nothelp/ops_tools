from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser

# from assets.models import ItemModel


class UserProfile(AbstractUser):
    """
    用户类拓展
    """
    avatar = models.CharField(max_length=100, null=True, blank=True,
                              default='https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                              verbose_name="头像地址")

    introduction = models.TextField(max_length=500, null=True, blank=True, verbose_name="introduction")
    role = models.ManyToManyField('RoleModel', verbose_name='所拥有的角色', related_name="users", blank=True)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class PermissionModel(models.Model):
    """
    权限表
    """
    permission_choice = (
        (0, '只读'),
        (1, '修改'),
        (2, '删除'),
    )

    title = models.CharField(verbose_name='标题', max_length=32)
    read_or_edit = models.SmallIntegerField(choices=permission_choice, default=0)
    # Permission_Item = models.ForeignKey(ItemModel, null=True, blank=True,
    #                                     on_delete=models.SET_NULL,
    #                                     related_name='ItemModel_to_Permission')

    class Meta:
        verbose_name = "权限"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class RoleModel(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField('PermissionModel', verbose_name='拥有的权限', related_name="roles", blank=True)
    menu = models.ManyToManyField('MenuModel', verbose_name='拥有的菜单', related_name="roles", blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class MenuModel(models.Model):
    """
    菜单
    """
    # operate_type = {
    #     'add': '新增',
    #     'del': '删除',
    #     'update': '编辑',
    #     'view': '查看',
    # }

    MENU_TYPE = (
        (1, "一级菜单"),
        (2, "二级菜单"),
        (3, "三级菜单"),
    )

    title = models.CharField(max_length=32, unique=True, verbose_name='菜单名称')
    menu_type = models.IntegerField(choices=MENU_TYPE, verbose_name="类目级别")
    parent = models.ForeignKey("MenuModel", null=True, blank=True, on_delete=models.SET_NULL,
                               verbose_name='父级菜单', related_name='children')
    code = models.CharField(max_length=64, default='#', verbose_name='菜单对应组件路径')
    icon = models.CharField(max_length=128, null=True, blank=True, verbose_name='icon样式')
    curl = models.CharField(max_length=101, default='#', verbose_name='菜单URL')
    hidden = models.BooleanField(default=False, verbose_name='菜单是否隐藏')
    # operate = models.CharField(max_length=11, choices=tuple(operate_type.items()), default='none',
    #                            verbose_name='菜单对应功能类型')
    redirect = models.CharField(max_length=101, default='#', verbose_name='菜单跳转url')
    active_menu = models.CharField(max_length=101, default='#', verbose_name='指定高亮')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name = "菜单"
        verbose_name_plural = verbose_name

    def __str__(self):
        # 显示层级菜单
        title_list = [self.title]
        p = self.parent
        while p:
            title_list.insert(0, p.title)
            p = p.parent
        return '菜单名: ' + '-->'.join(title_list) + ' 当前菜单为：(%s级菜单)' % self.menu_type


