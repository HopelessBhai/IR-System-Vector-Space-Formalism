
# Search Engine Application

This project implements a search engine application that supports multiple models and allows user input queries. The code works for both Python 2 and Python 3 and includes pre-calculated matrices for efficient search performance. The project also provides an autocomplete feature for user queries.

## Prerequisites

Ensure you have the necessary dependencies installed before running the search engine. You may need:
- Python (version 2.x or 3.x)
- NumPy

You can install the necessary Python dependencies by running:
```bash
pip install -r requirements.txt
```

## Files Description

- **`main.py`**: The main file to run the search engine.
- **`term_term.npy`**: Contains pre-calculated similarity values between tokens in the document corpus. This is used by the CRN model to improve search results.
- Other files in the folder may include code for tokenization, segmentation, and model implementation.

## Usage

To run the search engine, use the following command with the appropriate arguments:

```bash
python main.py [-custom] [-dataset DATASET FOLDER] [-out_folder OUTPUT FOLDER] [-model MODEL_TYPE (CRN|VSM|LSI)]
               [-segmenter SEGMENTER TYPE (naive|punkt)] [-tokenizer TOKENIZER TYPE (naive|ptb)] [-autocomplete AUTOCOMPLETE]
```

### Example Usage

#### 1. Custom User Query
If you want to input a custom query, pass the `-custom` flag along with the model type:
```bash
python main.py -custom -model 'CRN'
```
You will be prompted to enter your query:
```bash
> Enter query below
```

#### 2. Autocomplete Functionality
To enable autocomplete functionality for user queries, use the `-autocomplete` flag with `-custom`:
```bash
python main.py -model 'CRN' -custom -autocomplete
```
You will be prompted to enter an incomplete query:
```bash
> Enter query below
```
The system will then provide suggestions based on the most complete matches from the stored corpus queries. If multiple queries match, you will be prompted to choose one.

#### 3. Cranfield Dataset
When the `-custom` flag is not used, the search engine will consider all the queries in the Cranfield dataset. The following metrics will be computed:
- **Precision@k**
- **Recall@k**
- **F-score@k**
- **nDCG@k**
- **Mean Average Precision (MAP)**

### Output

For both custom and dataset-based queries, the system will generate two output files in the specified `OUTPUT FOLDER`:
- `*queries.txt`: Contains the queries after preprocessing.
- `*docs.txt`: Contains the documents after preprocessing.

Additionally, when a custom query is provided, the IDs of the five most relevant documents will be printed to the console.

## Notes

- The `term_term.npy` file is used exclusively by the CRN model to enhance the similarity calculations between terms.
- When using the `-autocomplete` flag, it must always be used in conjunction with the `-custom` flag.
- Ensure that the dataset folder is correctly specified if you are using a dataset for evaluation.


## Implementation

The search engine application is implemented using various models and techniques to deliver efficient and accurate search results. Below are the key components:

### 1. Models
- **CRN (Contextual Relevance Network)**: A model that uses term-term similarity values (from `term_term.npy`) to enhance the search results based on context.
- **VSM (Vector Space Model)**: A classical information retrieval model that represents documents and queries as vectors in a high-dimensional space.
- **LSI (Latent Semantic Indexing)**: A model that reduces the dimensionality of the document-term matrix and captures latent relationships between terms and documents.

### 2. Tokenization and Segmentation
- The application provides options to use different segmenters and tokenizers. 
  - **Segmenters**: Options include `naive` (basic segmentation) and `punkt` (more advanced segmentation using NLTK's Punkt tokenizer).
  - **Tokenizers**: Options include `naive` (basic whitespace tokenization) and `ptb` (Penn Treebank tokenizer for more sophisticated tokenization).

### 3. Autocomplete
The autocomplete feature uses pre-processed queries stored in the corpus. It takes incomplete user queries and suggests possible completions based on the most relevant stored queries.

### 4. Evaluation Metrics
When processing queries from the Cranfield dataset, the search engine calculates the following performance metrics:
- **Precision@k**
- **Recall@k**
- **F-score@k**
- **nDCG@k** (Normalized Discounted Cumulative Gain)
- **Mean Average Precision (MAP)**

These metrics help in evaluating the relevance and accuracy of the search results.

### 5. Pre-calculated Matrices
The pre-calculated similarity matrix `term_term.npy` is crucial for the CRN model, as it boosts the performance by considering relationships between terms across documents.
