import os
import re
import thulac
import pkuseg
import jieba.posseg as pseg
import jieba

def tokenize(raw_path, tokenized_path):
    thu1 = thulac.thulac()
    seg = pkuseg.pkuseg(postag=True)
    with open(raw_path, 'r') as f:
        data = f.read()
        new_data = re.sub('#\d', '', data)
        lines = new_data.split('\n')

        with open(tokenized_path, 'w') as f:
            for i in range(0, len(lines)-1, 2):
                line = lines[i].split('\t')
                id = line[0]
                sent = line[1]
                #text = thu1.cut(sent, text=True)
                text = ' '.join(['{}_{}'.format(key, value) for key, value in seg.cut(sent)])
                #text = ' '.join(['{}_{}'.format(key, value) for key, value in pseg.cut(sent, use_paddle=True)])
                f.write(text + '\n')

                if i % 200 == 0:
                    print("Process {0}.".format(i))

def cut_word(raw_path, words_path):
    thu1 = thulac.thulac()
    seg = pkuseg.pkuseg()
    with open(raw_path, 'r') as f:
        data = f.read()
        new_data = re.sub('#\d', '', data)
        lines = new_data.split('\n')

        with open(words_path, 'w') as f:
            for i in range(0, len(lines)-1, 2):
                line = lines[i].split('\t')
                id = line[0]
                sent = line[1]
                #text = ' '.join([i[0] for i in thu1.cut(sent)])
                text = ' '.join(seg.cut(sent))
                #text = ' '.join([key for key, _ in pseg.cut(sent, use_paddle=True)])
                f.write(text + '\n')

                if i % 200 == 0:
                    print("Process {0}.".format(i))

def extract_text(raw_path, original_text_path):
    with open(raw_path, 'r') as f:
        lines = f.readlines()
        lines = lines[::2]
        with open(original_text_path, 'w') as fout:
            for line in lines:
                line = line.split('\t')
                fout.write(line[1])


def split_text(original_text_path, texts_path):
    def split_line(lines, separator, file):
        parts = []
        for line in lines:
            parts += line.strip().split(separator)
        parts_ = [re.sub('#\d', '', part) for part in parts]
        file.write(' '.join(parts_) + '\n')
        return parts

    with open(original_text_path, 'r') as f:
        lines = f.readlines()

        f1 = open(texts_path[0][0], 'w')
        f2 = open(texts_path[1][0], 'w')
        f3 = open(texts_path[2][0], 'w')
        f4 = open(texts_path[3][0], 'w')
        for line in lines:
            line = split_line([line], texts_path[3][1], f4)
            line = split_line(line, texts_path[2][1], f3)
            line = split_line(line, texts_path[1][1], f2)
            split_line(line, texts_path[0][1], f1)

        f1.close()
        f2.close()
        f3.close()
        f4.close()


def tag(words_path, tokenzied_path, tag_pos_path):
    f = open(tokenzied_path, 'r')
    lines = f.readlines()
    f2 = open(words_path, 'r')
    lines2 = f2.readlines()

    fout = open(tag_pos_path, 'w')

    def compute_range(items):
        cur = 0
        ranges = []
        start = []
        end = []
        for item in items:
            ranges.append((cur, cur + len(item)))
            start.append(cur)
            end.append(cur + len(item))
            cur += len(item)
        return start, end

    for tok, sep in zip(lines2, lines):
        toks = tok.strip().split(' ')
        seps = sep.strip().split(' ')
        tok_s, tok_e = compute_range(toks)
        sep_s, sep_e = compute_range(seps)

        pairs = []
        for i in range(len(toks)):
            if (tok_s[i] in sep_s):
                pairs.append(toks[i] + '_B')
            elif (tok_e[i] in sep_e):
                pairs.append(toks[i] + '_I')
            else:
                pairs.append(toks[i] + '_I')
        fout.write(' '.join(pairs) + '\n')


def split_pos(tokenzied_path, idx, pos_path):
    with open(tokenzied_path, 'r') as f:
        lines = f.readlines()
        f = open(pos_path, 'w')
        for line in lines:
            parts = line.strip().split(' ')
            parts = [part.split('_')[idx] for part in parts]
            f.write(' '.join(parts) + '\n')


def integrate_pos(data_path, pos_path, tag_pos_path):
    with open(data_path, 'r') as f_data:
        with open(pos_path, 'r') as f_pos:
            with open(tag_pos_path, 'w') as f_new:
                for data, pos in zip(f_data, f_pos):
                    data = data.strip().split()
                    pos = pos.strip().split()
                    for i in range(len(pos)):
                        data[i] += '_' + pos[i]
                    new = " ".join(data)
                    f_new.write(new + '\n')


if __name__ == "__main__":
    # raw_path = 'data/biaobei/processed/000001-010000.txt'
    OUTPUT_DIR = 'output'
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    raw_path = '000001-010000.txt'
    tokenized_path = os.path.join(OUTPUT_DIR, 'tokenized.txt')
    words_path = os.path.join(OUTPUT_DIR, 'words.txt')
    original_text_path = os.path.join(OUTPUT_DIR, 'text.txt')
    tokenize(raw_path, tokenized_path)
    cut_word(raw_path, words_path)
    extract_text(raw_path, original_text_path)

    texts_path = [(os.path.join(OUTPUT_DIR, 'text{}.txt'.format(i)), '#{}'.format(i)) for i in range(1,5)]
    split_text(original_text_path, texts_path)

    pos_path = os.path.join(OUTPUT_DIR, 'pos.txt')
    split_pos(tokenized_path, 1, pos_path)

    for i in range(4):
        tag_path = os.path.join(OUTPUT_DIR, 'final_tag_{}.txt'.format(i + 1))
        tag_pos_path = os.path.join(OUTPUT_DIR, 'final_tag_{}_pos.txt'.format(i + 1))

        tag(words_path, texts_path[i][0], tag_path)
        integrate_pos(tag_path, pos_path, tag_pos_path)
