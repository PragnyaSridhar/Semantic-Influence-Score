# Semantic-Influence-Score
On a network of influential papers obtained through vigorous filtering, topics were obtained via topic modelling. Semantic similarity between the papers and their derivative works was computed using their references. A strong semantic similarity (in the range of 0.9 to 24) was observed between these articles. Together with the reference intersection, semantic topic similarity gives us a credible corpora of articles to study scholarly influence of base papers on their 'derivative works network'. These networks, which we term as Semantic Influence Networks, and not the traditional citation networks, are the building blocks for analyzing and quantifying article influence, SIS, via a novel application of the Heat Diffusion Model for the influence score. Our final corpora, carefully filtered, is a sample of 1258 articles with 307696 total citations, an average citation of 244, and median citation of 151. The maximum citation of one article stands at 12871 and the minimum at 100 (due to applied filter).

## Set up
Download Aminer.json(DBLP-Citation-network V12) from https://www.aminer.cn/citation

## File Directory
Directories have been named in order of tasks carried out
1_Filter dataset
  filter.ipynb - read Aminer.json line by line using python generator and filter required rows
  
2_Document tagging
  tagging.ipynb - use 'fields of study' to tag articles with classes Machine Learning, Metaheuristic Optimization and Deep Learning using SciBERT
  dbscan.ipynb - use dbscan clustering to hierarchically tag articles
  tagged_Aminer_dataset.csv - filtered Aminer dataset with tags
  test_ijcnn.csv - used to test SciBERT model as IJCNN predominantly accepts ML papers only
  
3_Make network
  bib_downloader.py - webscraping using selenium to download derivative works bib files from connected papers
  bibtex_parser.ipynb - parse bib file to get names and IDs of derivative works
  make_dataset.ipynb - add derivative works IDs to main dataset
  
4_Influence score
  adj_mat.zip - contains csv files with adjacency matrices of each base paper separately
  initial_heats.csv - initial heat assigned to each base paper (length of knowledge chain)
  make_adjmat.ipynb - make adjacency matrices to compute influence score
  Result.csv - contains heat values/influence scores assigned to each node in adjacency matrices
  
5_Similarity score
  add2dataset.ipynb - add obtained similarity scores to final dataset
  refint_L0-1.ipynb - analyse and store reference intersections between nodes of level 0 and 1
  refint_L1-2.ipynb - analyse and store reference intersections between nodes of level 1 and 2
  Similarity_measure.ipynb - compute similarity measure
  Similarity.csv - contains similarity scores between node pairs
  sparse_mat.ipynb - make sparse matrix to compute similarity scores
  ssAPI.py - make semantic scholar API calls and obtain references of all papers in network

6_SIS
  Normalize_venue_prestige.ipynb - normalize H5 scores of venues obtained
  semantic_score.ipynb - compute semantic score using influence and similarity scores
  venue_prestige.csv - contains the h5 and normalized h5 indices of venues of base papers
  venue_prestige.ipynb - make dataset containing details about venue - name, type(journal/conference), h5 index

7_Result analysis
  regression&distribution.ipynb - check if regression between SIS and raw citation possible, find distribution SIS belongs to

final_dataset.csv - complete dataset with tags, complete network details, similarity, influence and semantic scores

## Results
- SIS is not lineraly dependent on Raw citations (Best fit line does not exist)
- Correlation between SIS and raw citation is scant (Confidence interval of Pearson correlation coefficient)
- SIS does NOT follow Pareto and Power Law distribution (KS test)
