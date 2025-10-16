"""
Django management command to test admin functionality and check for conflicts
"""
from django.core.management.base import BaseCommand
from django.contrib.admin.sites import site
from django.apps import apps


class Command(BaseCommand):
    help = 'Test admin functionality and check for registration conflicts'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🔍 Checking admin registrations...')
        )
        
        # Check all registered models
        registered_models = {}
        for model, admin_class in site._registry.items():
            app_label = model._meta.app_label
            model_name = model._meta.model_name
            
            if app_label not in registered_models:
                registered_models[app_label] = []
            
            registered_models[app_label].append({
                'model': model_name,
                'admin_class': admin_class.__class__.__name__
            })
        
        # Display results
        for app_label, models in registered_models.items():
            self.stdout.write(f"\n📱 {app_label.upper()}")
            for model_info in models:
                self.stdout.write(
                    f"  ✅ {model_info['model']} -> {model_info['admin_class']}"
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✨ Found {len(site._registry)} registered models')
        )
        
        # Check for potential conflicts
        conflicts = []
        seen_models = set()
        
        for model in site._registry.keys():
            model_key = f"{model._meta.app_label}.{model._meta.model_name}"
            if model_key in seen_models:
                conflicts.append(model_key)
            seen_models.add(model_key)
        
        if conflicts:
            self.stdout.write(
                self.style.ERROR(f'\n⚠️  Found {len(conflicts)} conflicts:')
            )
            for conflict in conflicts:
                self.stdout.write(f"  ❌ {conflict}")
        else:
            self.stdout.write(
                self.style.SUCCESS('\n🎉 No admin registration conflicts found!')
            )