# Problem Set 20: Pagerank

This task revolves around implementing a basic version of the PageRank algorithm, the cornerstone of Google's initial search approach. Three functions need implementation:

1. transition_model: Given a current page, return a probability distribution for the next page visit.

2. sample_pagerank: Determine PageRank values for each page by sampling n pages using the transition model, beginning with a random page.

3. iterate_pagerank: Compute PageRank values for each page through iterative updates until convergence.