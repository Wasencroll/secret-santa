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
* first make sure that you change the files 'participants.txt' and 'contents.txt' in the root/main directory
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
* You can find a layout of all sections in [this image](https://github.com/Wasencroll/secret-santa/doc/email_sections.png).
* In addition to the sections detailed in the image, you can also define the subject line of your email as well as a preheader
text that will only show up in the email preview in an email client.
