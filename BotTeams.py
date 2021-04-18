import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
from time import sleep
import speech_recognition as sr

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 2,
    "profile.default_content_setting_values.media_stream_camera": 2,
    "profile.default_content_setting_values.geolocation": 2,
    "profile.default_content_setting_values.notifications": 2
})

driver = webdriver.Chrome(
    chrome_options=opt,
    executable_path=r"C:\SeuCaminho\chromedriver.exe")

driver.get("https://teams.microsoft.com")

try:
    print("Logando no teams")
    sleep(2)
    inptUser = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "i0116"))
    ).send_keys("youremail@email.com.br")

    btnUser = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "idSIButton9"))
    ).click()

    sleep(2)

    inptSenha = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "i0118"))
    ).send_keys("yourpassword")

    btnSenha = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "idSIButton9"))
    ).click()
except:
    print("Erro ao logar.")
    driver.close()

try:
    sleep(2)
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "idBtn_Back"))
    ).click()
except:
    print("Erro ao inicializar perfil")
    driver.close()

try:
    print("Entrando no calendario")
    joinCalendar = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="favorite-teams-panel"]/div/div[1]/div[2]/div[3]/div/ng-include/div/div/div[3]/h1'))
    )
    driver.get("https://teams.microsoft.com/_#/calendarv2")
except:
    print("erro ao entrar no teams")
    driver.close()

try:
    print("procurando aula em andamento...")
    currentAula = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[title="Ingressar"]'))
    ).click()

    print("confirmando ingresso")
    confIngres = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="ngdialog1"]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button'))
    ).click()

    joinAula = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button'))
    ).click()
    print("Entrou com sucesso!!")
except:
    print("erro ao confirmar ingresso / entrar na aula")
    driver.close()


def enviarEmail(ultimo_nome, horario):
    sleep(2)
    mail_content = "ULTIMO NOME REGISTRADO:" + \
        ultimo_nome + " às " + horario + " horas"
    # The mail addresses and password
    sender_address = 'yourmail'
    sender_pass = 'yourpassword'
    receiver_address = 'email01@gmail.com, email02@gmail.com'
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    # The subject line
    message['Subject'] = '**CHAMADA OCORRENDO!!**'
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    # login with mail_id and password
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address.split(','), text)
    session.quit()
    print('Email enviado!')


nomes = ["chamada",
         "Amanda",
         "Beatriz",
         "Bia",
         "Bia Pontes",
         "Bia Fischer",
         "Bruno",
         "Caio",
         "Cassio",
         "Davi",
         "Debora",
         "Giovana",
         "João",
         "Julia",
         "Leonardo",
         "Luigi",
         "Luiza",
         "Matheus",
         "Matheus",
         "Murilo",
         "Pedro",
         "Rodrigo",
         "Silva",
         "Gabriel",
         "Trotman",
         "Vinicius",
         "Vitor",
         "Alegre"]


def reconhecerVoz():
    r = sr.Recognizer()
    with sr.Microphone() as fonte:
        print("Escutando professor(a)")
        audio = r.listen(fonte)
        texto = r.recognize_google(audio, language='pt-BR')

        now = datetime.now()
        current_hour = now.strftime("%H:%M")
        current_min = now.strftime("%M")
        minuteInt = int(current_min)

        print("Ele disse: " + texto)
        print("Verificando se é uma chamada")
        for nome in nomes:
            if nome in texto:
                enviarEmail(texto, current_hour)
                break


sleep(2)
x = True
while x == True:
    reconhecerVoz()
    sleep(30)
