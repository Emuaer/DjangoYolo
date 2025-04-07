from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
import numpy as np
import argparse
import time
import cv2
import os
# Create your views here.
from django.http import HttpResponse

from django.conf import settings
