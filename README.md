
# Master King Calculation DEMO:
<iframe width="854" height="480" src="https://www.youtube.com/embed/VYOjWnS4cMY" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>


# Motivation
Making calculations in a web page has never been an easy task for anyone. Many times, programmers have to find outside help, such as hiring mathematicians and designers to assist in properly developing, implementing, and analyzing a program or algorithm. One popular example of this is Wolfram Alpha. Occasionally, when a person is in need of such a program, they resort to finding and utilizing different websites to get the results they need. This requires the user to get familiar with a potentially overwhelming amount of different software. Therefore, they might decide to make accounts and pay for services like the aforementioned Wolfram Alpha. Additionally, sometimes these very programs are slow and unresponsive, and often scale suboptimally on different screens. These factors can cause the user to have an unpleasant and needlessly complicated experience. This is where MathML with Master King Calculations comes in. 
 
MathML is an application of XML for describing mathematical notations and capturing both its structure and content. The mathematical notations can be created with them. Master King Calculations intends to close the boundaries between coders and notations of the functions that they will use, engineer designer and mathematics  will comes to web page development. This tool will  be able to serve a development environment for web developers in order to calculate, and make equations in websites with easier programming methods. This will make it available for  persons that are interest on developing on making  new libraries and designs,  creating an and supporting to education.
 
Using the Master King Calculations, generating MathML is fast, easy and maintainable in all devices . This is utilizing the concept of object oriented and  penmanship capabilities from high level essential,  and concurrency with the languages. Master King Calculations uses these same concepts of Math, on generating both simple and complex mathematical equations by simply calling functions. Its purpose is to become an easy to learn programming language for students in school and job works. This is made to save time and for the programmer’s convenience when it comes to adding new functions and customizing new commands in the webpages.




### Python 3.6.5
For this project you will need to have the JDK installed and in your path. You can find it  [here](https://www.python.org/downloads/ )

To verify if java is installed and in your system path open a terminal and type
```bash
$ java -version
```
You should receive the version in the next line.


### JavaCC
You will also need to install JavaCC. To download  visit the [JavaCC Homepage](https://javacc.java.net/ "JavaCC Home").

### Building PieL

1. Open Terminal on the folder where the .jj file is along with the javacc.jar file is.
2. Run these commands
```bash
java -cp "path to javacc.jar" javacc "path to PieL.jj"
```
```bash
javac *.java
```


### Instructions to run the language:
1. Run a terminal inside the folder where the parser,lexer and intermidiate code reside.
```bash
java PieL
```
3. This will allow you to start writing code in the PieL Language.

Example code to write (the words inside the quotations are to be replaced for information of your choice ex. ID would be the name of a variable you have created):

a) Crea un "TYPE" llamado "ID" con valor ("STRING" OR "NUMBER" OR "ID").

b) Crea un "STRUCT" de "TYPE" llamado "ID" y valores [ "MULTITERM" ].

c) Si ("STRING" OR "NUMBER" OR "ID") es igual a ("STRING" OR "NUMBER" OR "ID") {"insert instructions here"}.

d) Imprime "ID".

e) Imprime arreglo o lista "ID".
