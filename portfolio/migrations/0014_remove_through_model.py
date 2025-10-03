# Generated manually to handle M2M field transition
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0013_add_skill_fields"),
    ]

    operations = [
        # Remove the through relationship by creating a new M2M field
        migrations.RemoveField(
            model_name="skill",
            name="technologies",
        ),
        migrations.AddField(
            model_name="skill",
            name="technologies",
            field=models.ManyToManyField(blank=True, to="portfolio.technology"),
        ),
        # Delete the through model
        migrations.DeleteModel(
            name="SkillTechnologyDetail",
        ),
    ]
