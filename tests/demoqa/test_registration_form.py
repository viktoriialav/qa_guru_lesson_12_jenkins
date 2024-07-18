import os
from datetime import date

import allure
from selene import browser, have, command
from selenium.webdriver.common.keys import Keys

import tests


@allure.title('Successful fill form')
def test_demoqa_student_registration_form(setup_browser):
    first_name = 'Viktoriia'
    last_name = 'Lav'
    user_email = 'newuser@gmail.com'
    user_gender = 'Female'
    user_number = '8800222334'
    date_of_birth = date(1993, 5, 17)
    user_subjects = 'Chemistry'
    user_hobbies = 'Sports'
    user_picture='photo.png'
    user_current_address = '144 Broadway, suit 12'
    user_state = 'NCR'
    user_city = 'Gurgaon'


    with allure.step('Open registration form'):
        browser.open('/automation-practice-form')
        browser.element('.practice-form-wrapper').should(have.text("Student Registration Form"))
        # browser.driver.execute_script("$('footer').remove()")
        # browser.driver.execute_script("$('#fixedban').remove()")
        browser.all('[id^=google_ads][id$=container__]').with_(timeout=10).wait_until(
            have.size_greater_than_or_equal(3)
        )
        browser.all('[id^=google_ads][id$=container__]').perform(command.js.remove)

    with allure.step('Fill form'):
        browser.element('#firstName').type(first_name)
        browser.element('#lastName').type(last_name)
        browser.element('#userEmail').type(user_email)
        browser.all('[name=gender]').element_by(have.value(user_gender)).element('..').click()
        browser.element('#userNumber').type(user_number)

        browser.element('#dateOfBirthInput').send_keys(Keys.CONTROL, 'a').type(
            date_of_birth.strftime('%m.%d.%Y')).press_enter()

        browser.element('#subjectsInput').type(user_subjects).click().press_enter()
        browser.all('[for^=hobbies-checkbox]').element_by(have.exact_text(user_hobbies)).click()
        # browser.all('[for^=hobbies-checkbox]').element_by(have.exact_text('Reading')).click()

        browser.element('#currentAddress').set_value(user_current_address)
        browser.element('#state').perform(command.js.scroll_into_view)
        browser.element('#state').click()
        browser.all('[id^=react-select][id*=option]').element_by(have.exact_text(user_state)).click()
        browser.element('#city').click()
        browser.all('[id^=react-select][id*=option]').element_by(have.exact_text(user_city)).click()

        browser.element('#uploadPicture').send_keys(os.path.abspath(
            os.path.join(os.path.dirname(tests.__file__), 'resources/photo.png')
        ))

        browser.element('#submit').click()

    with allure.step('Check form results'):
        browser.element('#example-modal-sizes-title-lg').should(have.text('Thanks for submitting the form'))
        browser.element('.table').all('td').even.should(have.exact_texts(f'{first_name} {last_name}',
                                                                         user_email,
                                                                         user_gender,
                                                                         user_number,
                                                                         date_of_birth.strftime('%d %B,%Y'),
                                                                         user_subjects,
                                                                         user_hobbies,
                                                                         user_picture,
                                                                         user_current_address,
                                                                         f'{user_state} {user_city}'))
