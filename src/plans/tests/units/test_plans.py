from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from faker import Faker

from src.plans.models import Plan

fake = Faker()


def test_create_plan():
    # given
    start_date = fake.date_this_month()

    plan = Plan(
        name='Test Plan',
        description='Test Description',
        start_date=start_date,
        end_date=start_date + timedelta(days=1),
        fat=20.2,
        protein=20.2,
        carb=20.2,
        kcal=300.0,
    )

    # when / then
    plan.full_clean()


def test_create_plan_with_invalid_end_date():
    # given
    start_date = fake.date_this_month()

    plan = Plan(
        name='Test Plan',
        description='Test Description',
        start_date=start_date,
        end_date=start_date - timedelta(days=1),
        fat=20.2,
        protein=20.2,
        carb=20.2,
        kcal=300.0,
    )

    # when / then
    with pytest.raises(ValidationError):
        plan.full_clean()
