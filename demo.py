import argparse
import os

from core.inference.api import ProsodyNet, concate, _tokenize

from pypinyin import lazy_pinyin, Style
import time

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
print('Working directory: {0}'.format(dname))

parser = argparse.ArgumentParser()
parser.add_argument('--model_dir', default='model', help="Directory containing pretrained models")

def not_empty(s):
    return s and s.strip()

def run(nets, tokenize):
    while True:
        text = input('>> ')
        check = time.time()
        words, pos = tokenize(text)
        # print(words, pos)
        prosody=['']*len(pos)

        for i, [net, name] in enumerate(nets):
            tags = net.inference(words, pos)
            # print(name, tags)
            # print(name, concate(words, tags))
            for idx, tag in enumerate(tags):
                if tag == 'B' and idx > 0:
                    prosody[idx-1] = '#{}'.format(i+1)

        result = []
        for i, [c, p] in enumerate(zip(words, prosody)):
            c_pinyin = lazy_pinyin(c, style=Style.TONE3, neutral_tone_with_five=True)
            result.extend(c_pinyin)
            if p:
                # result.extend(' {} '.format(p))
                result.extend([p])
        print(time.time() - check)
        print(' '.join(result))


if __name__ == '__main__':
    args = parser.parse_args()

    net1 = ProsodyNet(args.model_dir, 'biaobei1')
    net2 = ProsodyNet(args.model_dir, 'biaobei2')
    net3 = ProsodyNet(args.model_dir, 'biaobei3')

    run([(net1, 'PW'), (net2, 'PPH'), (net3, 'IPH')], _tokenize())
