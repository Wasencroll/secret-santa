# Your Secret Santa
this is an implementation of the secret santa game, which lets you input a list of participants, then randomly draws names
and sends out these assignments via email

## Application parts
* main.py is the app script, with all of the required functions to run the application
* /images folder contains images used in the email
* /doc folder contains some documentation
* /samples folder contains samples of how to format .txt files for the application
* contents.txt contains an example of how contents in your email could look like
* participants.txt contains an example of how to enter participants of your secret santa to the file

## How things work
* First, make sure that you change the files 'participants.txt' and 'contents.txt' in the root/main directory
   * In 'participants.txt' you should enter your participants in the format "Name, email-adress" (without the ""). Each person
should be written on a new line in this file. You do not need to put anything at the end of a line.
   * In 'contents.txt' add the text you would like to show in your email. The format is "section, text" (without "") where
section refers to a specific part of the email. Do not change the names of the sections as the email generating function will
not pick up your text if you do so. Only change the text after the ",". The comma separates section from text. Within your text
however, you can use commas if you wish to do so. End your text with a plain semicolon to tell the program that the next
section starts.

   **Note:**
   * The rules in the rules section need to be separated by a double slash ("//") as you can see in the example. This
   tells the program where one rule ends and the next one starts.
   * You can find a layout of all sections in [this image](https://github.com/Wasencroll/secret-santa/tree/master/doc/email_sections.png).
   * In addition to the sections detailed in the image, you can also define the subject line of your email as well as a preheader
   text that will only show up in the email preview in an email client.

* Then, you have the chance to exclude 1 name per participant that **cannot** be assigned to them. I created this feature in order
to not assign the same name to a person two years in a row (an issue my family was complaining about...). Of course, you can
also simply use it to exclude a name of your liking if you do not have a previous draw. If you do not want to exclude any names,
just leave the file untouched or delete it. The file should always start with the line "GIVER, RECEIVER;" and then one line per
exclude in the format "name1, name2;" where **name2** cannot be assigned to **name1**.

   **Note:**
   * You do not have to exclude a name for every person, if you just have three conditions, that's find too.
   * The program is set up to record the draw from this year into a file just like "draw2017.txt" (I wrote this 2018). This
   makes the draw next year much simpler, because the exclude condition are already on file and the program automatically knows where
   to look for them. Again, if you do not wish to exclude any names next year, simply delete the file before running the program.

* Finally, you should run the main function **santa(fromAddr, password, smtp, port)**.
    * fromAddr is the address that the secret santa assignment mails are sent from to all your participants. This could be your own email
    or another address specifically for this purpose.
    * password is the password belonging to the account in fromAddr.
    * smtp is the outgoing mail server, e.g. smtp.gmail.com.
    * port is the outgoing mail port. Note that when I connect to the server, I am using *server = smtplib.SMTP_SSL(smtp, port)*
    to force the program to use an SSL connection. In this case, the gmail port was 465. Make sure your connection details are
    correct and for SSL.


