"""
Django management command to test admin functionality in production
"""
from django.core.management.base import BaseCommand
from django.contrib.admin.sites import site
from django.contrib import admin


class Command(BaseCommand):
    help = 'Test admin functionality and check for issues'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🔍 Testing admin functionality...')
        )
        
        try:
            # Test 1: Check admin site registration
            registered_count = len(site._registry)
            self.stdout.write(f"✅ Admin models registered: {registered_count}")
            
            # Test 2: Check specific models
            from portfolio.models import Project, Technology, Category
            
            models_to_test = [Project, Technology, Category]
            
            for model in models_to_test:
                if model in site._registry:
                    admin_class = site._registry[model]
                    self.stdout.write(f"✅ {model._meta.model_name}: {admin_class.__class__.__name__}")
                else:
                    self.stdout.write(
                        self.style.ERROR(f"❌ {model._meta.model_name}: NOT registered")
                    )
            
            # Test 3: Check admin URLs
            try:
                from django.urls import reverse
                admin_index_url = reverse('admin:index')
                project_changelist_url = reverse('admin:portfolio_project_changelist')
                self.stdout.write(f"✅ Admin URLs working")
                self.stdout.write(f"   - Index: {admin_index_url}")
                self.stdout.write(f"   - Projects: {project_changelist_url}")
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Admin URLs error: {e}")
                )
            
            # Test 4: Check static files
            from django.conf import settings
            import os
            
            admin_css_path = os.path.join(settings.STATIC_ROOT, 'admin', 'css', 'base.css')
            custom_css_path = os.path.join(settings.STATIC_ROOT, 'admin', 'css', 'custom_admin.css')
            
            if os.path.exists(admin_css_path):
                self.stdout.write("✅ Admin CSS exists")
            else:
                self.stdout.write(self.style.ERROR("❌ Admin CSS missing"))
                
            if os.path.exists(custom_css_path):
                self.stdout.write("✅ Custom admin CSS exists")
            else:
                self.stdout.write(self.style.WARNING("⚠️ Custom admin CSS missing"))
            
            self.stdout.write(
                self.style.SUCCESS('🎉 Admin functionality test completed!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Admin test failed: {e}')
            )
            import traceback
            self.stdout.write(traceback.format_exc())