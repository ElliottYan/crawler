import codecs

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def extract_singer_set(file_path, threshold):
    singer_set = set()
    count = 0
    with codecs.open(file_path, 'r', 'utf-8') as f:
        for line in f:
            count += 1
            tmp = line.strip().split('\t')
            name = tmp[0]
            hotness = int(tmp[-1])
            if hotness < threshold:
                break
            singer_set.add(name)
            if count % 10000 == 0:
                print(count)
    return singer_set

def write_singer_set(singer_set, out_file_path):
    with open(out_file_path, 'wb') as f:
        for item in singer_set:
            f.write("{}\n".format(unicode(item)).encode('utf-8'))


if __name__ == '__main__':
    file_path = './data/singer_album_song_hot.sort'
    threshold = 1000
    singer_set = extract_singer_set(file_path, threshold)
    
    out_file_path = './data/extracted_singer_set_{}.txt'.format(threshold)
    write_singer_set(singer_set, out_file_path)