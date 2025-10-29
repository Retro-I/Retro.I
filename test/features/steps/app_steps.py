from behave import given, when, then
from playwright.sync_api import sync_playwright

@given("the app is running")
def step_start_app(context):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=False)
    context.page = context.browser.new_page()
    context.page.goto("http://localhost:8550")  # Your Flet web target

@when('I click the "{button_text}" button')
def step_click_button(context, button_text: str):
    context.page.get_by_text(button_text).click()

@then('I should see the counter increase to "1"')
def step_check_counter(context):
    assert context.page.get_by_text("1").is_visible()

def after_scenario(context, scenario):
    context.browser.close()
    context.playwright.stop()