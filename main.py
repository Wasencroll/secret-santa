import email.utils
import random
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from PIL import Image, ImageDraw, ImageFont
import os, sys, traceback, logging
import re
import datetime


# function to load last year's draw
def last_year():
    last_draw = []
    givers = []
    receivers = []
    now = datetime.datetime.now()
    last_year = int(now.year) -1

    if os.path.exists('draw'+str(last_year)+'.txt'):
        file = open('draw'+str(last_year)+'.txt', 'r')
        items = file.read().split(';')[1:]
        for i in range(len(items)-1):
            last_draw.append(items[i].strip().split(',', 1))
            givers.append(last_draw[i][0])
            receivers.append(last_draw[i][1].lstrip().replace('\n', ' '))
        dic = dict(zip(givers, receivers))
    else:
        dic = {}
    return dic


# function to load participants from file (participants.txt) into python list
def load_participants():
    participants = []
    try:
        file = open('participants.txt', 'r')
        lines = file.read().splitlines()
        for line in lines:
            participants.append(re.sub(r'\s', '', line).split(','))
    except:
        logging.exception(">>> Please check your 'participants.txt' file again")
    return participants


# function to load email text contents from file (contents.txt) into python dictionary, format "email part" -> "text"
def load_contents():
    contents = []
    sections = []
    txt = []
    try:
        file = open('contents.txt', 'r')
        items = file.read().split(';')
        for i in range(len(items)-1):
            contents.append(items[i].strip().split(',', 1))
            sections.append(contents[i][0])
            txt.append(contents[i][1].lstrip().replace('\n', ' '))
        dic = dict(zip(sections, txt))
    except:
        logging.exception(">>> Please check your 'contents.txt' file again!")
    return dic


# function to create html list object based on an input list (for html email alternative)
def html_lists(list, ulstyle, listyle):
    html_list = '<ul ' + ulstyle + '>'
    for item in list:
        html_list = html_list + '<li ' + listyle + '>' + item + "</li>"
    html_list = html_list + '</ul>'
    return html_list


# function to create unordered list ("-") text string based on input list (for plain text email alternative)
def plain_lists(list):
    plain_list = ""
    for item in list:
        plain_list = plain_list + "- " + item + '\n'
    return plain_list


# function that generates the email for each participant
def create_mail(contents, gives, toAddr, receives, fromAddr):

    # CSS styling for <ul> and <li> items
    ulstyle = 'style="Margin-bottom: 30px !important; font-size:16px !important; line-height: 1.5 !important;"'
    listyle = 'style="margin: 0; font-family: "Georgia"; font-size: 16px; line-height: 1.5; ' \
              'text-align: left;"'

    # grabbing all rules from the dictionary, splitting rules string into single rules
    # and saving them in a separate list, then generating <ul>/<li> html string / plain text string
    rules_raw = contents['rules']
    rules = rules_raw.split('//')
    rules = [i.strip(' ') for i in rules]
    rules_html = html_lists(rules, ulstyle, listyle)
    rules_plain = plain_lists(rules)

    # mail basic information and structure
    msgRoot = MIMEMultipart('mixed')
    msgRoot['From'] = email.utils.formataddr(("Your Secret Santa", fromAddr))
    msgRoot['To'] = email.utils.formataddr((gives, toAddr))
    msgRoot['Subject'] = contents['subject']

    msgAlternative = MIMEMultipart('alternative')
    msgRelated = MIMEMultipart('related')

    # adding header image to mail
    fp = open('images/header-image.jpg', 'rb')
    msgHeaderImage = MIMEImage(fp.read())
    fp.close()

    msgHeaderImage.add_header('Content-ID', '<image1@gmail.com>')
    msgHeaderImage.add_header('Content-Disposition', 'inline; filename="christmasbanner.jpg"')

    # adding secret santa name image to mail
    fp = open('temp.jpg', 'rb')
    msgSantaImage = MIMEImage(fp.read())
    fp.close()

    msgSantaImage.add_header('Content-ID', '<image2@gmail.com>')
    msgSantaImage.add_header('Content-Disposition', 'inline; filename="yoursecretsanta.jpg"')

    # mail body, plain text and html alternatives
    plain_text = (contents['greeting'] + '\n' + '\n' + contents['intro'] + '\n' + '\n' + contents['announcement']
                  + '\n' + '\n' + "Du beschenkst dieses Jahr " + receives.upper() + "." + '\n' + '\n' + contents[
                      'rules-intro']
                  + '\n' + rules_plain + '\n' + contents['outro'] + '\n' + '\n' + contents['goodbye'])
    html = """\
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head></head>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <!--[if !mso]><!-->
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <!--<![endif]-->
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title></title>
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.5.0/css/all.css" 
                integrity="sha384-B4dIYHKNBt8Bc12p+WXckhzcICo0wtJAoU8YZTY5qE0Id1GSseTk6S+L3BlXeVIU" crossorigin="anonymous">
        <style type="text/css">
            /* Basics */
            body {
                margin: 0 !important;
                padding: 0;
                background-color: #ffffff;
            }
            table {
                border-spacing: 0;
                font-family: "Georgia";
                color: #333333;
            }
            td {
                padding: 0;
            }
            img {
                border: 0;
            }
            div[style*="margin: 16px 0"] { 
                margin:0 !important;
            }
            .wrapper {
                width: 100%;
                table-layout: fixed;
                -webkit-text-size-adjust: 100%;
                -ms-text-size-adjust: 100%;
            }
            .webkit {
                max-width: 700px;
                margin: 0 auto;
            }
            .outer {
                Margin: 0 auto;
                width: 95%;
                max-width: 700px;
            }
            .full-width-image img {
                width: 100%;
                max-width: 700px;
                height: auto;
            }
            .inner {
                padding: 20px;
            }
            p {
                Margin: 0;
            }
            a {
                color: #ee6a56;
                text-decoration: underline;
            }
            ul {
                font-family: "Georgia";
                font-size: 16px;
                line-height: 1.5;
                text-align: left;
                Margin-bottom: 30px;
            }
            .ul {
                font-family: "Georgia";
                font-size: 16px;
                line-height: 1.5;
                text-align: left;
                Margin-bottom: 30px;
            }
            .h1 {
                font-size: 36px;
                font-weight: bold;
                text-align: center;
                Margin-bottom: 30px;
            }
            .h2 {
                font-size: 20px;
                font-weight: 500;
                text-align: center;
                Margin-bottom: 30px;
            }
            .text {
                font-size: 16px;
                text-align: justify;
                line-height: 1.5;
                Margin-bottom: 10px;
            }
            .footer {
                font-family: "Georgia";
                color: rgba(255,255,255, 0.8);
                Margin: 0;
                padding: 0 20px;
                font-size: 12px;
                text-align: left;
            }
            .footer a {
                color: rgba(255,255,255, 0.6);
                float: right;
            }
            .footer a:hover {
                color: #ffffff;
            }
            /* One column layout */

            .one-column .contents {
                text-align: center;
            }
            .one-column p {
                font-family: "Georgia";
            }
        </style>
    <!--[if (gte mso 9)|(IE)]>
        <style type="text/css">
            table {border-collapse: collapse;}
        </style>
    <![endif]-->
    </head>

    <body style="margin: 0 !important; padding: 0; background-color: #ffffff;">
        <center class="wrapper" style="max-width: 700px; width: 100%; table-layout: fixed; -webkit-text-size-adjust: 100%;
                -ms-text-size-adjust: 100%;">
        <div class="webkit" style="max-width: 700px; margin: 0 auto;">
            <!--[if (gte mso 9)|(IE)]>
            <table width="700" align="center" cellpadding="0" cellspacing="0" border="0">
            <tr>
            <td>
            <![endif]-->
            <table class="outer" align="center" style="border: 1px solid #b3000c; border-spacing: 0; 
                font-family: "Georgia"; Margin: 0 auto; width: 95%; max-width: 700px;">
                <tr>
                    <td style="display:none !important; visibility:hidden; mso-hide:all; font-size:1px; color:#ffffff;
                        line-height:1px; max-height:0px; max-width:0px; opacity:0; overflow:hidden;">
                        """ + contents['preheader'] + """            
                    </td>
                    <td align="center" style="background-color: #b3000c; padding: 10px;" class="full-width-image">
                        <img src="cid:image1@gmail.com" style="width: 100%; max-width: 700px; height: auto;" 
                        alt='""" + contents['alt1'] + """'>
                    </td>
                </tr>
                <tr>
                    <td class="one-column" align="center">
                        <table width="90%" align="center" style="border-spacing: 0; font-family: "Georgia";">
                            <tr>
                                <td class="inner contents" style="padding: 20px;">
                                    <p class="h1" style="margin: 0; font-size: 36px; font-weight: bold; text-align: center;
                                        Margin-bottom: 30px;">""" + contents['title'] + """</p>
                                    <p class="h2" style="margin: 0; font-size: 20px; font-weight: 500; text-align: center;
                                        Margin-bottom: 30px;">""" + contents['subtitle1'] + """</p>
                                    <p class="text" style="margin: 0; font-size: 16px; text-align: justify; line-height: 1.5;
                                        Margin-bottom: 10px;">""" + contents['greeting'] + """</p>
                                    <p class="text" style="margin: 0; font-size: 16px; text-align: justify; line-height: 1.5;
                                        Margin-bottom: 10px;">""" + contents['intro'] + """</p>
                                    <p class="text" style="margin: 0; font-size: 16px; text-align: justify; line-height: 1.5;
                                        Margin-bottom: 10px;">""" + contents['announcement'] + """</p>
                                </td>
                            </tr>
                            <tr>
                                <td class="inner full-width-image" align="center" style="padding: 20px;">
                                    <img src="cid:image2@gmail.com" style="width: 100%; max-width: 700px; height: auto;"
                                    alt='""" + contents['alt2'] + """'>
                                </td>
                            </tr>
                            <tr>
                                <td class="inner contents" style="padding: 20px;">
                                    <p class="h2" style="margin: 0; font-size: 20px; font-weight: 500; text-align: center;
                                        Margin-bottom: 30px;">""" + contents['subtitle2'] + """</p>
                                    <p class="text" style="margin: 0; font-size: 16px; text-align: justify; line-height: 1.5;
                                        Margin-bottom: 10px;">""" + contents['rules-intro'] + """</p>
                                    """ + rules_html + """
                                    <p class="text" style="margin: 0; font-size: 16px; text-align: justify; line-height: 1.5;
                                        Margin-bottom: 10px;">""" + contents['outro'] + """</p>
                                    <p class="text" style="margin: 0; font-size: 16px; text-align: justify; line-height: 1.5;
                                        Margin-bottom: 10px;">""" + contents['goodbye'] + """</p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td class="one-column" align="center" height="60" style="background-color: #b3000c;">
                        <table width="90%" style="border-spacing: 0; font-family: "Georgia";">        
                            <tr width="100%">
                                <td width="70%" class="footer" style="Margin: 0; padding: 0 0 0 20px
                                !important; color: #ffffff !important;">
                                    <p style="margin: 0; font-family: "Georgia"; color: rgba(255,255,255, 0.8) !important; 
                                        font-size: 12px; text-align: left;">Your Secret Santa - A Python Tool</p>
                                    <p style="margin: 0; font-family: "Georgia"; color: rgba(255,255,255, 0.8); 
                                        font-size: 12px; text-align: left;">2018. Alexander Croll.</p>
                                </td>
                                <td width="30%" align="right" class="footer" style="float: right !important;">
                                    <a style="align: right !important;" target="_blank" 
                                    href="https://github.com/Wasencroll/secret-santa">
                                    <i class="fab fa-github fa-3x"></i></a>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
            <!--[if (gte mso 9)|(IE)]>
            </td>
            </tr>
            </table>
            <![endif]-->
        </div>
        </center>
    </body>
    </html>"""

    # mail alternatives, last part is preferred version
    part1 = MIMEText(plain_text, 'plain')
    part2 = MIMEText(html, 'html')

    # adding alternatives to message and sending
    msgRelated.attach(part2)
    msgAlternative.attach(part1)
    msgAlternative.attach(msgRelated)
    msgRoot.attach(msgAlternative)
    msgRelated.attach(msgHeaderImage)
    msgRelated.attach(msgSantaImage)
    text = msgRoot.as_string()

    return text


# main function, assigns secret santa partners, mails assignments to participants
# fromAddr = mail address you're sending from, password = corresponding password,
# smtp = outgoing smtp server, port = SSL port
def santa (fromAddr, password, smtp, port):

    server = smtplib.SMTP_SSL(smtp, port)
    server.login(fromAddr, password)

    print("Welcome to Your Secret Santa!" + '\n')

    # loading email contents from text file into dictionary
    print("> loading email contents from file...")
    contents = load_contents()

    # loading participants from file into list
    print("> loading participants from file...")
    participants = load_participants()

    # number of participants and mails being sent for review purposes
    countParticipants = len(participants)
    countMails = 0

    print("> a total of " + str(countParticipants) + " participants have been found...")
    print("> participant list: " + '\n' + str(participants))

    # loading draw from previous year, initializing list to log this year's draw
    last_draw = last_year()
    new_draw = [["GIVER", "RECEIVER"]]

    # shuffling participant list to avoid possibility of having last two givers excluding each other due to last year's draw
    # example: A gifted B, B gifted A last year, if (A, B) are last two in participant list, there is a scenario where
    # (A, B) could also be last two names to draw from
    while (participants[-1][0] == last_draw.get(participants[-2][0], '')) or (participants[-2][0] == last_draw.get(participants[-1][0], '')):
        random.shuffle(participants)
    hat = [item[0] for item in participants]

    print("> starting secret santa assignments...")

    # Iterating through participant list one-by-one, determining current participant (gives)
    # and next participant (receives)
    for i in range(len(participants)):
        gives = participants[i][0]
        toAddr = participants[i][1] # email address of 'gives'
        valid_hat = [item for item in hat if item not in (gives, last_draw.get(gives, ''))]

        if len(valid_hat) > 2:
            receives = random.choice(valid_hat)
        else:
            if participants[-1][0] in valid_hat:
                receives = participants[-1][0]
            else:
                receives = random.choice(valid_hat)

        # Remove the name that was just drawn from the hat
        hat.remove(receives)

        # Rendering text on image to display receiver of gift in email in illustrative fashion,
        # Determine font size based on text height in perspective to overall image height
        # to ensure identical text height on all rendered images
        fontSize = 1
        myFont = ImageFont.truetype("Georgia.ttf", fontSize)
        image = Image.open('images/name-image.jpg')
        draw = ImageDraw.Draw(image)
        img_fraction = 0.13 # change fraction to adjust text height in image
        txt = receives # text to render in image

        while myFont.getsize(txt)[1] < image.size[1]*img_fraction:
            fontSize += 1
                # print("font size: " + str(fontSize))
            myFont = ImageFont.truetype("Georgia.ttf", fontSize)

        # Getting image (W, H) and text (w, h) dimensions for centering text on image
        W, H = image.size
        w, h = myFont.getsize(txt)

        # Drawing text on center of image
        draw.text(((W-w)/2, (H-h)/2), receives, font=myFont, fill="black")

        # Saving image as temp file to current directory
        image.save('temp.jpg', 'JPEG')

        # Some testing to keep track of how/if application works
        # print("final font size: " + str(fontSize))
        # print("image dimension: " + str(W) + ", " + str(H))
        # print("font dimension: " + str(w) + ", " + str(h))
        # print(gives + " - " + toAddr)
        # print(gives + " gives to " + receives)

        mail = create_mail(contents, gives, toAddr, receives, fromAddr)

        server.sendmail(fromAddr, toAddr, mail)

        # Removing temp image from directory, so no secrets are revealed
        os.remove('temp.jpg')

        # Counting number of mails sent
        countMails += 1

        # log secret santa draw into list in format gives, receives
        new_draw.append([gives, receives])

    # saving this year's draw to file for next year's draw name excluding
    with open('private/draw'+str(datetime.datetime.now().year)+'.txt', 'w') as f:
        for sub in new_draw:
            f.write(str(sub[0]) + ', ' + str(sub[1]) + ';\n')

    # logging out from email server
    server.quit()

    print("> a total of "+str(countMails) + " mails have been sent to " + str(countParticipants) + " participants...")
    print('\n' + "Merry Christmas!")

# Calling Main to run Your Secret Santa
santa([fromAddr], [password], [smtp], [port])
