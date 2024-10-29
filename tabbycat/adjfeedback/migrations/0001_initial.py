# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-10 09:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdjudicatorFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
                ('version', models.PositiveIntegerField(verbose_name='version')),
                ('submitter_type', models.CharField(choices=[('T', 'Tab room'), ('P', 'Public')], max_length=1, verbose_name='submitter type')),
                ('confirmed', models.BooleanField(default=False, verbose_name='confirmed')),
                ('confirm_timestamp', models.DateTimeField(blank=True, null=True, verbose_name='confirm timestamp')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP address')),
                ('score', models.FloatField(verbose_name='score')),
            ],
            options={
                'verbose_name': 'adjudicator feedback',
                'verbose_name_plural': 'adjudicator feedbacks',
            },
        ),
        migrations.CreateModel(
            name='AdjudicatorFeedbackBooleanAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.BooleanField(verbose_name='answer')),
            ],
            options={
                'verbose_name': 'adjudicator feedback boolean answer',
                'verbose_name_plural': 'adjudicator feedback boolean answers',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdjudicatorFeedbackFloatAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.FloatField(verbose_name='answer')),
            ],
            options={
                'verbose_name': 'adjudicator feedback float answer',
                'verbose_name_plural': 'adjudicator feedback float answers',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdjudicatorFeedbackIntegerAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.IntegerField(verbose_name='answer')),
            ],
            options={
                'verbose_name': 'adjudicator feedback integer answer',
                'verbose_name_plural': 'adjudicator feedback integer answers',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdjudicatorFeedbackQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seq', models.IntegerField(help_text='The order in which questions are displayed', verbose_name='sequence number')),
                ('text', models.CharField(help_text='The question displayed to participants, e.g., "Did you agree with the decision?"', max_length=255, verbose_name='text')),
                ('name', models.CharField(help_text='A short name for the question, e.g., "Agree with decision"', max_length=30, verbose_name='name')),
                ('reference', models.SlugField(help_text='Code-compatible reference, e.g., "agree_with_decision"', verbose_name='reference')),
                ('from_adj', models.BooleanField(help_text='Adjudicators should be asked this question (about other adjudicators)', verbose_name='from adjudicator')),
                ('from_team', models.BooleanField(help_text='Teams should be asked this question', verbose_name='from team')),
                ('answer_type', models.CharField(choices=[('bc', 'checkbox'), ('bs', 'yes/no (dropdown)'), ('i', 'integer (textbox)'), ('is', 'integer scale'), ('f', 'float'), ('t', 'text'), ('tl', 'long text'), ('ss', 'select one'), ('ms', 'select multiple')], max_length=2, verbose_name='answer type')),
                ('required', models.BooleanField(default=True, help_text='Whether participants are required to fill out this field', verbose_name='required')),
                ('min_value', models.FloatField(blank=True, help_text='Minimum allowed value for numeric fields (ignored for text or boolean fields)', null=True, verbose_name='minimum value')),
                ('max_value', models.FloatField(blank=True, help_text='Maximum allowed value for numeric fields (ignored for text or boolean fields)', null=True, verbose_name='maximum value')),
                ('choices', models.CharField(blank=True, help_text="Permissible choices for select one/multiple fields, separated by '//' (ignored for other fields)", max_length=500, verbose_name='choices')),
            ],
            options={
                'verbose_name': 'adjudicator feedback question',
                'verbose_name_plural': 'adjudicator feedback questions',
            },
        ),
        migrations.CreateModel(
            name='AdjudicatorFeedbackStringAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(verbose_name='answer')),
            ],
            options={
                'verbose_name': 'adjudicator feedback string answer',
                'verbose_name_plural': 'adjudicator feedback string answers',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdjudicatorTestScoreHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(verbose_name='score')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
            ],
            options={
                'verbose_name': 'adjudicator test score history',
                'verbose_name_plural': 'adjudicator test score histories',
            },
        ),
    ]
