import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

fromEmail = 'adressemaile@gmail.com' #Adresse mail de l'expéditeur
fromEmailPassword = 'mdp' #MDP du compte de l'expéditeur
toEmail = 'adressemaild@gmail.com' #Adresse mail du destinataire

def sendEmail(image): #Fonction de création et d'envoie un mail
	msgRoot = MIMEMultipart('related') #Initialisation d'un message à plusieurs partie sur serveur Google
	msgRoot['Subject'] = 'Mouvement detecte' #Objet du mail
	msgRoot['From'] = fromEmail #Récupération de l'adresse mail de l'expéditeur
	msgRoot['To'] = toEmail #Récupération de l'adresse mail du destinataire
	msgRoot.preamble = 'Camera Exterieure a detecte un mouvement'

	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)
	msgText = MIMEText('Camera a detecte un objet')
	msgAlternative.attach(msgText)

	msgText = MIMEText('<h1>Alerte de securite</h1><h6>Mouvement detecte dans le jardin</h6><img src="cid:image1">', 'html') #Corps du mail en html et positionnement de l'image
	msgAlternative.attach(msgText)

	msgImage = MIMEImage(image) #Récupération de l'image
	msgImage.add_header('Content-ID', '<image1>')
	msgRoot.attach(msgImage)

	smtp = smtplib.SMTP('smtp.gmail.com', 587) #Adresse mail du serveur Google
	smtp.starttls() #Start connexion
	smtp.login(fromEmail, fromEmailPassword) #Login via information de connexion
	smtp.sendmail(fromEmail, toEmail, msgRoot.as_string()) #Envoie du mail
	smtp.quit() #Fin de la connexion au serveur
