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
    all_pages = list(corpus.keys())
    all_pages_len = len(all_pages)
    all_pages_prob = (1-damping_factor)/all_pages_len
    page_corpus = list(corpus[page])
    page_corpus_len = len(page_corpus)
    page_corpus_prob = damping_factor/page_corpus_len
    output = {}
    for page in all_pages:
        page_prob = all_pages_prob
        if page in page_corpus:
            page_prob += page_corpus_prob
        output[page] = page_prob
    return output


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    all_pages = list(corpus.keys())
    pages_count = {page: 0 for page in all_pages}
    first_prob = 1/len(all_pages)
    page = random.choices(all_pages, [first_prob]*len(all_pages))[0]
    pages_count[page] += 1
    i = 1
    while i < n:
        get_probs = transition_model(corpus, page, damping_factor)
        page = random.choices(list(get_probs.keys()),
                              list(get_probs.values()))[0]
        pages_count[page] += 1
        i += 1
    output = {}
    for page_name in pages_count.keys():
        output[page_name] = pages_count[page_name]/n
    return output


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    all_pages = list(corpus.keys())
    N = len(all_pages)
    first_prob = 1/len(all_pages)
    pages_pr = {page: first_prob for page in all_pages}
    links_to_pages = {page: [] for page in all_pages}
    for page, links_to_other_pages in corpus.items():
        for link in links_to_other_pages:
            links_to_pages[link].append(page)
    changed = True
    while changed:
        page_changed = False
        for page, links_to_page in links_to_pages.items():
            page_pr_first_part = (1-damping_factor)/N
            prop_of_links = 0
            for i in links_to_page:
                prop_of_links += pages_pr[i]/len(corpus[i])
            page_pr_second_part = damping_factor*prop_of_links
            new_page_pr = page_pr_first_part + page_pr_second_part
            if pages_pr[page]-0.01 > new_page_pr or new_page_pr > pages_pr[page]+0.01:
                page_changed = True
            pages_pr[page] = new_page_pr
        if not page_changed:
            changed = False
    return pages_pr


if __name__ == "__main__":
    main()
