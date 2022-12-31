from django.contrib import admin

from Split.models import Transaction

# register the transaction model
class TransationAdmin(admin.ModelAdmin):
    model = Transaction
    fields = ['amount', 'title', 'split_between_users', 'paid_by']
    list_display = ['amount', 'title', 'get_split_between_users', 'paid_by']

    def get_split_between_users(self, obj):
        return ", ".join([u.username for u in obj.split_between_users.all()])


admin.site.register(Transaction, TransationAdmin)