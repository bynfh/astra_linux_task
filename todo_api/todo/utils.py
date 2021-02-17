import csv

from django.http import HttpResponse
from .models import Todo


def export_to_csv(queryset, fields, titles, file_name):
    """
    will export the model data in the form of csv file
    :param queryset: queryset that need to be exported as csv
    :param fields: fields of a model that will be included in csv
    :param titles: title for each cell of the csv record
    :param file_name: the exported csv file name
    :return:
    """
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force download
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(file_name)
    # the csv writer
    writer = csv.writer(response)
    if fields:
        headers = fields
        if titles:
            titles = titles
        else:
            titles = headers
    else:
        headers = []
        for field in model._meta.fields:
            headers.append(field.name)
        titles = headers

    # Writes the title for the file
    writer.writerow(titles)

    # write data rows
    for item in queryset:
        writer.writerow([getattr(item, field) for field in headers])
    return response


def ImportToDbFromCsv(FilePath, Todo):
    FirstLine = True
    with open(FilePath, "r") as file:
        file_reader = csv.reader(file, delimiter=",")
        for line in file_reader:
            if FirstLine:
                FirstLine = False
                continue
            Todo.task = line[0]
            Todo.finish_date = line[4]
            Todo.save()