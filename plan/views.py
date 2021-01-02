import io

from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import F, Q, Sum
from django.http import HttpResponse
from django.shortcuts import render
from .resources import PlanResource
from .models import TestUpload, Plan
import pandas as pd
from .forms import UploadFile
import csv

# Create your views here.
from .utils import get_plot, test_graph, export


def home(request):
    """ Show the all data """
    datas = Plan.objects.all()[:20]

    context = {
        'datas': datas
    }
    return render(request, 'plan/home.html', context)


################# export the plan data #########################

def export_all(request):
    """ Export the all the plan data"""
    plan_resource = PlanResource()
    data_set = plan_resource.export()
    response = HttpResponse(data_set.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="all_Plan.csv"'
    return response


def export_low_high(request):
    """ Export data to customer change from low price to high price """

    datas = Plan.objects.filter(old_plan_price__lt=F('new_plan_price')). \
        values_list('store_code', 'old_plan_name', 'old_plan_speed', 'old_plan_quota', 'old_plan_price',
                    'new_plan_name', 'new_plan_speed', 'new_plan_quota', 'new_plan_price', 'number_of_movements')
    name = 'Low_to_High'
    data = export(datas, name)

    return data


def export_high_low(request):
    """ Export data to customer change from high price to low price """

    datas = Plan.objects.filter(old_plan_price__gt=F('new_plan_price')). \
        values_list('store_code', 'old_plan_name', 'old_plan_speed', 'old_plan_quota', 'old_plan_price',
                    'new_plan_name', 'new_plan_speed', 'new_plan_quota', 'new_plan_price', 'number_of_movements')

    name = 'High To Low'
    data = export(datas, name)

    return data


def export_same_plan(request):
    """ Export data to customer change from high price to low price """
    datas = Plan.objects.filter(old_plan_price=F('new_plan_price')). \
        values_list('store_code', 'old_plan_name', 'old_plan_speed', 'old_plan_quota', 'old_plan_price',
                    'new_plan_name', 'new_plan_speed', 'new_plan_quota', 'new_plan_price', 'number_of_movements')

    name = 'Same Price'
    data = export(datas, name)
    return data


def panda_export(request):
    response = HttpResponse(content_type='text/csv')
    data = Plan.objects.all().values()
    df = pd.DataFrame(data)
    low = df[df['old_plan_price'] > df['new_plan_price']]
    low.to_csv(response, index=False)
    response['Content-Disposition'] = f'attachment;filename="mid.csv"'

    return response


############## Delete ###################
def delete_all(request):
    """ Delete all data in the plan database """
    old = Plan.objects.all()
    old.delete()

    return redirect('plan:home')


def lower_higher(request):
    """ Show Prices and the different between them """
    template = 'plan/lowhigh.html'
    data = Plan.objects.all().aggregate(Sum('number_of_movements')).get('number_of_movements__sum')

    lower = Plan.objects.filter(old_plan_price__lt=F('new_plan_price'))
    lowers = lower.aggregate(Sum('number_of_movements')).get('number_of_movements__sum')

    higher = Plan.objects.filter(new_plan_price__lt=F('old_plan_price'))
    highers = higher.aggregate(Sum('number_of_movements')).get('number_of_movements__sum')

    same_price = Plan.objects.filter(new_plan_price=F('old_plan_price'))
    same_prices = same_price.aggregate(Sum('number_of_movements')).get('number_of_movements__sum')

    lower_per = round((lowers * 100) / data, 2)
    higher_per = round((highers * 100) / data, 2)
    same_per = round((same_prices * 100) / data, 2)

    y = [lower_per, higher_per, same_per]
    x = ['To Higher', 'To Lower', 'Same price']

    chart = get_plot(x, y)

    context = {
        'all_data': data,

        'lowers': lowers,
        'lower_per': lower_per,

        'highers': highers,
        'higher_per': higher_per,

        'same_prices': same_prices,
        'same_per': same_per,

        'chart': chart,

    }

    return render(request, template, context)


def same_plan(request):
    """ Show The Customers That Stay In The Same Plan """
    template = 'plan/same_plan.html'
    data = Plan.objects.all().aggregate(Sum('number_of_movements')).get('number_of_movements__sum')
    all_same = Plan.objects.filter(old_plan_name=F('new_plan_name'))
    as_same = all_same.aggregate(Sum('number_of_movements')).get('number_of_movements__sum')

    super = Plan.objects.filter(Q(old_plan_name__icontains='super'), Q(new_plan_name__icontains='super'))
    supers = super.aggregate(Sum('number_of_movements')).get('number_of_movements__sum')
    super_per = round((supers * 100) / as_same, 2)

    ultra = Plan.objects.filter(Q(old_plan_name__icontains='Ultra'), Q(new_plan_name__icontains='Ultra'))
    ultras = ultra.aggregate(Sum('number_of_movements')).get('number_of_movements__sum')
    ultra_per = round((ultras * 100) / as_same, 2)

    mega = Plan.objects.filter(Q(old_plan_name__icontains='Mega'), Q(new_plan_name__icontains='Mega'))
    megas = mega.aggregate(Sum('number_of_movements')).get('number_of_movements__sum')
    mega_per = round((megas * 100) / as_same, 2)

    context = {
        'data': data,
        'as_same': as_same,

        'supers': supers,
        'super_per': super_per,

        'ultras': ultras,
        'ultra_per': ultra_per,

        'megas': megas,
        'mega_per': mega_per,
    }

    return render(request, template, context)


def change_plan(request):
    """ Show The Customers That Change Plan """
    template = 'plan/change_plan.html'
    all_data = Plan.objects.all().aggregate(Sum('number_of_movements')).get('number_of_movements__sum')

    super_to = Plan.objects.filter(Q(old_plan_name__icontains='super'),
                                   Q(new_plan_name__icontains='mega') | Q(new_plan_name__icontains='ultra'))

    num_super_to = super_to.aggregate(Sum('number_of_movements')).get('number_of_movements__sum')

    per_super_to = round((num_super_to * 100) / all_data, 2)

    to_super = Plan.objects.filter(Q(old_plan_name__icontains='mega') | Q(old_plan_name__icontains='ultra'),
                                   Q(new_plan_name__icontains='super'))
    num_to_super = to_super.aggregate(Sum('number_of_movements')).get('number_of_movements__sum')
    per_to_super = round((num_to_super * 100) / all_data, 2)

    context = {
        'all_data': all_data,

        'num_super_to': num_super_to,
        'per_super_to': per_super_to,

        'num_to_super': num_to_super,
        'per_to_super': per_to_super,
    }

    return render(request, template, context)


def test(request):
    data = Plan.objects.all().values()
    df = pd.DataFrame(data)
    low = df[df['old_plan_price'] > df['new_plan_price']]
    low_nofm = low['number_of_movements'].sum()
    all_nofm = df['number_of_movements'].sum()

    low_per = round((low_nofm * 100) / all_nofm, 2)
    vc = df['old_plan_name'].value_counts()

    z = dict(vc)
    print('#' * 20)
    print(z)

    y = [y for y in z.values()]
    print(y)
    x = [x for x in z.keys()]
    print(x)

    charts = get_plot(x, y)

    secchart = test_graph(x, y)

    expo = df.to_csv('df', index=False)

    context = {
        'all_data': df,
        'df': low.head(10).to_html(),
        'vc': vc,
        'all_nofm': all_nofm,
        'low_nofm': low_nofm,
        'low_per': low_per,
        'charts': charts,
        'secchart': secchart,
        'expo': expo,
        # 'des':df.describe().to_html(),

    }

    return render(request, 'plan/test.html', context)


################# Upload Data ######################
def upload_csv(request):
    """ Upload The Whole Data """
    template = 'plan/upload_csv.html'
    if request.method == 'GET':
        return render(request, template)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'Have to be csv file')
    else:
        df = pd.read_csv(csv_file)
        for row in df.values:
            create = Plan.objects.create(
                change_date=row[0],
                store_code=row[1],
                old_plan_name=row[2],
                old_plan_speed=row[3],
                old_plan_quota=row[4],
                old_plan_price=row[5],
                new_plan_name=row[6],
                new_plan_speed=row[7],
                new_plan_quota=row[8],
                new_plan_price=row[9],
                number_of_movements=row[10],
            )

    context = {}
    return redirect('plan:home')
