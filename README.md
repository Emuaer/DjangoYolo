# DjangoYolo
一个简易的django前后端yolo检测客户端
A Django based web project that uses custom YOLO model, trained on google open images, to detect and count number of coco in an image.




# Requirements:

> python >3.8.10 with pip


> Django

	pip install Django==4.2.5

> opencv 4.8.0.76

	pip install opencv-python

> ultralytics

	pip install ultralytics


# Setting up the project

- go to project root DjangoYolo
- Run the Django migrations:
```
python manage.py migrate
```
- Run Django server
	python manage.py runserver



The Project should be live and accessible at 
	http://localhost:8000/emuayolo





