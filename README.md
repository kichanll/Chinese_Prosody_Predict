# Prosody Prediction

韵律预测停顿位置  
生产停顿等级：#1 #2 #3 #4

## Quickstart

1. 到 https://ai.tencent.com/ailab/nlp/en/index.html 下载腾讯开源的ChineseEmbedding
到根目录

2. 下载标贝开源数据，提取 000001-010000.txt 文件到根目录

3. 开始训练

```shell
sh run.sh
```

4. 运行交互式命令行进行测试

```shell
python demo.py
Working directory: /home/chan/test/Prosody_Prediction_3
2021-01-04 16:26:46,792 - ProsodyPred - DEBUG - Loaded pretrained model in 0.1708s
2021-01-04 16:26:46,807 - ProsodyPred - DEBUG - Number of Parameters: 5414614
2021-01-04 16:26:46,807 - ProsodyPred - DEBUG - Number of Trainable Parameters: 402814
2021-01-04 16:26:46,983 - ProsodyPred - DEBUG - Loaded pretrained model in 0.1280s
2021-01-04 16:26:46,983 - ProsodyPred - DEBUG - Number of Parameters: 5414614
2021-01-04 16:26:46,984 - ProsodyPred - DEBUG - Number of Trainable Parameters: 402814
2021-01-04 16:26:47,203 - ProsodyPred - DEBUG - Loaded pretrained model in 0.1727s
2021-01-04 16:26:47,203 - ProsodyPred - DEBUG - Number of Parameters: 5414614
2021-01-04 16:26:47,203 - ProsodyPred - DEBUG - Number of Trainable Parameters: 402814
Model loaded succeed
>> 高铁坐过站咋办？这样做免费返回
0.01025991439819336
gao1 tie3 #1 zuo4 guo4 zhan4 #1 za3 ban4 #3 ？ zhe4 yang4 zuo4 #1 mian3 fei4 #1 fan3 hui2
```

## API

1. 指定模型进行预测, 参考`demo.py`

```python
net1 = ProsodyNet(args.model_dir, 'pw')
words, pos = tokenize(text)
tags = net.inference(words, pos)
```

## Training(2020/12/20)

### thulac
| prosody level | accuracy | block_acc | precison | recall | loss |
| :------------ | :------- | :-------- | :------- | :----- | :--- |
| biaobei1 EVAL | 0.939 | 0.885 | 0.750 | 0.950 | 0.154 |
| biaobei2 EVAL | 0.930 | 0.747 | 0.573 | 0.853 | 0.168 |
| biaobei3 EVAL | 0.982 | 0.910 | 0.809 | 0.952 | 0.061 |
| biaobei4 EVAL | 1.000 | 1.000 | 0.999 | 1.000 | 0.000 |

### pkuseg
| prosody level | accuracy | block_acc | precison | recall | loss |
| :------------ | :------- | :-------- | :------- | :----- | :--- |
| biaobei1 EVAL | 0.940 | 0.900 | 0.799 | 0.965 | 0.154 |
| biaobei2 EVAL | 0.924 | 0.737 | 0.590 | 0.846 | 0.176 |
| biaobei3 EVAL | 0.981 | 0.909 | 0.871 | 0.953 | 0.065 |
| biaobei4 EVAL | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |

### jieba
| prosody level | accuracy | block_acc | precison | recall | loss |
| :------------ | :------- | :-------- | :------- | :----- | :--- |
| biaobei1 EVAL | 0.939 | 0.895 | 0.810 | 0.957 | 0.150 |
| biaobei2 EVAL | 0.922 | 0.751 | 0.594 | 0.865 | 0.183 |
| biaobei3 EVAL | 0.980 | 0.907 | 0.813 | 0.951 | 0.065 |
| biaobei4 EVAL | 1.000 | 0.999 | 0.930 | 0.999 | 0.000 |
