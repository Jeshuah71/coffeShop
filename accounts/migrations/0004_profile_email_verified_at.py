from django.conf import settings
from django.db import migrations, models
from django.utils import timezone


def migrate_email_verification_state(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(app_label, model_name)
    Profile = apps.get_model("accounts", "Profile")
    EmailVerificationToken = apps.get_model("accounts", "EmailVerificationToken")

    migration_timestamp = timezone.now()
    token_user_ids = list(
        EmailVerificationToken.objects.values_list("user_id", flat=True)
    )

    User.objects.filter(pk__in=token_user_ids, is_active=False).update(
        is_active=True
    )

    for user_id in User.objects.exclude(pk__in=token_user_ids).values_list(
        "pk", flat=True
    ):
        profile, _ = Profile.objects.get_or_create(user_id=user_id)
        profile.email_verified_at = migration_timestamp
        profile.save(update_fields=["email_verified_at"])


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_merge_20260527_1554"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="email_verified_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RunPython(
            migrate_email_verification_state,
            migrations.RunPython.noop,
        ),
    ]
