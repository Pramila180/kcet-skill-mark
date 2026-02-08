import os
print('CWD:', os.getcwd())
print('Exists skill_marks.db:', os.path.exists('skill_marks.db'))
print('\nFiles in cwd:')
for f in os.listdir('.'):
    print('-', f)
