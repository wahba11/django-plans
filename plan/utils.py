import csv

import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django.db.models import F, Q
from django.http import HttpResponse
from .models import Plan


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_plot(x, y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 3))
    plt.title('Test Graph')
    plt.barh(x, y)
    plt.xticks(rotation=45)
    plt.xlabel('x lable')
    plt.ylabel('y lable')
    plt.style.use('Solarize_Light2')
    plt.tight_layout()
    graph = get_graph()
    return graph


def test_graph(x, y):
    fig = plt.figure()
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    axes.set_xlabel('my x')
    axes.set_ylabel('my y')
    axes.set_title('my title')
    graph = get_graph()
    return graph


def export(datas,name):
    """ Export data to customer change from low price to high price """
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['store_code', 'old_plan_name', 'old_plan_speed', 'old_plan_quota',
                     'old_plan_price', 'new_plan_name', 'new_plan_speed', 'new_plan_quota', 'new_plan_price',
                     'number_of_movements'])

    datas = datas

    for data in datas:
        writer.writerow(data)

    response['Content-Disposition'] = f'attachment;filename="{name}.csv"'

    return response


