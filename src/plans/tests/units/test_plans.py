from datetime import timedelta

import pytest
from faker import Faker

from src.core.exception import DomainError
from src.plans.models import Plan

fake = Faker()


def test_create_plan():
    # given
    start_date = fake.date_this_month()

    plan = Plan(
        name="Test Plan",
        description="Test Description",
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
        name="Test Plan",
        description="Test Description",
        start_date=start_date,
        end_date=start_date - timedelta(days=1),
        fat=20.2,
        protein=20.2,
        carb=20.2,
        kcal=300.0,
    )

    # when / then
    with pytest.raises(DomainError):
        plan.full_clean()


def test_create_plan_with_invalid_macro():
    # given
    start_date = fake.date_this_month()

    plan = Plan(
        name="Test Plan",
        description="Test Description",
        start_date=start_date,
        end_date=start_date + timedelta(days=1),
        fat=0,
        protein=0,
        carb=0,
        kcal=0,
    )

    # when / then
    with pytest.raises(DomainError):
        plan.full_clean()
