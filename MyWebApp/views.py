# MyWebApp/views.py
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import UserData
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


def user_data_form(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user_data = form.save(commit=False)
            
            # Custom Name
            custom_numbers_filename = 'numbers.csv'
            custom_image_filename = 'image.jpg'
            custom_video_filename = 'video.mp4'
            custom_document_filename = 'document.pdf'
            custom_message_filename = 'message.txt'

            # Save files to desktop
            desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')

            numbers_path = os.path.join(desktop_path, 'uploads', 'csv', custom_numbers_filename)
            image_path = os.path.join(desktop_path, 'uploads', 'images', custom_image_filename)
            video_path = os.path.join(desktop_path, 'uploads', 'videos', custom_video_filename)
            document_path = os.path.join(desktop_path, 'uploads', 'documents', custom_document_filename)
            message_path = os.path.join(desktop_path, 'uploads', 'message', custom_message_filename)


            os.makedirs(os.path.dirname(numbers_path), exist_ok=True)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            os.makedirs(os.path.dirname(video_path), exist_ok=True)
            os.makedirs(os.path.dirname(document_path), exist_ok=True)
            os.makedirs(os.path.dirname(message_path), exist_ok=True)
            

            with open(message_path, 'w') as file:
                file.write(user_data.message)
            

            with open(numbers_path, 'wb') as f:
                for chunk in user_data.numbers_file.chunks():
                    f.write(chunk)

            with open(image_path, 'wb') as f:
                for chunk in user_data.image.chunks():
                    f.write(chunk)

            with open(video_path, 'wb') as f:
                for chunk in user_data.video.chunks():
                    f.write(chunk)

            with open(document_path, 'wb') as f:
                for chunk in user_data.document.chunks():
                    f.write(chunk)
                    

            return redirect('success')
    else:
        form = UserForm()

    return render(request, 'user_data_form.html', {'form': form})

def success(request):
    
    loginTime = 40
    newMsgTime = 20
    sendMsgTime = 10
    actionTime = 5
    country_code = 91                # Set your country code

    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    custom_numbers_filename = 'numbers.csv'
    custom_image_filename = 'image.jpg'
    custom_video_filename = 'video.mp4'
    custom_document_filename = 'document.pdf'
    custom_message_filename = 'message.txt'

    # Absolute path to your numbers.csv
    numbers_path = os.path.join(desktop_path, 'uploads', 'csv', custom_numbers_filename)
    
    # Absolute path to your image
    image_path = os.path.join(desktop_path, 'uploads', 'images', custom_image_filename)

    # Absolute path to your video
    video_path = os.path.join(desktop_path, 'uploads', 'videos', custom_video_filename)

    # Absolute path to your document
    document_path = os.path.join(desktop_path, 'uploads', 'documents', custom_document_filename)
    
    # Absolute path to your message
    message_path = os.path.join(desktop_path, 'uploads', 'message', custom_message_filename)

    # Create driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    # Encode Message Text
    with open(message_path, 'r') as file1:
        imgMsg = file1.read()

    # Open browser with default link
    link = 'https://web.whatsapp.com'
    driver.get(link)
    time.sleep(loginTime)

    # Loop Through Numbers List
    with open(numbers_path, 'r') as file:
        for n in file.readlines():
            try:
                num = n.rstrip()
                link = f'https://web.whatsapp.com/send/?phone={country_code}{num}'
                driver.get(link)
                time.sleep(newMsgTime)
                
                if(image_path):
                    driver.find_element(By.CSS_SELECTOR, '._1OT67').click()
                    time.sleep(actionTime)
                    # Find and send image path to input
                    driver.find_elements(By.CSS_SELECTOR, '._2UNQo input')[1].send_keys(image_path)
                    time.sleep(actionTime)
                
                # Start the action chain to write the message
                actions = ActionChains(driver)
                    
                actions.send_keys(Keys.ENTER)
                actions.perform()
                time.sleep(sendMsgTime)
                
                # Click on button to load the input DOM
                if(video_path):
                    driver.find_element(By.CSS_SELECTOR, '._1OT67').click()
                    time.sleep(actionTime)
                    # Find and send image path to input
                    driver.find_elements(By.CSS_SELECTOR, '._2UNQo input')[1].send_keys(video_path)
                    time.sleep(actionTime)
                
                # Start the action chain to write the message
                actions = ActionChains(driver)
                    
                actions.send_keys(Keys.ENTER)
                actions.perform()
                time.sleep(sendMsgTime)
                
                if(document_path):
                    driver.find_element(By.CSS_SELECTOR, '._1OT67').click()
                    time.sleep(actionTime)
                    # Find and send image path to input
                    driver.find_elements(By.CSS_SELECTOR, '._2UNQo input')[0].send_keys(document_path)
                    time.sleep(actionTime)
                
                # Start the action chain to write the message
                actions = ActionChains(driver)     
                actions.send_keys(Keys.ENTER)
                actions.perform()
                time.sleep(sendMsgTime)
                
                actions = ActionChains(driver)
                for line in imgMsg.split('\n'):
                    actions.send_keys(line)
                    # SHIFT + ENTER to create next line
                    actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)
                    
                actions.send_keys(Keys.ENTER)
                actions.perform()
                time.sleep(sendMsgTime)
                
                
            except Exception as e:
                print(f"Error sending message to {num}: {str(e)}")

    # Quit the driver
    driver.quit()


    
    return render(request, 'success.html')
