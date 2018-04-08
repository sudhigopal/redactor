# The Redactor

Certian documents contain sensitive information, which cannot be shared in public. So, those data must hidden or redacted like, name, place, address, phone numbers. These kind of redaction are often done with court manuscript, police report or a hospital record. So all these information hinding comes with a cost and redaction process is often costly and time consuming

# List of redacted features

  - Names
  - Places
  - Phone Numbers
  - Addresses
  - Concept (such as kids, child, arrest etc.)
  - Dates
  
This is just the first phase of the project.

### Tech

* [Python 3.6.3] - Object oriented programming language!
* [NLTK] - NLTK is a leading platform for building Python programs to work with human language data.

And of course Redactor itself is open source with a [public repository][red] on GitHub.

### Installation

Redactor requires you to install NLTK and its directories

Install the dependencies and devDependencies and start the server.

```sh
$ git clone https://github.com/sudhigopal/redactor.git
$ tar -xvzf redactor.tar.gz
$ cd redactor
$ pip3 install setup.py
$ cd redactor
```

To run the code...

```sh
$ python3 redactor.py --input '*.txt' \
                    --input '/otherfiles/*.txt' \
                    --names --places --addresses --phones --dates \
                    --concept 'kid' \
                    --output 'files/' \
                    --stats stderr
```

### Plugins

Instructions to run the code and it gives the brief description of all the functions, my assumptions and errors found in some in-built NLTK functions

| Plugin | README |
| ------ | ------ |
| Github | [plugins/github/README.md][PlGh] |

### Development

This is a text analytics class projects from Department of Computer Science at University of Oklahoma, Norman. 

#### Functions
##### Redactor
```sh
name_loc_redactor(file_input):
    This function searchs for names and location in the given data file, redacts them and store it into the same file_input file.
    I have made use of ne_chunk to detect names, locations and GPE (another name for locations) 
    "I tried using StanfordNERTagger for the same, but was not able to connect properly with my java environment."
    Tag: --names, --places
```
```sh
date_redactor(file_input):
    This function finds different format of dates in a given file using datefinder function and redacts it. My initial approach was to write a regex and find all different date formats and it was a successful.
    "Main disadvantage of using datefinder funtion is, I found couple of errors. This function detected 'on' which was before a date and if any 'th' appeared after the date. Then this function abruptly detects certain functions." 
    Tag: --dates
```
```sh
address_redactor(file_input):
    I used regex to determine the address from the data. The format used in the regex is USPS standard format. In the future I would make it a universal regex to detect all forms of address in a given data file
    Tag: --addresses
```
```sh
gender_redactor(file_input):
    This function redacts all the gender references like he, she, him, her etc. I have used a list of gender references and run this through the data and redact them.
    Tag: --genders
```
```sh
phone_redactor(file_input):
    This function uses another regex to detect all formats of phone numbers universally. It searchs for all the possible phone numbers and redacts them. It returns the redacted file back to the main function.
    Tag: --phones
```
```sh
concept_redactor(file_input, concept):
    This function uses wordnet to find out all the possible synonyms of a concept word and redacts the whole sentence. Concept here can be defined as very sensitive words such as "kid", "kindergarten", "arrest" etc.
```
```sh
stats:
    Contains the details of which flag is redacted, file name, lenght of the redacted content and redacted content. Each column is seperated by Thorn character ('þ' U+00FE) and stored in stats.csv 
```
```sh
Input and Output procedure:
    Input is given through command line argument, which is when calling a py file. 
    I have used --input as a tag name which will be followed by input file path. Multiple --inputs can be mentioned for a given run
    Output is similarly to that of a input procedure. Tag used to present output directory is --output followed by path.
    Main Function reads the input argument using glob function and stores all the path in a list.
    The symbol used to redact text is "█" (U+2588)
```
##### Unredactor
  - This is a reverse engineering process of redaction, where in we use Machine learning algorithms to predict the possible names for which redaction is carried out.

Fucntions used in this process are:
```sh
    Main function processes the input data (redacted file) and create a list dictonary which is the test file for our given program. The list dictonary contains {"left of name", "name(redacted)","length of the name","right of the name"}. 
```
```sh
get_entity(text):
    This function takes a text data as an input and lists out all the possible names, word which is left of names and word which is in right of names.
```
```sh
get_features(glob_text,tested_names):
    This function creates name feature for training the model. This feature is stored in a list dictonary similar to our main function's test dictonary. The list dictonary contains {"left of name", "name","length of the name","right of the name"}.
```
```sh
get_prediction(tested_names):
    This function takes in the test name list as an input. I have used KNeighborsClassifier for which predicts the 5 possible names which could perfectly fit into the redacted content.
```
### Sample Input and Output
```
I/P
My phone number is 

+1(405)-123-0000
(405)1230000
405-123-0000
4051230000

O/P
My phone number is 

████████████████
████████████
████████████
██████████
```
### Testing
 - To execute the pytests, go to the parent "redactor" directory where "setup.py" resides. Execute the below command to run all the tests
```sh
"python3 setup.py test"
```

### Assumptions
 - Address is not a regular format, it changes with the region where the place reside. It is very hard to compile all formats of address. This function will just help you to detect USPS (United States Postal Services) format address representation. It is appreciated, if one can add any address format in future.
 - This goes same with the phone number. I have tried to cover almost all possible ways a phone number can be represented. 
 - I have used a list for gender referrences, there exists a slight chance where I might have missed some of the references due to my limited knowledge with the language.

### Todos
 - Can try to implement other classifier and check if the predicited names are the actually true.
 - usage of many test files at once
 
[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [glob]: <https://docs.python.org/3/library/glob.html>
   [red]: <https://github.com/sudhigopal/>
   [git-repo-url]: <https://github.com/sudhigopal/redactor.git>
   [NLTK]: <http://www.nltk.org/>
   [Python 3.6.3]: <https://www.python.org/>
   [PlGh]: <https://github.com/sudhigopal/redactor/blob/master/redactor/README>
   
