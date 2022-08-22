"""
Contains the methods to create the search results
From the list of query terms, these should return the following list
of recipes, in order:
    - all the recipes whose list of ingredients contain all query terms
    - all the recipes whose list of ingredients contains more than
      one query term
    - all the recipes with one of the query terms in the recipe name
    - all the recipes whose list of ingredients contains one query term
"""
# Thanks to https://www.cyberhavenprogramming.com/blog/2019/4/23/django-q-object-how-make-many-complex-multiple-and-dynamic-queries-python-reduce-function-functools-or-operator-and-requestget-search-fields-parameters/
import operator
import re

from functools import reduce
from django.db.models import Q

from recipes.models import Recipes


def get_results(query):
    """
    The algorithm used to produce the set of recipes from the query term
    :param query: the user query
    :return: a query set of the recipes matching the query terms
    """
    normalized_queries = [re.sub(r'[^\w]', "", i) for i in query.split()]
    all_ingredients = reduce(operator.and_, (
        Q(ingredients__name__icontains=term) for term in normalized_queries
    ))
    multiple_lookups = reduce(operator.or_, (
        Q(ingredients__name__icontains=term) |
        Q(name__icontains=term) for term in normalized_queries
    ))
    final_query = reduce(operator.or_, (all_ingredients, multiple_lookups))
    return Recipes.objects.select_related('category').filter(final_query).\
        distinct()
