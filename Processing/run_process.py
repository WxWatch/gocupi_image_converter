import glob
import os
import sys
sys.path.append("PIL")
import Processing

for filename in glob.glob('input/*.gif'):
    im = Processing.open(filename)
    im = im.convert('1')
    newFilename = os.path.splitext(filename)[0] + '.pbm'
    im.save(newFilename)
    print('python tspart.py "' + newFilename + '" "output/' + os.path.splitext(os.path.basename(filename))[0] + '.svg"')
    os.system('python tspart.py "' + newFilename + '" "output/' + os.path.splitext(os.path.basename(filename))[0] + '.svg"')