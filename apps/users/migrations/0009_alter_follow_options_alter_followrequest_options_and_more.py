import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_merge_20260602_2045'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='followrequest',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='following_relationships', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='follow',
            name='following',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='follower_relationships', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='followrequest',
            name='from_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sent_follow_requests', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='followrequest',
            name='to_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='received_follow_requests', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blockuser',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected'), ('CANCELED', 'Canceled')], default='PENDING', max_length=20),
        ),
        migrations.AlterField(
            model_name='followrequest',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='restrictuser',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AddIndex(
            model_name='follow',
            index=models.Index(fields=['follower'], name='users_follo_followe_3a2483_idx'),
        ),
        migrations.AddIndex(
            model_name='follow',
            index=models.Index(fields=['following'], name='users_follo_followi_e01def_idx'),
        ),
        migrations.AddIndex(
            model_name='follow',
            index=models.Index(fields=['status'], name='users_follo_status_2f8c09_idx'),
        ),
        migrations.AddIndex(
            model_name='follow',
            index=models.Index(fields=['created_at'], name='users_follo_created_8655d4_idx'),
        ),
        migrations.AddIndex(
            model_name='followrequest',
            index=models.Index(fields=['from_user'], name='users_follo_from_us_12e928_idx'),
        ),
        migrations.AddIndex(
            model_name='followrequest',
            index=models.Index(fields=['to_user'], name='users_follo_to_user_e0975a_idx'),
        ),
        migrations.AddIndex(
            model_name='followrequest',
            index=models.Index(fields=['created_at'], name='users_follo_created_c6a9a9_idx'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('follower', 'following'), name='unique_follow_relation'),
        ),
        migrations.AddConstraint(
            model_name='followrequest',
            constraint=models.UniqueConstraint(fields=('from_user', 'to_user'), name='unique_follow_request'),
        ),
    ]
