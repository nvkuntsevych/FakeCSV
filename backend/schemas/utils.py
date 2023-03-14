"""
Module containing utility functions for generating
and working with CSV datasets.
"""

__all__ = ['generate_csv', 'get_row', 'escape',
           'get_dataset_path', 'get_fieldnames',
           'get_fieldtypes']

import csv
import os

from faker import Faker

from base.settings import MEDIA_ROOT


def generate_csv(records_number, dataset_path, column_separator,
                 string_character, fieldnames, fieldtypes):
    """Generate csv file and save it to the given path."""
    faker = Faker()
    with open(dataset_path, "w", newline='') as dataset_file:
        dataset_writer = csv.writer(
            dataset_file,
            delimiter=column_separator,
            quotechar=string_character
        )
        dataset_writer.writerow(fieldnames)
        for _ in range(records_number):
            row = get_row(faker, fieldtypes)
            dataset_writer.writerow(row)


def get_row(faker, fieldtypes):
    """Return list with fake data.

    The returned list is formed by the
    given list with column types.
    """
    funcs = {
        '1': faker.name,
        '2': faker.email,
        '3': faker.phone_number,
        '4': faker.address,
        '5': faker.date
    }
    return [escape(funcs[fieldtype]()) for fieldtype in fieldtypes]


def escape(string):
    """Escape '\n' symbols."""
    return string.replace('\n', '\\n')


def get_dataset_path(username, schema_name, dataset_number):
    """Return path to the dataset.

    The path is formed according to the following pattern:
    <MEDIA_ROOT>/<username>/<schema_name>_<datasetN>.csv
    N - sequence number of dataset.
    For example:
    /usr/src/backend/media/admin/schema1_dataset41.csv
    """
    parent_path = os.path.join(MEDIA_ROOT, username)
    if not os.path.isdir(parent_path):
        os.makedirs(parent_path)
    return os.path.join(parent_path, f"{schema_name}_dataset{dataset_number}.csv")


def get_fieldnames(schema):
    """Return list with column names of given schema.

    The returned names is sorted by 'order' column.
    """
    columns = schema.columns.values('name', 'order')
    sorted_columns = sorted(columns, key=lambda col: col['order'])
    return [column['name'] for column in sorted_columns]


def get_fieldtypes(schema):
    """Return list with column types of given schema.

    The returned types is sorted by 'order' column.
    """
    columns = schema.columns.values('type', 'order')
    sorted_columns = sorted(columns, key=lambda col: col['order'])
    return [column['type'] for column in sorted_columns]
