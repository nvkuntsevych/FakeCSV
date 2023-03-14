from schemas.models import DataSet
from schemas.utils import generate_csv


def task(records_number, schema_path, column_separator,
         string_character, fieldnames, fieldtypes, dataset_id):
    generate_csv(records_number, schema_path, column_separator,
                 string_character, fieldnames, fieldtypes)

    dataset = DataSet.objects.get(pk=dataset_id)
    dataset.status = "Ready"
    dataset.save()
