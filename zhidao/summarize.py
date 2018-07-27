from collections import defaultdict
import re
import os
import codecs
import sys
import pdb

reload(sys)
sys.setdefaultencoding('utf-8')

def isdigit(s):
    try:
        tmp = int(s)
    except ValueError:
        return False
    return True

def normalization(string):
    string = re.sub(r'(\n|\t)', ' ', string)
    return string

def summarize(f_path):
    with codecs.open(f_path, 'r', 'utf-8') as f:
        lines = f.readlines()
    
    dialogue_history = defaultdict(str)

    line_idx = 0
    floor_text = ''
    # read-in title
    while True:
        if line_idx < len(lines) and  not (isdigit(lines[line_idx].strip()) and isdigit(lines[line_idx+1].strip())):
            current_line = lines[line_idx]
            floor_text += current_line
            line_idx += 1
        else:
            title = normalization(floor_text)
            break
            
    dialogue_history[0] += title
    while line_idx < len(lines):
        floor_id = int(lines[line_idx].strip())
        reply_id = int(lines[line_idx+1].strip())
        floor_text = ""
        line_idx += 2
        # read-in all floor text
        while line_idx < len(lines) and not (isdigit(lines[line_idx].strip()) and isdigit(lines[line_idx+1].strip())):
            current_line = lines[line_idx]
            floor_text += current_line
            line_idx += 1
        floor_text = normalization(floor_text)
        dialogue_history[floor_id] = (dialogue_history[reply_id] + '\t' + floor_text).strip()
    
    return dialogue_history


def main():
    data_root = '../data/hupu/'
    path_iter = iter(os.listdir('../data/hupu/'))
    print('Reading list of files')
    saving_path = '../data/summarization/hupu_dialogue.dat'
    count = 0
    for f_path in path_iter:
        full_path = os.path.join(data_root, f_path)
        dialogue_histories = summarize(full_path)
        count += 1
        if count % 1000 == 0:
            print("count : {}".format(count))
        with codecs.open(saving_path, 'ab', 'utf-8') as f:
            for _, val in dialogue_histories.items():
                f.write("{}\n".format(val))
                
if __name__ == '__main__':
    main()
