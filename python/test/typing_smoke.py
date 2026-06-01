import sentencepiece as spm

sp = spm.SentencePieceProcessor(model_file="x.model")
ids = sp.encode("hello", out_type=int)
text = sp.decode(ids)
spm.set_min_log_level(1)
