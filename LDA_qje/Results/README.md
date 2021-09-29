*Results from LDA viz*

**Topic modeling results**

Topic modeling results are obtained on a 2000-statements, 1000-features, 10-components sample.
We chose to keep either 5 or 10 topics.

`_fulldoc` : calculated on a full dictionary instead of a statement sample. 


**Extracting time**


For a full dictionary (12678 statements):
- NMF Frobenius : 19.231s
- NMF Kullback Leibler : 71.219s
- LDA : 120.139s

For a sample dictionary : 
- NMF Frobenius : 0.051s
- NMF Kullback Leibler : 0.436s
- LDA : 2.373s
