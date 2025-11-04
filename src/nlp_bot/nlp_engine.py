import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.common.exceptions import CorpusEmptyError, InvalidQueryError
from src.common.logger import get_logger

logger = get_logger(__name__)


@dataclass
class CorpusEntry:
    question: str
    answer: str
    category: Optional[str] = None


class NLPEngine:
    def __init__(self, corpus: List[CorpusEntry], similarity_threshold: float = 0.3):
        if not corpus:
            raise CorpusEmptyError("Corpus cannot be empty")
        
        self.corpus = corpus
        self.similarity_threshold = similarity_threshold
        
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            strip_accents='unicode',
            analyzer='word',
            ngram_range=(1, 2)
        )
        
        corpus_questions = [entry.question for entry in corpus]
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus_questions)
        
        logger.info(f"NLP Engine initialized with {len(corpus)} corpus entries")
    
    def find_best_match(self, query: str) -> Tuple[Optional[str], float]:
        if not query or not query.strip():
            raise InvalidQueryError("Query cannot be empty")
        
        try:
            query_vector = self.vectorizer.transform([query])
            similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]
            
            best_idx = np.argmax(similarities)
            best_score = similarities[best_idx]
            
            logger.debug(f"Query: '{query}' | Best match score: {best_score:.3f}")
            
            if best_score >= self.similarity_threshold:
                best_answer = self.corpus[best_idx].answer
                return best_answer, best_score
            
            return None, best_score
            
        except Exception as e:
            logger.error(f"Error finding match for query '{query}': {e}")
            raise
    
    def get_fallback_response(self) -> str:
        return (
            "Lo siento, no entendí tu pregunta. "
            "¿Podrías reformularla o preguntar sobre nuestros servicios, "
            "horarios o ubicación?"
        )


def load_corpus_from_json(file_path: Path) -> List[CorpusEntry]:
    if not file_path.exists():
        raise FileNotFoundError(f"Corpus file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    corpus = [
        CorpusEntry(
            question=qa['question'],
            answer=qa['answer'],
            category=qa.get('category')
        )
        for qa in data['qa_pairs']
    ]
    
    logger.info(f"Loaded {len(corpus)} entries from corpus")
    return corpus
