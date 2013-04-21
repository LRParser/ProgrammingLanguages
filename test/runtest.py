import sys
import os
import subprocess

test_dir = 'test/SampleInputs/'
answers_dir = 'test/answers'
output_dir = 'test/output'

interpreter = 'python interpreterext.py'

answers = os.listdir(answers_dir)

#Create the output dir, which will be cleaned on 'make clean'
os.makedirs(output_dir)

for answer in answers:
    os.system('%s < ./%s%s > %s/%s' % (interpreter,test_dir,
                                       answer,output_dir,answer))
