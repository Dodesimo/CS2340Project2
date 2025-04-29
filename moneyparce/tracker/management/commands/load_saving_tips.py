from django.core.management.base import BaseCommand
from tracker.models import SavingTip

class Command(BaseCommand):
    help = 'Loads initial saving tips into the database'

    def handle(self, *args, **kwargs):
        tips = [
            {
                'tip': 'Bring your own lunch to work instead of eating out. This can save you $10-15 per day.',
                'category': 'Food',
                'difficulty': 'easy',
                'potential_savings': '$50-75 per week'
            },
            {
                'tip': 'Use public transportation or carpool instead of driving alone. This reduces fuel and parking costs.',
                'category': 'Transportation',
                'difficulty': 'medium',
                'potential_savings': '$20-40 per week'
            },
            {
                'tip': 'Cancel unused subscriptions and memberships. Many people pay for services they rarely use.',
                'category': 'Subscriptions',
                'difficulty': 'easy',
                'potential_savings': '$10-50 per month'
            },
            {
                'tip': 'Plan your meals for the week and buy groceries in bulk. This reduces impulse purchases and food waste.',
                'category': 'Food',
                'difficulty': 'medium',
                'potential_savings': '$30-50 per week'
            },
            {
                'tip': 'Use energy-efficient appliances and turn off lights when not in use. Small changes can add up.',
                'category': 'Utilities',
                'difficulty': 'easy',
                'potential_savings': '$10-20 per month'
            },
            {
                'tip': 'Wait 24 hours before making non-essential purchases. This helps avoid impulse buying.',
                'category': 'Shopping',
                'difficulty': 'medium',
                'potential_savings': 'Varies, but can prevent unnecessary spending'
            },
            {
                'tip': 'Use cashback apps and credit cards with rewards for your regular purchases.',
                'category': 'Shopping',
                'difficulty': 'easy',
                'potential_savings': '2-5% on purchases'
            },
            {
                'tip': 'Make coffee at home instead of buying it daily. A $5 coffee habit costs $1,825 per year.',
                'category': 'Food',
                'difficulty': 'easy',
                'potential_savings': '$25-35 per week'
            },
            {
                'tip': 'Shop with a list and stick to it. This helps avoid unnecessary purchases.',
                'category': 'Shopping',
                'difficulty': 'easy',
                'potential_savings': '$20-50 per shopping trip'
            },
            {
                'tip': 'Use the library instead of buying books and movies. Many libraries also offer digital content.',
                'category': 'Entertainment',
                'difficulty': 'easy',
                'potential_savings': '$20-50 per month'
            }
        ]

        for tip_data in tips:
            SavingTip.objects.get_or_create(
                tip=tip_data['tip'],
                category=tip_data['category'],
                difficulty=tip_data['difficulty'],
                potential_savings=tip_data['potential_savings']
            )

        self.stdout.write(self.style.SUCCESS('Successfully loaded saving tips')) 