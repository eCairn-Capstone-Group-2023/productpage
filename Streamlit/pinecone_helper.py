import datetime
import numpy as np
import itertools

def chunks(iterable, batch_size=100):
		"""A helper function to break an iterable into chunks of size batch_size."""
		it = iter(iterable)
		chunk = tuple(itertools.islice(it, batch_size))
		while chunk:
			yield chunk
			chunk = tuple(itertools.islice(it, batch_size))

def uploadToPineCone(logger, index, embeddings_dataset):
	#TODO ask about these two
	vector_dim = 384
	vector_count = len(embeddings_dataset)

	# Upsert data with 100 vectors per upsert request
	logger.pinecone_Ustart = datetime.datetime.now()
	for ids_vectors_chunk in chunks(embeddings_dataset, batch_size=100):
		index.upsert(vectors=ids_vectors_chunk, namespace=logger.pinecone_namespace)  # Assuming `index` defined elsewhere

	# with pinecone.Index('example-index', pool_threads=30) as index:
	#     # Send requests in parallel
	#     async_results = [
	#         index.upsert(vectors=ids_vectors_chunk, async_req=True)
	#         for ids_vectors_chunk in chunks(example_data_generator, batch_size=100)
	#     ]
	#     # Wait for and retrieve responses (this raises in case of error)
	#     [async_result.get() for async_result in async_results]
	logger.pinecone_Ustop = datetime.datetime.now()
	
	#FIXME
def uploadLog(logger, index, embeddings_dataset):
	logger.pinecone_Qstart = datetime.datetime.now()
	top = index.query(
		vector=[embeddings_dataset[0][1]],
		top_k = logger.top_n+1,
		include_values=False,
		namespace=logger.pinecone_namespace
	)
	logger.pinecone_Qstop = datetime.datetime.now()
	logger.output = [(int(i["id"]), float(i["score"])) for i in top["matches"][1:]]
	logger.pinecone_Kmin = min(map(lambda x: x[1], logger.output))
	logger.pinecone_Kmax = max(map(lambda x: x[1], logger.output))
	logger.pinecone_Kavg = float(np.average(list(map(lambda x: x[1], logger.output))))
	logger.system_stop = datetime.datetime.now()
	logger.check_vars()
	list(map(lambda x: type(x), logger.check_vars()))
	type(round(logger.output[0][1],2))
	logger.upload_to_db()