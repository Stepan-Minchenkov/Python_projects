from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


# content_type = ContentType.objects.get(app_label='auth', model='user')
# permission = Permission.objects.create(codename='registered_customer',
#                                        name='Registered Customer',
#                                        content_type=content_type)   # creating permissions
# group, created = Group.objects.get_or_create(name='Customers')
# group.permissions.add(permission)
#
# content_type = ContentType.objects.get(app_label='auth', model='user')
# permission = Permission.objects.create(codename='manager',
#                                        name='Manager',
#                                        content_type=content_type)   # creating permissions
# group, created = Group.objects.get_or_create(name='Managers')
# group.permissions.add(permission)
#
# content_type = ContentType.objects.get(app_label='auth', model='user')
# permission = Permission.objects.create(codename='admin',
#                                        name='Admin',
#                                        content_type=content_type)   # creating permissions
# group, created = Group.objects.get_or_create(name='Admin')
# group.permissions.add(permission)

# Permission.objects.filter(codename="registered_customer").delete()
# Permission.objects.filter(codename="manager").delete()
# Permission.objects.filter(codename="admin").delete()

permissions = Permission.objects.filter(codename__in=(
    "admin",
    "add_logentry", "change_logentry", "delete_logentry", "view_logentry",
    "add_group", "change_group", "delete_group", "view_group",
    "add_permission", "change_permission", "delete_permission", "view_permission",
    "add_user", "change_user", "delete_user", "view_user",
    "add_basket", "change_basket", "delete_basket", "view_basket",
    "add_book", "change_book", "delete_book", "view_book",
    "add_customer", "change_customer", "delete_customer", "view_customer",
    "add_goodsinbasket", "change_goodsinbasket", "delete_goodsinbasket", "view_goodsinbasket",
    "add_contenttype", "change_contenttype", "delete_contenttype", "view_contenttype",
    "add_author", "change_author", "delete_author", "view_author",
    "add_genre", "change_genre", "delete_genre", "view_genre",
    "add_publisher", "change_publisher", "delete_publisher", "view_publisher",
    "add_serie", "change_serie", "delete_serie", "view_serie",
    "add_session", "change_session", "delete_session", "view_session",
    "add_basketcomments", "change_basketcomments", "delete_basketcomments", "view_basketcomments",
    "add_bookcomments", "change_bookcomments", "delete_bookcomments", "view_bookcomments"
                                        ))
group = Group.objects.get(name='Admin')
for permission in permissions:
    group.permissions.add(permission)

permissions = Permission.objects.filter(codename__in=(
    "manager",
    "add_user", "change_user", "view_user",
    "change_basket", "view_basket",
    "add_book", "change_book", "delete_book", "view_book",
    "add_customer", "change_customer", "view_customer",
    "add_goodsinbasket", "change_goodsinbasket", "delete_goodsinbasket", "view_goodsinbasket",
    "add_author", "change_author", "delete_author", "view_author",
    "add_genre", "change_genre", "delete_genre", "view_genre",
    "add_publisher", "change_publisher", "delete_publisher", "view_publisher",
    "add_serie", "change_serie", "delete_serie", "view_serie",
    "add_basketcomments", "change_basketcomments", "delete_basketcomments", "view_basketcomments",
    "add_bookcomments", "change_bookcomments", "delete_bookcomments", "view_bookcomments"
                                        ))
group = Group.objects.get(name='Managers')
for permission in permissions:
    group.permissions.add(permission)

permissions = Permission.objects.filter(codename__in=(
    "registered_customer",
    "add_user", "change_user", "view_user",
    "add_basket", "change_basket", "delete_basket", "view_basket",
    "view_book",
    "add_customer", "change_customer", "view_customer",
    "add_goodsinbasket", "change_goodsinbasket", "delete_goodsinbasket", "view_goodsinbasket",
    "view_author",
    "view_genre",
    "view_publisher",
    "view_serie",
    "add_basketcomments", "view_basketcomments",
    "add_bookcomments", "view_bookcomments"
                                        ))
group = Group.objects.get(name='Customers')
for permission in permissions:
    group.permissions.add(permission)
