from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.functions import TruncDate
from django.db.models import Count
from .models import UsageReportProxy, LoginEvent
from django.contrib.auth.models import User
import plotly.graph_objs as go
import plotly.offline as opy

@admin.register(UsageReportProxy)
class UsageReportAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        start_date = request.GET.get('start', (now() - timedelta(days=7)).date().isoformat())
        end_date = request.GET.get('end', now().date().isoformat())

        # User signups
        user_signups = User.objects.filter(date_joined__date__range=[start_date, end_date])
        signup_counts = user_signups.annotate(date=TruncDate('date_joined')) \
            .values('date').annotate(count=Count('id')).order_by('date')

        # Logins
        login_counts = LoginEvent.objects.filter(timestamp__date__range=[start_date, end_date]) \
            .annotate(date=TruncDate('timestamp')) \
            .values('date').annotate(count=Count('id')).order_by('date')

        signup_dates = [x['date'].isoformat() for x in signup_counts]
        signup_values = [x['count'] for x in signup_counts]

        login_dates = [x['date'].isoformat() for x in login_counts]
        login_values = [x['count'] for x in login_counts]

        signup_trace = go.Scatter(x=signup_dates, y=signup_values, mode='lines+markers', name='Signups')
        login_trace = go.Scatter(x=login_dates, y=login_values, mode='lines+markers', name='Logins')

        layout = go.Layout(title='User Signups & Logins', xaxis={'title': 'Date'}, yaxis={'title': 'Count'})
        fig = go.Figure(data=[signup_trace, login_trace], layout=layout)
        chart_html = opy.plot(fig, auto_open=False, output_type='div')

        extra_context = extra_context or {}
        extra_context.update({
            'title': 'Usage Report',
            'chart': chart_html,
            'start': start_date,
            'end': end_date
        })

        return TemplateResponse(request, "admin/usage_report.html", extra_context)
