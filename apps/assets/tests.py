from django.test import TestCase
import  subprocess,os
# Create your tests here.

num = 1
count = 0

while (num < 101):
    count += num
    num += 2
print (count)