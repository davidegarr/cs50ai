import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    #initialize the probability dict
    probability_dict = {}

    #initialize the dict with all the pages in the corpus. base prob is 1-dampl/len(corp)
    for web_page in corpus:
        probability_dict[web_page] = round((1-damping_factor)/len(corpus), 3)

    #for the pages within the page we are currently in, add extra prob
    for web_page in corpus:
        if web_page == page:
            for sub_page in corpus[page]:
                probability_dict[sub_page] += round(damping_factor/len(corpus[page]), 3)

    return probability_dict
  


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    #initialize the sampling dict
    sampled_dict = {}

    #fill the dict with the webs in the corpus. base sample is int 0.
    for web_page in corpus:
        sampled_dict[web_page] = 0
    
    #first sample is generated by choosing one page at random
    pages = list(corpus.keys())
    current_page = random.choice(pages)
    next_page = None
    
    #iterate n times
    i = 0
    while i < n:
        #Get the probability dict from transition model
        probability_dict = transition_model(corpus, current_page, damping_factor)

        # Get a list of the dictionary keys and values (weights)
        keys = list(probability_dict.keys())
        weights = list(probability_dict.values())

        # Choose a random key based on the weights
        next_page = random.choices(keys, weights)[0]
        sampled_dict[next_page] += 1

        #swap current and next page
        current_page = next_page
        next_page = None

        i += 1

    #normalize sampled_dict
    normalized_sampled_dict = {k: v/n for k, v in sampled_dict.items()}

    return normalized_sampled_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    #initialize dict
    initial_dict = {}
    N = len(corpus)
    for page in corpus:
        initial_dict[page] = 1/N
        
    # fill corpus if needed:
    updated_corpus = corpus
    for page in corpus:
        if len(corpus[page]) == 0:
            updated_corpus[page] = set(corpus.keys())


    
    #dictionary of linking pages. reads as "we can find link to key in set(values)"
    links_to_page = {}
    for page in updated_corpus:
        links_to_page[page] = set()
    
    for page in updated_corpus:
        for link in updated_corpus[page]:
            links_to_page[link].add(page)

    
    #iterate until diff < .001
    c = (1-damping_factor)/N

    while True:
        new_dict = {}
        for page in updated_corpus:
            new_dict[page] = (1-damping_factor) / N
            for link in links_to_page[page]:
                new_dict[page] += damping_factor * initial_dict[link]/len(updated_corpus[link])
        
        diff = sum(abs(new_dict[page] - initial_dict[page]) for page in updated_corpus)
        if diff < 0.001:
            break
        initial_dict = new_dict
    
    return new_dict


if __name__ == "__main__":
    main()
