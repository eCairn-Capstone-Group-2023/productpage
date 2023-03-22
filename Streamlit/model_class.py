from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
import numpy as np
import seaborn as sns
from types import SimpleNamespace
import datetime
import time
import itertools
import streamlit as st


class Model:
	def __init__(self):
		self.name = None
		self.tokenizer_name = None
		self.model_name = None
		self.dimensions = None
		self.rows = None
		self.device = None
		 
	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, value):
		self._name = value

	@property
	def tokenizer_name(self):
		return self._tokenizer_name

	@tokenizer_name.setter
	def tokenizer(self, value):
		self._tokenizer_name = value

	@property
	def model_name(self):
		return self._model_name

	@model_name.setter
	def model_name(self, value):
		self._model_name = value

	@property
	def dimensions(self):
		return self._dimensions

	@dimensions.setter
	def dimensions(self, value):
		self._dimensions = value

	@property
	def rows(self):
		return self._rows

	@rows.setter
	def rows(self, value):
		self._rows = value
		
	@property
	def device(self):
		return self._device

	@device.setter
	def device(self, value):
		self._device = value

	#TODO add logger

	def get_embeddings(cls, logger, test_list, progress_bar):
		tokenizer, model = cls.pretrained_setup()
		logger.model_start = datetime.datetime.now()
		embeddings_dataset = []
		next_read = time.time() + 5
		total = len(test_list)

		one_percent = 100 // total
		progress_complete = 0

		for item in test_list:
			if time.time() > next_read:
				print(f"{len(embeddings_dataset)}/{total}")
				next_read = time.time() + 5
			embeddings_dataset.append( (f'vector-{item[0]}', cls.emb(str(item[1]),model,tokenizer)[0].tolist(), {"original_id": item[0]}) )
		
			progress_complete += one_percent
			progress_bar.progress(progress_complete, text="Please Wait")
		progress_bar.progress(100)
		logger.model_stop = datetime.datetime.now()
			
		return embeddings_dataset

	@classmethod
	def emb(cls, text, model, tokenizer):
		encoded_input = tokenizer(text =text, padding=True, truncation=True, return_tensors='pt').to(cls.device)
		with torch.no_grad():
			model_output = model(**encoded_input)
		sentence_embeddings = cls.mean_pooling(model_output, encoded_input['attention_mask'])
		sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
		return np.array(sentence_embeddings.to('cpu'))
	
	# Mean Pooling - Take attention mask into account for correct averaging
	def mean_pooling(model_output, attention_mask):
		token_embeddings = model_output[0] #First element of model_output contains all token embeddings
		input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
		return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


	# Loading up the model and the tokenizer
	@classmethod
	def pretrained_setup(cls):
		tokenizer = AutoTokenizer.from_pretrained(cls.tokenizer_name)
		model = AutoModel.from_pretrained(cls.model_name).to(cls.device)
		return tokenizer, model