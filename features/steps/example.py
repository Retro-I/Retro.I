from behave import Then, When
from behave.runner import Context


@When("Blupp")
def blupp(context: Context):
    assert 1 == 1


@Then("Blopp")
def blopp(context: Context):
    assert 1 == 1
