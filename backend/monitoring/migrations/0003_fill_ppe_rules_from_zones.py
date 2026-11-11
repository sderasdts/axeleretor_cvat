"""Data-миграция: переносит Zone.required_ppe в таблицу PPE_Rules.

Zone.required_ppe остаётся (его использует приём детекций), правила
создаются только для известных классов СИЗ и без дублей.
"""
from django.db import migrations

KNOWN_PPE = {"helmet", "gloves", "vest", "goggles", "mask", "boots"}


def forwards(apps, schema_editor):
    Zone = apps.get_model("monitoring", "Zone")
    PPERule = apps.get_model("monitoring", "PPERule")
    rules = []
    for zone in Zone.objects.all().iterator():
        for ppe in dict.fromkeys(zone.required_ppe or []):
            if ppe in KNOWN_PPE:
                rules.append(PPERule(zone_id=zone.id, ppe_class=ppe, is_required=True))
    PPERule.objects.bulk_create(rules, ignore_conflicts=True)


class Migration(migrations.Migration):

    dependencies = [
        ("monitoring", "0002_employees_ppe_rules_frames"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
