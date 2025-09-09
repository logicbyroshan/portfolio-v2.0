from django.core.management.base import BaseCommand
from portfolio.models import Skill

class Command(BaseCommand):
    help = 'Populate skill categories based on skill titles'

    def handle(self, *args, **options):
        # Define category mappings based on common skill titles
        category_mappings = {
            'FRONTEND': [
                'react', 'vue', 'angular', 'javascript', 'typescript', 'html', 'css', 
                'sass', 'scss', 'bootstrap', 'tailwind', 'frontend', 'web design',
                'ui', 'ux', 'figma', 'photoshop', 'illustrator', 'sketch'
            ],
            'BACKEND': [
                'python', 'django', 'flask', 'fastapi', 'node', 'express', 'php', 
                'laravel', 'java', 'spring', 'c#', 'asp.net', 'ruby', 'rails',
                'go', 'rust', 'api', 'rest', 'graphql', 'backend'
            ],
            'DATABASE': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'database',
                'sql', 'nosql', 'elasticsearch', 'oracle', 'sqlserver'
            ],
            'DEVOPS': [
                'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins', 'gitlab ci',
                'github actions', 'terraform', 'ansible', 'nginx', 'apache', 'linux',
                'ubuntu', 'centos', 'devops', 'deployment', 'ci/cd'
            ],
            'MOBILE': [
                'react native', 'flutter', 'swift', 'kotlin', 'android', 'ios',
                'mobile', 'app development', 'xamarin'
            ],
            'AI_ML': [
                'machine learning', 'artificial intelligence', 'tensorflow', 'pytorch',
                'scikit-learn', 'pandas', 'numpy', 'ai', 'ml', 'deep learning',
                'neural networks', 'nlp', 'computer vision', 'data science'
            ],
            'DESIGN': [
                'design', 'ui/ux', 'figma', 'sketch', 'photoshop', 'illustrator',
                'adobe', 'canva', 'graphic design', 'web design', 'prototyping'
            ],
            'TOOLS': [
                'git', 'github', 'gitlab', 'vscode', 'vim', 'jetbrains', 'postman',
                'insomnia', 'tools', 'development tools', 'ide', 'editor'
            ],
            'TESTING': [
                'testing', 'pytest', 'jest', 'selenium', 'cypress', 'unit testing',
                'integration testing', 'test automation', 'qa'
            ]
        }

        skills_updated = 0
        
        for skill in Skill.objects.all():
            if skill.category == 'OTHER':  # Only update skills that haven't been categorized
                skill_title_lower = skill.title.lower()
                
                # Find the best category match
                best_category = 'OTHER'
                for category, keywords in category_mappings.items():
                    for keyword in keywords:
                        if keyword in skill_title_lower:
                            best_category = category
                            break
                    if best_category != 'OTHER':
                        break
                
                # Update the skill category
                if best_category != 'OTHER':
                    skill.category = best_category
                    skill.save()
                    skills_updated += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Updated "{skill.title}" to category: {best_category}')
                    )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {skills_updated} skills with categories.')
        )
