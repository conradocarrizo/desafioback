from django.db import migrations

from app.enums import PayableStatesEnum


def run(apps, schema_editor):
    PayableState = apps.get_model("app", "PayableState")
    loaded_states = list(PayableState.objects.all().values_list("name", flat=True))
    states = []

    for choice in PayableStatesEnum.choices():
        name = choice[1]
        if name not in loaded_states:
            states.append(PayableState(name=name))

    PayableState.objects.bulk_create(states)


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(run),
    ]
