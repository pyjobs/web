# -*- coding: utf-8 -*-
from tg import config


def compute_index_name(desired_name):
    es_project_name = config.get('elasticsearch.project_name')
    es_instance_name = config.get('elasticsearch.instance_name')

    index_prefix = '%s_%s' % (es_project_name, es_instance_name)

    # This test prevents infinite length indexes. Indeed, elasticsearch_dsl
    # makes heavy uses of meta programming, and when you try to modify the
    # index name in document_cls._doc_type.index to use a custom generated index
    # name (and not static one), through the use of a callback, or a regular
    # function, it won't work. Therefore, we are forced to change the index name
    # dynamically (during the object object instantiation, in its constructor),
    # thus calling this function in the constructor. BUT, the index name for
    # a document is stored in a meta class which is shared by EVERY documents of
    # the same type. And, when dynamically setting the index name to a new
    # custom computed value (by say adding a prefix to the original name, like
    # we do in this function), it would behave this way:
    #
    #     - first instantiation:
    #         - _doc_type.index = foo
    #         - constructor: prepend bar_ to foo
    #         - result: _doc_type.index = bar_foo
    #     - second instantiation:
    #         - _doc_type.index = bar_foo
    #         - constructor: prepend bar_ to bar_foo
    #         - result: _doc_type.index = bar_bar_foo
    #              .
    #              .
    #              .
    #              .
    #     - nth instantiation:
    #         - _doc_type.index = bar_...bar_foo (with nth - 1 bar)
    #         - constructor: prepend bar_ to bar_...bar_foo (with nth - 1 bar)
    #         - result: _doc_type.index = bar_...bar_foo (with nth bar)
    #
    # Which would cause a lot of issues as you might have guessed, (such as
    # creating n index for the same document, until the size of the index was
    # too big for Elasticsearch, but the damages would already be consequent).
    # I don't know of any other way to fix this properly, until we can use
    # functions or callbacks in the Meta class for an elasticsearch_dsl.DocType
    # class to dynamically compute indexes name at run time. At least this
    # is a working method.
    if index_prefix in desired_name:
        return desired_name

    return '%s_%s' % (index_prefix, desired_name)
