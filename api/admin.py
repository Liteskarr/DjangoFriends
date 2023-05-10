from django.contrib import admin

import api.models as models


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.User, UserAdmin)


class FriendsRequestAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.FriendRequest, FriendsRequestAdmin)
