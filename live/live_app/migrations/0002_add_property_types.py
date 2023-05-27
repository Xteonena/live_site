from django.db import migrations


def create_property_types(apps, schema_editor):
    PropertyType = apps.get_model('live_app', 'PropertyType')
    property_types = [
        'Квартира',
        'Дом',
        'Земельный участок',
        'Коммерческая недвижимость',
        'Отель',
        'Хостел'
    ]

    for property_type in property_types:
        PropertyType.objects.create(name=property_type)


class Migration(migrations.Migration):

    dependencies = [
        ('live_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_property_types),
    ]
