# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Alert'
        db.create_table(u'asg_alert', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('message', self.gf('tinymce.models.HTMLField')()),
        ))
        db.send_create_signal(u'asg', ['Alert'])

        # Adding model 'Announcement'
        db.create_table(u'asg_announcement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('link_title_to', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('message', self.gf('tinymce.models.HTMLField')()),
            ('date_posted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'asg', ['Announcement'])

        # Adding model 'Person'
        db.create_table(u'asg_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254, blank=True)),
            ('date_joined', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('photo', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('website_role', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
        ))
        db.send_create_signal(u'asg', ['Person'])

        # Adding M2M table for field positions on 'Person'
        m2m_table_name = db.shorten_name(u'asg_person_positions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'asg.person'], null=False)),
            ('position', models.ForeignKey(orm[u'asg.position'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'position_id'])

        # Adding model 'Position'
        db.create_table(u'asg_position', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('committee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['asg.Committee'], null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('on_exec_board', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('senate_leadership', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'asg', ['Position'])

        # Adding model 'Committee'
        db.create_table(u'asg_committee', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('show_in_list', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'asg', ['Committee'])

        # Adding M2M table for field members on 'Committee'
        m2m_table_name = db.shorten_name(u'asg_committee_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('committee', models.ForeignKey(orm[u'asg.committee'], null=False)),
            ('person', models.ForeignKey(orm[u'asg.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['committee_id', 'person_id'])

        # Adding model 'Project'
        db.create_table(u'asg_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('committee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['asg.Committee'])),
            ('primary_contact', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['asg.Person'])),
        ))
        db.send_create_signal(u'asg', ['Project'])

        # Adding M2M table for field members on 'Project'
        m2m_table_name = db.shorten_name(u'asg_project_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'asg.project'], null=False)),
            ('person', models.ForeignKey(orm[u'asg.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'person_id'])

        # Adding model 'Legislation'
        db.create_table(u'asg_legislation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('status_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'asg', ['Legislation'])

        # Adding model 'NewsLink'
        db.create_table(u'asg_newslink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('date_published', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'asg', ['NewsLink'])

        # Adding model 'GoogleCalendar'
        db.create_table(u'asg_googlecalendar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('xml_feed_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('calendar_id', self.gf('django.db.models.fields.TextField')()),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_office_hours', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('event_color', self.gf('colorfield.fields.ColorField')(max_length=10, blank=True)),
        ))
        db.send_create_signal(u'asg', ['GoogleCalendar'])

        # Adding model 'Event'
        db.create_table(u'asg_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=455, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('calendar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['asg.GoogleCalendar'], null=True, blank=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='office_hours', null=True, to=orm['asg.Person'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['asg.Project'], null=True, blank=True)),
            ('committee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['asg.Committee'], null=True, blank=True)),
        ))
        db.send_create_signal(u'asg', ['Event'])

        # Adding model 'HomepageSlide'
        db.create_table(u'asg_homepageslide', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'asg', ['HomepageSlide'])

        # Adding model 'Page'
        db.create_table(u'asg_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('width', self.gf('django.db.models.fields.CharField')(default='9', max_length=2)),
            ('content', self.gf('tinymce.models.HTMLField')()),
        ))
        db.send_create_signal(u'asg', ['Page'])

        # Adding model 'Resource'
        db.create_table(u'asg_resource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('logo_image', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('users', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'asg', ['Resource'])

        # Adding model 'Upload'
        db.create_table(u'asg_upload', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'asg', ['Upload'])


    def backwards(self, orm):
        # Deleting model 'Alert'
        db.delete_table(u'asg_alert')

        # Deleting model 'Announcement'
        db.delete_table(u'asg_announcement')

        # Deleting model 'Person'
        db.delete_table(u'asg_person')

        # Removing M2M table for field positions on 'Person'
        db.delete_table(db.shorten_name(u'asg_person_positions'))

        # Deleting model 'Position'
        db.delete_table(u'asg_position')

        # Deleting model 'Committee'
        db.delete_table(u'asg_committee')

        # Removing M2M table for field members on 'Committee'
        db.delete_table(db.shorten_name(u'asg_committee_members'))

        # Deleting model 'Project'
        db.delete_table(u'asg_project')

        # Removing M2M table for field members on 'Project'
        db.delete_table(db.shorten_name(u'asg_project_members'))

        # Deleting model 'Legislation'
        db.delete_table(u'asg_legislation')

        # Deleting model 'NewsLink'
        db.delete_table(u'asg_newslink')

        # Deleting model 'GoogleCalendar'
        db.delete_table(u'asg_googlecalendar')

        # Deleting model 'Event'
        db.delete_table(u'asg_event')

        # Deleting model 'HomepageSlide'
        db.delete_table(u'asg_homepageslide')

        # Deleting model 'Page'
        db.delete_table(u'asg_page')

        # Deleting model 'Resource'
        db.delete_table(u'asg_resource')

        # Deleting model 'Upload'
        db.delete_table(u'asg_upload')


    models = {
        u'asg.alert': {
            'Meta': {'object_name': 'Alert'},
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('tinymce.models.HTMLField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'asg.announcement': {
            'Meta': {'object_name': 'Announcement'},
            'date_posted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_title_to': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'message': ('tinymce.models.HTMLField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'asg.committee': {
            'Meta': {'object_name': 'Committee'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['asg.Person']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'show_in_list': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'asg.event': {
            'Meta': {'object_name': 'Event'},
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['asg.GoogleCalendar']", 'null': 'True', 'blank': 'True'}),
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['asg.Committee']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '455', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'office_hours'", 'null': 'True', 'to': u"orm['asg.Person']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['asg.Project']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'asg.googlecalendar': {
            'Meta': {'object_name': 'GoogleCalendar'},
            'calendar_id': ('django.db.models.fields.TextField', [], {}),
            'event_color': ('colorfield.fields.ColorField', [], {'max_length': '10', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_office_hours': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'xml_feed_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'asg.homepageslide': {
            'Meta': {'ordering': "['active', 'order', 'caption']", 'object_name': 'HomepageSlide'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'asg.legislation': {
            'Meta': {'ordering': "['-status_date', '-code']", 'object_name': 'Legislation'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'status_date': ('django.db.models.fields.DateField', [], {'blank': 'True'})
        },
        u'asg.newslink': {
            'Meta': {'ordering': "['-date_published']", 'object_name': 'NewsLink'},
            'date_published': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        u'asg.page': {
            'Meta': {'object_name': 'Page'},
            'content': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'width': ('django.db.models.fields.CharField', [], {'default': "'9'", 'max_length': '2'})
        },
        u'asg.person': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'object_name': 'Person'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'positions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['asg.Position']", 'symmetrical': 'False', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'website_role': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'})
        },
        u'asg.position': {
            'Meta': {'ordering': "['on_exec_board', 'senate_leadership', 'order']", 'object_name': 'Position'},
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['asg.Committee']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'on_exec_board': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'senate_leadership': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'asg.project': {
            'Meta': {'object_name': 'Project'},
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['asg.Committee']"}),
            'description': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['asg.Person']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'primary_contact': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['asg.Person']"})
        },
        u'asg.resource': {
            'Meta': {'object_name': 'Resource'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'logo_image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'users': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'asg.upload': {
            'Meta': {'object_name': 'Upload'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['asg']