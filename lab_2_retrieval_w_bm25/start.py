"""
Laboratory Work #2 starter
"""
# pylint:disable=too-many-locals, unused-argument, unused-variable, too-many-branches, too-many-statements, duplicate-code
import lab_2_retrieval_w_bm25.main as m


def main() -> None:
    """
    Launches an implementation
    """
    paths_to_texts = [
        "assets/fairytale_1.txt",
        "assets/fairytale_2.txt",
        "assets/fairytale_3.txt",
        "assets/fairytale_4.txt",
        "assets/fairytale_5.txt",
        "assets/fairytale_6.txt",
        "assets/fairytale_7.txt",
        "assets/fairytale_8.txt",
        "assets/fairytale_9.txt",
        "assets/fairytale_10.txt",
    ]
    query, file_path = 'Which fairy tale has Fairy Queen?', 'assets/metrics.json'
    alpha, k1, b, avg_doc_len = 0.2, 1.5, 0.75, 0.0
    tf_idf_list, bm25_list, optimized_bm25_list = [], [], []
    documents, clear_documents = [], []

    for path in paths_to_texts:
        with open(path, "r", encoding="utf-8") as file:
            documents.append(file.read())
    with open("assets/stopwords.txt", "r", encoding="utf-8") as file:
        stopwords = file.read().split("\n")

    for document in documents:
        if document is not None:
            avg_doc_len += len(document)
            tokenized_document = m.tokenize(document)
            if tokenized_document is not None:
                tokenized_document = m.remove_stopwords(tokenized_document, stopwords)
            if tokenized_document is not None:
                clear_documents.append(tokenized_document)

    avg_doc_len /= len(clear_documents)

    vocab = m.build_vocabulary(clear_documents)
    if vocab is None:
        return
    idf_dict = m.calculate_idf(vocab, clear_documents)
    if idf_dict is None:
        return

    for clear_document in clear_documents:
        if clear_document is None:
            return
        doc_len = len(clear_document)
        tf_dict = m.calculate_tf(vocab, clear_document)
        if tf_dict is not None:
            tf_idf = m.calculate_tf_idf(tf_dict, idf_dict)
            if tf_idf is not None:
                tf_idf_list.append(tf_idf)
        bm25 = m.calculate_bm25(vocab, clear_document, idf_dict, k1, b, avg_doc_len, doc_len)
        if bm25 is not None:
            bm25_list.append(bm25)
        optimized_bm25 = m.calculate_bm25_with_cutoff(vocab, clear_document, idf_dict,
                                                      alpha, k1, b, avg_doc_len, doc_len)
        if optimized_bm25 is not None:
            optimized_bm25_list.append(optimized_bm25)

    m.save_index(optimized_bm25_list, file_path)
    loaded_index = m.load_index(file_path)
    if loaded_index is None:
        return

    ranked_index = m.rank_documents(loaded_index, query, stopwords)
    ranked_tf_idf = m.rank_documents(tf_idf_list, query, stopwords)
    ranked_bm25 = m.rank_documents(bm25_list, query, stopwords)
    if ranked_index is None or ranked_tf_idf is None or ranked_bm25 is None:
        return

    golden_rank = [i[0] for i in ranked_index]
    tf_idf_spearman = m.calculate_spearman([i[0] for i in ranked_tf_idf], golden_rank)
    bm25_spearman = m.calculate_spearman([i[0] for i in ranked_bm25], golden_rank)

    result = (golden_rank, tf_idf_spearman, bm25_spearman)
    print(result)
    assert result, "Result is None"


if __name__ == "__main__":
    main()
