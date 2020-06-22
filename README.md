# Let Me Answer For You
> A Simple and Powerful Deep Learning Dialog System for Question and Answering 


<img alt="Exporting from nbdev" width="1000" caption="The three Dialog Systems' methods" src="nbs/images/let_me_answer_for_you.gif">

## Requirements

The library has been tested in `python 3.7`

## Install

### Pip

The system can be installed via the `pip` command:
```
pip install let_me_answer_for_you
```

## Initialize the Dialog System 

Install the configuration files by instantiating the `SystemClass` 

```
from let_me_answer_for_you.dialog_system import DialogSystem()

ds = DialogSystem( context_data_file=None,
        faq_data_file=None,
        configs_faq=None,
        download_models=True)
```

If the **context_data_file** or the **faq_data_file** parameters are  `None` , a *data* directory will be created in the directory where the script is running. The data directory will contain the FAQ or the context CSV files

## Get Response

To get a response to a question call the method `question_answer` in the instance of  `SystemClass`


```
ds.question_answer()

Introduce question:
what can you offer me at Intekglobal?


what can you offer me at Intekglobal?:

1: expert resources to connect your different devices and exchange data within those devices
2: Connect with us for further information
3: We like to provide world class solutions with complete features what you want to impletement in your business!
```

## New Question-Answer Pair

Populate the FAQ data file with a new question answer by calling the method `new_q_a`:

```
ds.new_q_a()

Introduce question:
What type of Dialog System is this?

Introduce the answer:
Is a combination of context question answering system with a faq system
```

## New Context

The systems accept a response as a context. The advantage of having contexts is that many answers can be found in one context. To create a new context, call the `new_context` method:

```
ds.new_context()

Give context a title:
 IOT
Introduce the context:
We can provide expert resources to connect your different devices and exchange data within those devices. Further make the data accessible via web tools. Connect with us for further information.   DevOps Our team can help you organization to implement best DevOps practices that can automate the processes between software development and various IT teams, in order that they can build, test, and release software faster and more reliably.
```

## Docker

A container with all the configurations installed can be pulled it with the following instruction:

```
docker pull ejimenezr/dialog_system
```
