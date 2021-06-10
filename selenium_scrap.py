from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.common import exceptions
import itertools
import random

SHORT_WAIT = 0.1
MEDIUM_WAIT = 3
LONG_WAIT = 100
PATH = "C:\\Users\Kamil\\Downloads\\chromedriver\\chromedriver.exe"
truegamedata_url = "https://www.truegamedata.com/weapon_builder"
driver = webdriver.Chrome(PATH)
all_data = pd.DataFrame(
    columns=['Gun', 'Muzzle', 'Barrel', 'Laser', 'Optic', 'Stock', 'Underbarrel', 'Ammunition', 'Perk', 'Fire Rate', 'Range', 'ADS', 'Sprint to Fire Time', 'Tactical Sprint to Fire Time', 'Movement',
             'ADS Movement', 'Vertical Recoil', 'Horizontal Bounce', 'Hipfire Area', 'Reload Time', 'Bullet Velocity', 'Mag Size'])
driver.get(truegamedata_url)
prev_button = driver.find_element_by_id('simplePreviousButton')
next_button = driver.find_element_by_id('simpleNextButton')

guntype_radio = driver.find_elements(by=By.CLASS_NAME, value='radio-item')
dropdown = driver.find_element_by_id('simpleGun')
iteration = 0
time.sleep(MEDIUM_WAIT)
gun_global = "None"


def get_random_time(n):
    return random.random() * n


def scrap_to_csv():
    global iteration
    global status_dictionary

    for key, value in status_dictionary.items():
        all_data.at[iteration, key] = value

    stats_container = driver.find_elements_by_class_name('summary-side-container')[1].find_element(by=By.CLASS_NAME,
                                                                                                   value='base-stats-container')
    metrics = stats_container.find_elements(by=By.TAG_NAME, value="h4")
    values = stats_container.find_elements(by=By.TAG_NAME, value="p")

    for m, v in zip(metrics, values):
        all_data.at[iteration, str(m.text).replace(":", "")] = v.text
        # print(f"The value for metric {m.text} is {v.text}")

    iteration += 1
    all_data.to_csv('dataout_' + gun_global + '.csv')


for gun_type in guntype_radio:
    gun_type.click()
    print('-Gun Type: ', str(gun_type.text))
    time.sleep(get_random_time(MEDIUM_WAIT))
    dropdown.click()
    time.sleep(get_random_time(MEDIUM_WAIT))
    guns = driver.find_elements(by=By.CLASS_NAME, value='dropdown-list-item')
    attch_list = ['Gun', 'Muzzle', 'Barrel', 'Laser', 'Optic', 'Stock', 'Underbarrel', 'Ammunition', 'Perk']
    status_dictionary = {a: "None" for a in attch_list}
    for g in range(len(guns)):
        guns = driver.find_elements(by=By.CLASS_NAME, value='dropdown-list-item')
        gun_type.click()
        time.sleep(get_random_time(MEDIUM_WAIT))
        dropdown.click()
        time.sleep(get_random_time(MEDIUM_WAIT))
        # try:
        guns[g].click()
        print('--Gun: ', str(guns[g].text))
        gun_global = str(guns[g].text)
        all_data = pd.DataFrame(
            columns=['Gun', 'Muzzle', 'Barrel', 'Laser', 'Optic', 'Stock', 'Underbarrel', 'Ammunition', 'Perk', 'Fire Rate', 'Range', 'ADS', 'Sprint to Fire Time', 'Tactical Sprint to Fire Time',
                     'Movement',
                     'ADS Movement', 'Vertical Recoil', 'Horizontal Bounce', 'Hipfire Area', 'Reload Time', 'Bullet Velocity', 'Mag Size'])
        # all_data.at[iteration, 'Gun'] = str(guns[g].text)
        # except exceptions.StaleElementReferenceException as e:
        #     print(e)
        #     pass

        time.sleep(get_random_time(MEDIUM_WAIT))
        next_button.click()
        time.sleep(get_random_time(MEDIUM_WAIT))

        # change attachments simpleAttachmentSelection
        attachment_menu = driver.find_element(by=By.ID, value='simpleAttachmentSelection')
        all_attachments = attachment_menu.find_elements(by=By.CLASS_NAME, value='dropdown-item')

        print('---Attachments available: ', [str(a.text).split(" ")[0] for a in all_attachments])

        # list_of_tuples = list(itertools.combinations(all_attachments, 5))
        possible_selections = [i for i in itertools.combinations(all_attachments, 5)]
        for selection in possible_selections:
            time.sleep(get_random_time(MEDIUM_WAIT))
            print('---Selected combination: ', [str(a.text).split(" ")[0] for a in selection])
            for attachment in selection:
                attachment_name = str(attachment.find_element(By.TAG_NAME, value='h4').text).split(" ")[0]
                print('----Fixed attachment: ', attachment_name)
                att_dropdown_button = attachment.find_element(By.TAG_NAME, value='p')
                att_dropdown_button.click()
                time.sleep(get_random_time(SHORT_WAIT))
                att_options = attachment.find_element(By.TAG_NAME, value='ul').find_elements(By.TAG_NAME, value='li')
                for option in att_options:
                    fixed_attachment = str(option.text)
                    x_buttons = attachment_menu.find_elements(by=By.TAG_NAME, value='button')
                    for X in x_buttons:  # reset all option selections
                        X.click()
                        time.sleep(get_random_time(SHORT_WAIT))

                    status_dictionary = {a: "None" for a in attch_list}
                    status_dictionary['Gun'] = gun_global

                    # all_data.at[iteration, attachment_name] = str(option.text)

                    att_dropdown_button.click()
                    print('----Current option: ', str(option.text))
                    time.sleep(get_random_time(SHORT_WAIT))
                    try:
                        option.click()
                    except exceptions.ElementNotInteractableException as e:
                        print(e)
                        time.sleep(get_random_time(SHORT_WAIT))
                        break

                    all_other_attachments = [a for a in selection if a != attachment]
                    for other_attachment in all_other_attachments:
                        other_attachment_name = str(other_attachment.find_element(By.TAG_NAME, value='h4').text).split(" ")[0]
                        print('-----Changing attachment: ', other_attachment_name)
                        other_att_dropdown_button = other_attachment.find_element(By.TAG_NAME, value='p')
                        try:
                            other_att_dropdown_button.click()
                        except exceptions.ElementNotInteractableException as e:
                            print(e)
                            pass

                        time.sleep(get_random_time(SHORT_WAIT))
                        other_att_options = other_attachment.find_element(By.TAG_NAME, value='ul').find_elements(By.TAG_NAME, value='li')
                        for other_option in other_att_options:
                            # all_data.at[iteration, other_attachment_name] = str(other_option.text)
                            status_dictionary[other_attachment_name] = str(other_option.text)
                            status_dictionary[attachment_name] = str(fixed_attachment)

                            print('------Current option: ', str(other_option.text))
                            try:
                                other_option.click()
                            except exceptions.ElementNotInteractableException as e:
                                print(e)
                                other_att_dropdown_button.click()
                                time.sleep(get_random_time(SHORT_WAIT))
                                break

                            time.sleep(get_random_time(SHORT_WAIT))
                            scrap_to_csv()
                            time.sleep(get_random_time(SHORT_WAIT))
                            other_att_dropdown_button.click()
                            time.sleep(get_random_time(SHORT_WAIT))

                    att_dropdown_button = attachment.find_element(By.TAG_NAME, value='p')
                    att_dropdown_button.click()
                    time.sleep(get_random_time(SHORT_WAIT))

        prev_button.click()
        time.sleep(get_random_time(LONG_WAIT))
