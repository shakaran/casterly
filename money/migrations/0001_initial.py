# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BankAccount'
        db.create_table('money_bankaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bank_accounts', to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_digits', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('entity', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('initial_balance', self.gf('money.fields.CurrencyField')(default=0.0, max_digits=7, decimal_places=2)),
            ('current_balance', self.gf('money.fields.CurrencyField')(default=0.0, max_digits=7, decimal_places=2)),
        ))
        db.send_create_signal('money', ['BankAccount'])

        # Adding model 'MovementCategory'
        db.create_table('money_movementcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('money', ['MovementCategory'])

        # Adding model 'Movement'
        db.create_table('money_movement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='movements', to=orm['money.BankAccount'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='movements', null=True, to=orm['money.MovementCategory'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('amount', self.gf('money.fields.CurrencyField')(max_digits=7, decimal_places=2)),
            ('current_balance', self.gf('money.fields.CurrencyField')(null=True, max_digits=7, decimal_places=2, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('money', ['Movement'])

        # Adding model 'CategorySuggestion'
        db.create_table('money_categorysuggestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('expression', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['money.MovementCategory'])),
        ))
        db.send_create_signal('money', ['CategorySuggestion'])


    def backwards(self, orm):
        # Deleting model 'BankAccount'
        db.delete_table('money_bankaccount')

        # Deleting model 'MovementCategory'
        db.delete_table('money_movementcategory')

        # Deleting model 'Movement'
        db.delete_table('money_movement')

        # Deleting model 'CategorySuggestion'
        db.delete_table('money_categorysuggestion')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'money.bankaccount': {
            'Meta': {'object_name': 'BankAccount'},
            'current_balance': ('money.fields.CurrencyField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '2'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'entity': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_balance': ('money.fields.CurrencyField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '2'}),
            'last_digits': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bank_accounts'", 'to': "orm['auth.User']"})
        },
        'money.categorysuggestion': {
            'Meta': {'object_name': 'CategorySuggestion'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['money.MovementCategory']"}),
            'expression': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'money.movement': {
            'Meta': {'object_name': 'Movement'},
            'amount': ('money.fields.CurrencyField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'movements'", 'to': "orm['money.BankAccount']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'movements'", 'null': 'True', 'to': "orm['money.MovementCategory']"}),
            'current_balance': ('money.fields.CurrencyField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'money.movementcategory': {
            'Meta': {'object_name': 'MovementCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['money']