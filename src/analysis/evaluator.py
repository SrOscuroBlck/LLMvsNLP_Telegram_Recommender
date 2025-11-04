from dataclasses import dataclass
from typing import List
import json
from pathlib import Path

from src.common.logger import get_logger

logger = get_logger(__name__)


@dataclass
class BotResponse:
    query: str
    response: str
    response_time: float
    bot_type: str


@dataclass
class ComparisonMetrics:
    nlp_avg_response_time: float
    llm_avg_response_time: float
    total_queries: int
    
    def to_dict(self) -> dict:
        return {
            "nlp_avg_response_time_ms": round(self.nlp_avg_response_time * 1000, 2),
            "llm_avg_response_time_ms": round(self.llm_avg_response_time * 1000, 2),
            "total_queries": self.total_queries,
            "speed_comparison": "NLP is faster" if self.nlp_avg_response_time < self.llm_avg_response_time else "LLM is faster"
        }


class Evaluator:
    def __init__(self):
        self.nlp_responses: List[BotResponse] = []
        self.llm_responses: List[BotResponse] = []
        logger.info("Evaluator initialized")
    
    def add_nlp_response(self, query: str, response: str, response_time: float):
        self.nlp_responses.append(
            BotResponse(
                query=query,
                response=response,
                response_time=response_time,
                bot_type="NLP"
            )
        )
    
    def add_llm_response(self, query: str, response: str, response_time: float):
        self.llm_responses.append(
            BotResponse(
                query=query,
                response=response,
                response_time=response_time,
                bot_type="LLM"
            )
        )
    
    def calculate_metrics(self) -> ComparisonMetrics:
        if not self.nlp_responses or not self.llm_responses:
            logger.warning("Not enough data for comparison")
            return None
        
        nlp_avg = sum(r.response_time for r in self.nlp_responses) / len(self.nlp_responses)
        llm_avg = sum(r.response_time for r in self.llm_responses) / len(self.llm_responses)
        
        metrics = ComparisonMetrics(
            nlp_avg_response_time=nlp_avg,
            llm_avg_response_time=llm_avg,
            total_queries=min(len(self.nlp_responses), len(self.llm_responses))
        )
        
        logger.info("Calculated comparison metrics")
        return metrics
    
    def save_results(self, output_path: Path):
        results = {
            "nlp_responses": [
                {
                    "query": r.query,
                    "response": r.response,
                    "response_time_ms": round(r.response_time * 1000, 2)
                }
                for r in self.nlp_responses
            ],
            "llm_responses": [
                {
                    "query": r.query,
                    "response": r.response,
                    "response_time_ms": round(r.response_time * 1000, 2)
                }
                for r in self.llm_responses
            ],
            "metrics": self.calculate_metrics().to_dict() if self.calculate_metrics() else {}
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Results saved to {output_path}")
