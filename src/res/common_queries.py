COMMON_QUERIES = {
    "definition": [
        {"phrase": "Where is the function load_data defined?", "symbol": "load_data"},
        {"phrase": "What is DataProcessor?", "symbol": "DataProcessor"},
        {"phrase": "Tell me where train_model is implemented.", "symbol": "train_model"},
        {"phrase": "Define clean_text.", "symbol": "clean_text"},
        {"phrase": "Which file defines extract_features?", "symbol": "extract_features"},
        {"phrase": "Where can I find compute_loss?", "symbol": "compute_loss"}
    ],
    "usage": [
        {"phrase": "Where is load_data used?", "symbol": "load_data"},
        {"phrase": "Show every place clean_data is called.", "symbol": "clean_data"},
        {"phrase": "Which scripts use fetch_records?", "symbol": "fetch_records"},
        {"phrase": "List all occurrences of filter_invalid_rows.", "symbol": "filter_invalid_rows"},
        {"phrase": "What files invoke train_model?", "symbol": "train_model"},
        {"phrase": "Is evaluate_model used in main.py?", "symbol": "evaluate_model"},
        {"phrase": "Give examples of transform being used.", "symbol": "transform"}
    ],
    "summary": [
        {"phrase": "Summarize the purpose of main.py.", "symbol": "main.py"},
        {"phrase": "What does the repo do?", "symbol": "repository"},
        {"phrase": "Overview of the pipeline in preprocess.py.", "symbol": "preprocess.py"},
        {"phrase": "What is the main functionality of data_loader.py?", "symbol": "data_loader.py"},
        {"phrase": "Explain what train_pipeline.py is for.", "symbol": "train_pipeline.py"},
        {"phrase": "Briefly describe model.py.", "symbol": "model.py"}
    ],
    "library_usage": [
        {"phrase": "How is pandas used?", "symbol": "pandas"},
        {"phrase": "Where is numpy imported and used?", "symbol": "numpy"},
        {"phrase": "List where sklearn is applied.", "symbol": "sklearn"},
        {"phrase": "Are there matplotlib plots?", "symbol": "matplotlib"},
        {"phrase": "Is requests used to fetch data?", "symbol": "requests"},
        {"phrase": "Show all usages of os.path.", "symbol": "os.path"}
    ],
    "docstring": [
        {"phrase": "Generate a docstring for clean_data.", "symbol": "clean_data"},
        {"phrase": "Write documentation for train_model.", "symbol": "train_model"},
        {"phrase": "Describe parse_config.", "symbol": "parse_config"},
        {"phrase": "Document load_json_config.", "symbol": "load_json_config"},
        {"phrase": "Add a docstring to DataCleaner.", "symbol": "DataCleaner"},
        {"phrase": "Explain inputs and outputs of fit_model.", "symbol": "fit_model"}
    ],
    "class_contents": [
        {"phrase": "What methods are in DataProcessor?", "symbol": "DataProcessor"},
        {"phrase": "Show functions in Trainer.", "symbol": "Trainer"},
        {"phrase": "List members of ModelWrapper.", "symbol": "ModelWrapper"},
        {"phrase": "Which methods does DataCleaner have?", "symbol": "DataCleaner"},
        {"phrase": "Break down PipelineManager.", "symbol": "PipelineManager"},
        {"phrase": "What does the Validator class contain?", "symbol": "Validator"}
    ],
    "generic_search": [
        {"phrase": "Find all references to data loading.", "symbol": "data loading"},
        {"phrase": "Search for tokenization functions.", "symbol": "tokenization"},
        {"phrase": "Look for mentions of preprocessing.", "symbol": "preprocessing"},
        {"phrase": "Which code handles model training?", "symbol": "model training"},
        {"phrase": "Find argument parsing logic.", "symbol": "argument parsing"},
        {"phrase": "Which parts deal with CSVs?", "symbol": "CSV"}
    ]
}
