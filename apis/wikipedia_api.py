# Import the wikipediaapi library
import wikipediaapi

# Create a Wikipedia object for the English language
wiki_wiki = wikipediaapi.Wikipedia('en')

def get_summary(movie_title):
    page_py = wiki_wiki.page(movie_title + '_(film)')
    print("Page - Summary: %s" % page_py.summary)
    return page_py

