# DeepFramework
[![Build Status](https://travis-ci.org/issey173/DeepFramework.svg?branch=master)](https://travis-ci.org/issey173/DeepFramework)

DeepFramework is an abstract layer designed to be on top of any of your deep learning projects. 
This framework intends to provide a layer to separate your models logic (what is actually training, predicting...) from all the scripting needed to execute that, so that you can encapsulate and separate the core of your program from everything else.
With that you can actually focus on designing your architecture and forget about all the surrounding boilerplate, and what it's more important, it will speed up your prototyping and the scaffolding of your project.


## What it is vs. What it is not
What it does:

* Ease the process of starting a new DL project
* Provides classes to avoid boilerplate code
* Helps you building a processing pipeline
* Encapsulates the computing logic (training a model, validating it...) from all the other stuff so that you can easily change the underlying layer without worrying about refactor all your program

What it does not:

* Perform any kind of DL computation


## What can I find in each package?

* dframe.dataset: Classes to help you load and persist your dataset. The Dataset class provides common functions such as a batch generator, get all your dataset inputs as an array...
* dframe.model: Interface to encapsulate your models logic and definition. Right now it's only a skeleton, I expect to add more functionality on that
* dframe.pipeline: Once you already have a trained model, you can use the classes provided here to create a pipeline processing system to actually perform your application's logic. It already gives you all the process management, and a really simple and useful structure

 
 
## Big case scenarios
The project has been designed with two big scenarios in mind: the research and application. In both of them I have found a lack in terms of libraries supporting it and that's why I developed this framework.

### Research
For people looking to train and design a model. In order to do that, there's usually a need to construct a model, load a dataset, format it so that the model can process its data...
The packages dframe.dataset and dframe.model provide classes to easily code the scripts needed to do that in a clean and structured way. 
I've found out that when doing research the code tends to get messy and difficult to adapt and scale (because of the different amount of experiments needed to be conducted) so I've created those packages to, not only speed up this process, but to encourage best program practices.

### Application
Training a model sometime it's just a matter of wanting the results (e.g. for a publication) but other times you want to use it in your own application (an object detection model for your killer-app for example). 
In this case, dframe.pipeline package it's gonna suit your needs as it provides an easy way to implement a pipeline system formed by cores. Each core is a processing unit that could have your trained model inside that takes an input, process it and outputs the result.
The pipeline is in charge of connecting all the cores and of the communication with the outside world.

## Installation

This framework has been uploaded to PyPI. For an easy install:

`pip install DeepFramework`

## A word about the project
This project is in a beta state. After developing what I thought it was the main core of the framework I am releasing it so that everyone can give it a try and, most important, ptovide some feedback!
All of this is based on my experiences in programming deep learning projects, but as you can imagine, this is limitted, so one of the main reasons of releasing the beta is to gather opinions and suggestions from people that have worked on that longer than I am and have more experience than me.
I also want to mention that coding in Python is something more or less new to me, after programming in languages such as Java, C++, PHP and Javascript mainly. It might be the case where some piece of code is not as *pythonic* as it could be, or maybe there is an efficiency improvement it can be done. 
I would be very grateful if you could make me notice of those so I can improve this framework to something greater!



