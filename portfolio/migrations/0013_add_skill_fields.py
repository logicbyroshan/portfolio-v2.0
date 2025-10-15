# Generated manually to handle M2M field transition
from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0012_delete_aboutmeconfiguration_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="skill",
            options={"ordering": ["order", "title"]},
        ),
        migrations.AddField(
            model_name="skill",
            name="is_featured",
            field=models.BooleanField(
                default=False,
                help_text="Display this skill prominently on the home page",
            ),
        ),
        migrations.AddField(
            model_name="skill",
            name="learning_journey",
            field=tinymce.models.HTMLField(
                blank=True,
                help_text="Detailed learning journey and experience with this skill",
            ),
        ),
        migrations.AddField(
            model_name="skill",
            name="proficiency_level",
            field=models.CharField(
                choices=[
                    ("beginner", "Beginner"),
                    ("intermediate", "Intermediate"),
                    ("advanced", "Advanced"),
                    ("expert", "Expert"),
                ],
                default="intermediate",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="skill",
            name="years_of_experience",
            field=models.PositiveIntegerField(
                default=1, help_text="Years of experience with this skill"
            ),
        ),
    ]
