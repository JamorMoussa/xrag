# XRAG - eXtended RAG


## References: 
- [The Complete Guide to Hybrid Search in RAG (BM25 + Embeddings + Reranker)](https://www.youtube.com/watch?v=XvKiTfd6Xvo)
```mermaid
graph LR
    Q[Query] --> BM25[BM25<br/>bm25s]
    Q --> DENSE[Dense<br/>text-embedding-3-small]
    BM25 --> RRF[Reciprocal<br/>Rank Fusion]
    DENSE --> RRF
    RRF --> RR[Cross-encoder<br/>rerank-v4.0-fast]
    RR --> TOP[Top-10]
```

- [FiQA-2018, a financial Q&A benchmark](https://sites.google.com/view/fiqa): I guess this would be a good benchmark to evaluate the XRAG system.

- [EmbeddingGemma 2](https://huggingface.co/google/embeddinggemma-2): is an open multimodal embedding model built by Google DeepMind which maps text (incl. code), images, video, and audio inputs a single, unified 768-dimensional vector space. This is quite useful for building multimodal RAG systems and would be a nice feature to add to XRAG.
