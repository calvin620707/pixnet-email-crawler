from django import views
from django.contrib import messages
from django.shortcuts import render
from pathlib import Path
import json


from crawlers.forms import StartForm
from cli import Crawler


class IndexView(views.View):
    def get(self, request):
        form = StartForm()
        return render(request, 'crawlers/index.html', {'form': form})

    def post(self, request):
        form = StartForm(request.POST)
        if not form.is_valid():
            messages.error(request, "表單無效")
            return render(request, 'crawlers/index.html')
        c = Crawler()
        c.get(form.cleaned_data['pixnet_url'])
        with Path(c.scraped_ret_file).open('r') as f:
            ret_json = json.load(f)
            ret_json = list(map(lambda x: self.update_err_msg(x), ret_json))
            return render(request, 'crawlers/results.html', {'scraped': ret_json})

    def update_err_msg(self, row):
        if 'errors' not in row:
            row['err_msg'] = ''
            return row

        if 'is secret' in row['errors']:
            row['err_msg'] = "悄悄話"
        if 'email not found' in row['errors']:
            if row.get('err_msg'):
                row['err_msg'] += ', '
            else:
                row['err_msg'] = ''
            row['err_msg'] += "找不到Email"
        return row
