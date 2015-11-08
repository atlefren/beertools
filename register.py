import pypandoc
import os

doc = pypandoc.Document()
doc.markdown = open('README.MD').read()
f = open('README.txt', 'w+')
f.write(doc.rst)
f.close()
os.system("setup.py register")
os.remove('README.txt')
