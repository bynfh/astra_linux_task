import csv

from .models import Todo


def export_to_csv(file_name, response):
    """
    Export the model data in the form of csv file
    :param response:
    :param file_name: the exported csv file name

    """
    if '.csv' not in file_name:
        file_name += '.csv'
        response['Content-Disposition'] = f'attachment; filename={file_name}'

    queryset = Todo.objects.only('task', 'timestamp', 'completed', 'updated', 'finish_date', 'user')
    fields = ['task', 'timestamp', 'completed', 'updated', 'finish_date', 'user']
    writer = csv.writer(response)
    writer.writerow(fields)
    for item in queryset:
        writer.writerow([getattr(item, field) for field in fields])

    return response


def import_to_db_from_csv(file_path):
    with open(file_path, "r") as file:
        file_reader = csv.DictReader(file, delimiter=",")
        for line_dict in file_reader:
            todo = Todo()
            todo.task = line_dict.get('task')
            todo.finish_date = line_dict.get('finish_date')
            todo.timestamp = line_dict.get('timestamp')
            todo.completed = line_dict.get('completed')
            todo.updated = line_dict.get('updated')
            todo.save()


#{"file_name":"/home/oleg/Загрузки/test.csv"}