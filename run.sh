python preprocess.py
python build_biaobei_dataset.py
python build_vocab.py
python build_embedding.py
python train.py
python evaluate.py --data_dir=output/biaobei1 --model_dir=model/biaobei1 --emb_dir=output
python evaluate.py --data_dir=output/biaobei2 --model_dir=model/biaobei2 --emb_dir=output
python evaluate.py --data_dir=output/biaobei3 --model_dir=model/biaobei3 --emb_dir=output
python evaluate.py --data_dir=output/biaobei4 --model_dir=model/biaobei4 --emb_dir=output