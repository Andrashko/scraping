from gettext import find
from re import *

print (match(r"[А-ЯІЇЄ]{2,2}\d{6,6}" , "БЖ123456 "))
print (match(r"\w{2,2}\d{6,6}" , "FW123456"))
print (match(r"\w{1,}\s\w+" , "some words"))
print (match(r"^[А-Я]{2,2}\d{6,6}$" , "БЖ123456"))
print (match(r"^\w+@\w+\.\w+$" , "example@mail.com"))
print (match(r".{2,10}" , "БЖ123456"))
print (match(r"[^А-ЯІЇЄа-яіїє]{2,2}\d{6,6}" , "*+123456 "))
print (match(r".*" , "БЖ123456 "))
print (match(r"(\w\d){3,3}" , "a1b2c3"))
