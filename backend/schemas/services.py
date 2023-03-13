import csv
import os

from faker import Faker

from base.settings import MEDIA_ROOT


def generate_csv(records_number, get_schema_path, column_separator,
                 string_character, fieldnames, fieldtypes):
    faker = Faker()
    with open(get_schema_path, "w", newline='') as schema_file:
        schema_writer = csv.writer(
            schema_file,
            delimiter=column_separator,
            quotechar=string_character
        )
        schema_writer.writerow(fieldnames)
        for _ in range(records_number):
            row = get_row(faker, fieldtypes)
            schema_writer.writerow(row)


def get_row(faker, fieldtypes):
    funcs = {
        '1': faker.name,
        '2': faker.email,
        '3': faker.phone_number,
        '4': faker.address,
        '5': faker.date
    }
    row = [escape(funcs[fieldtype]()) for fieldtype in fieldtypes]
    return row


def escape(string):
    return string.replace('\n', '\\n')


def get_schema_path(username, schema_name):
    parent_path = os.path.join(MEDIA_ROOT, username)
    if not os.path.isdir(parent_path):
        os.makedirs(parent_path)
    return os.path.join(parent_path, f"{schema_name}.csv")


def get_fieldnames(schema):
    columns = schema.columns.values('name', 'type', 'order')
    sorted_columns = sorted(columns, key=lambda col: col['order'])
    return [column['name'] for column in sorted_columns]


def get_fieldtypes(schema):
    columns = schema.columns.values('name', 'type', 'order')
    sorted_columns = sorted(columns, key=lambda col: col['order'])
    return [column['type'] for column in sorted_columns]
