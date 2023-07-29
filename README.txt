Tokaji: Firenze
Novello: Rome
N01/Novello: Pisa

Workflow:
	generate_dataset.py:
		(1) Training_ids
		(2) Test_ids
		(3) Training_features - SVM, GBDT
		(4) Test_features
	
	(1), (2) are used for:
		where_next_input_generator.py
		baseline_probability.py
	
	dataset_stats.py (distrib, max len etc.)