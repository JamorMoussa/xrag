"""Inspect MarkdownNodeParser output for a paper excerpt.

Run without changing the project's dependencies:
    uv run --no-project --with llama-index-core python examples/markdown_nodes.py

MarkdownNodeParser creates TextNode objects, splitting at Markdown headings.
Tables, horizontal rules, bold text, and figure captions remain ordinary text
inside those nodes; this parser does not create special table or figure nodes.
"""

from llama_index.core import Document
from llama_index.core.node_parser import MarkdownNodeParser, SentenceSplitter
from pprint import pprint

MARKDOWN = """Table 1: Explaining neurons by comparing their weights with sums of token embeddings.

---

| Neuron | Vector |  |  |
|---|---|---|---|
| 0-12 | CNN + | Cold + | NBC + . . . + lying + . . . + TRUMP + . . . |
| 0-186 | remarked + | commented + | complained + |

0-192 being + Being + Having + be + Be + 0-205 selections + eclectic + selection + 0-247 resulted + based + Given + highlighted + . . .

Cos. Sim. 0.61

said + . . . 0.63

beings + . . . 0.65 assortment + . . . 0.58

0.62

---

**0-809** bring, bringing, ... >|

**7-1321 11-2172 to**

— —»

**0-3028** relating, relation, ... **to** >

Figure 2: Circuit discovery using similarities between Wout and Win vectors based on greedily obtained concept vectors. The two neurons in the first layer each focus on a set of tokens. The neuron 7-1321 seems to model a union of those sets, whose output is similar to the input of the depicted neuron in the last layer and the to unembedding. The last one has many inbound connections to previous outputs and seems to boost the concept of the to vector.

### 3.2 Processing of Concepts

Earlier experiments indicated that some neurons in GPT-2 focus on very specific tokens, such as the. Assuming that MLP blocks perform boolean operations on concept vectors and that word embeddings are concept vectors, we would expect some neurons to have weights representing either a single word vector or a composite vector made of several word vectors (e.g., the sum of all word embeddings that are variations of the). To test this hypothesis, we conducted experiments. Specifically, we aimed to determine if some neural weights could be explained by simple bundled vectors that are merely sums of word embeddings. For each possible input vector (word embedding), we compiled a list of the most similar neurons. That is, we looked for neurons in the first feedforward layer of the MLP block whose input weights have a reasonably high dot product with the centered candidate vector. For each neuron and its list of candidates, we then greedily assembled the bundled vector by including those vectors (ranked by similarity) that lead to an increase of the cosine similarity between the bundled vector and the respective neural weights. We discarded vectors with a cosine similarity of less than 0.05 with the neural weight vector. We also discarded those with less than 0.1 if they did not significantly increase the overall cosine similarity by more than 0.04. These thresholds represent hyperparameters and were conservatively chosen to obtain sets of highly relevant vectors. We enforced a minimal similarity to the target vector and only considered unweighted sums since any vector can be trivially represented by a weighted sum of sufficiently many nearly orthogonal vectors. With this simple approach, we achieve a similarity of 0.5 or higher for more than 80% of the neurons in the first layer, and at least 0.3 for more than 95% (this includes attributions to attention heads we discuss in the next section). For instance, our greedily obtained vector for neuron 1844 in the first layer has a high cosine similarity of 0.69 with the actual weights of that neuron. The list contains many first names, most of them male sounding (' Chris', ' Kevin', ' Jeff') with some exceptions (' Rebecca'). Neuronpedia explains this as first names of people. Neuron 20 (similarity of 0.73) focuses on tokens somehow semantically related to 'maintaining', including 'Nevertheless' and 'Storage' (Neuronpedia says verbs related to maintaining or keeping something). Table 1 lists more examples. It is important to note that we inferred these neuron explanations directly from the weights rather than through activation observations and correlations, or by training an autoencoder or probing classifier.

### 3.3 Processing Circuits

Using the analogy of concept vectors and matrix bindings, we would expect that the MLP blocks perform (boolean) functions on concept vectors sourced from either the token embeddings, previous results from MLP blocks (information from computations), or attention blocks (information from other tokens). The results are then written back to the stream via matrix binding. The sum of
"""


def main() -> None:
    document = Document(
        text=MARKDOWN,
        metadata={"source": "paper_excerpt", "page": 1},
    )
    parser = MarkdownNodeParser.from_defaults(
        include_metadata=True,
        include_prev_next_rel=True,
    )

    sections = parser.get_nodes_from_documents([document])

    splitter = SentenceSplitter(
        chunk_size=512,
        chunk_overlap=50,
    )
    nodes = splitter(sections)

    pprint([node.model_dump(mode="json") for node in nodes])

if __name__ == "__main__":
    main()
