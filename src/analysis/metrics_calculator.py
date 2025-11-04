import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from src.common.logger import get_logger

logger = get_logger(__name__)


@dataclass
class QueryResult:
    query_id: int
    query_text: str
    response_text: str
    response_time_ms: float
    bot_type: str
    timestamp: str
    keywords_found: List[str] = field(default_factory=list)
    keywords_expected: List[str] = field(default_factory=list)
    relevance_score: float = 0.0
    category: str = ""
    difficulty: str = ""


@dataclass
class BotMetrics:
    bot_type: str
    total_queries: int
    avg_response_time_ms: float
    min_response_time_ms: float
    max_response_time_ms: float
    avg_relevance_score: float
    accuracy_by_category: Dict[str, float]
    accuracy_by_difficulty: Dict[str, float]
    keyword_match_rate: float
    total_keywords_found: int
    total_keywords_expected: int


class MetricsCalculator:
    def __init__(self):
        self.results: List[QueryResult] = []
        logger.info("Metrics Calculator initialized")
    
    def add_result(self, result: QueryResult):
        self.results.append(result)
        logger.debug(f"Added result for query {result.query_id}")
    
    def calculate_relevance_score(self, result: QueryResult) -> float:
        if not result.keywords_expected:
            return 1.0
        
        keywords_found_count = len(result.keywords_found)
        keywords_expected_count = len(result.keywords_expected)
        
        score = keywords_found_count / keywords_expected_count if keywords_expected_count > 0 else 0.0
        return min(score, 1.0)
    
    def calculate_keyword_matches(self, response: str, expected_keywords: List[str]) -> List[str]:
        response_lower = response.lower()
        found = []
        
        for keyword in expected_keywords:
            if keyword.lower() in response_lower:
                found.append(keyword)
        
        return found
    
    def update_result_metrics(self, result: QueryResult):
        result.keywords_found = self.calculate_keyword_matches(
            result.response_text,
            result.keywords_expected
        )
        result.relevance_score = self.calculate_relevance_score(result)
    
    def calculate_bot_metrics(self, bot_type: str) -> BotMetrics:
        bot_results = [r for r in self.results if r.bot_type == bot_type]
        
        if not bot_results:
            return BotMetrics(
                bot_type=bot_type,
                total_queries=0,
                avg_response_time_ms=0.0,
                min_response_time_ms=0.0,
                max_response_time_ms=0.0,
                avg_relevance_score=0.0,
                accuracy_by_category={},
                accuracy_by_difficulty={},
                keyword_match_rate=0.0,
                total_keywords_found=0,
                total_keywords_expected=0
            )
        
        response_times = [r.response_time_ms for r in bot_results]
        relevance_scores = [r.relevance_score for r in bot_results]
        
        accuracy_by_category = self._calculate_accuracy_by_field(bot_results, "category")
        accuracy_by_difficulty = self._calculate_accuracy_by_field(bot_results, "difficulty")
        
        total_keywords_found = sum(len(r.keywords_found) for r in bot_results)
        total_keywords_expected = sum(len(r.keywords_expected) for r in bot_results)
        keyword_match_rate = total_keywords_found / total_keywords_expected if total_keywords_expected > 0 else 0.0
        
        return BotMetrics(
            bot_type=bot_type,
            total_queries=len(bot_results),
            avg_response_time_ms=sum(response_times) / len(response_times),
            min_response_time_ms=min(response_times),
            max_response_time_ms=max(response_times),
            avg_relevance_score=sum(relevance_scores) / len(relevance_scores),
            accuracy_by_category=accuracy_by_category,
            accuracy_by_difficulty=accuracy_by_difficulty,
            keyword_match_rate=keyword_match_rate,
            total_keywords_found=total_keywords_found,
            total_keywords_expected=total_keywords_expected
        )
    
    def _calculate_accuracy_by_field(self, results: List[QueryResult], field: str) -> Dict[str, float]:
        field_groups = {}
        
        for result in results:
            field_value = getattr(result, field, "unknown")
            if field_value not in field_groups:
                field_groups[field_value] = []
            field_groups[field_value].append(result.relevance_score)
        
        accuracy = {}
        for field_value, scores in field_groups.items():
            accuracy[field_value] = sum(scores) / len(scores)
        
        return accuracy
    
    def generate_comparison_report(self) -> Dict[str, Any]:
        nlp_metrics = self.calculate_bot_metrics("NLP")
        llm_metrics = self.calculate_bot_metrics("LLM")
        
        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "total_queries": len(self.results),
            "nlp_bot": {
                "total_queries": nlp_metrics.total_queries,
                "avg_response_time_ms": round(nlp_metrics.avg_response_time_ms, 2),
                "min_response_time_ms": round(nlp_metrics.min_response_time_ms, 2),
                "max_response_time_ms": round(nlp_metrics.max_response_time_ms, 2),
                "avg_relevance_score": round(nlp_metrics.avg_relevance_score, 3),
                "keyword_match_rate": round(nlp_metrics.keyword_match_rate, 3),
                "accuracy_by_category": {k: round(v, 3) for k, v in nlp_metrics.accuracy_by_category.items()},
                "accuracy_by_difficulty": {k: round(v, 3) for k, v in nlp_metrics.accuracy_by_difficulty.items()}
            },
            "llm_bot": {
                "total_queries": llm_metrics.total_queries,
                "avg_response_time_ms": round(llm_metrics.avg_response_time_ms, 2),
                "min_response_time_ms": round(llm_metrics.min_response_time_ms, 2),
                "max_response_time_ms": round(llm_metrics.max_response_time_ms, 2),
                "avg_relevance_score": round(llm_metrics.avg_relevance_score, 3),
                "keyword_match_rate": round(llm_metrics.keyword_match_rate, 3),
                "accuracy_by_category": {k: round(v, 3) for k, v in llm_metrics.accuracy_by_category.items()},
                "accuracy_by_difficulty": {k: round(v, 3) for k, v in llm_metrics.accuracy_by_difficulty.items()}
            },
            "comparison": {
                "response_time_improvement": self._calculate_improvement(
                    nlp_metrics.avg_response_time_ms,
                    llm_metrics.avg_response_time_ms,
                    lower_is_better=True
                ),
                "relevance_improvement": self._calculate_improvement(
                    nlp_metrics.avg_relevance_score,
                    llm_metrics.avg_relevance_score,
                    lower_is_better=False
                ),
                "keyword_match_improvement": self._calculate_improvement(
                    nlp_metrics.keyword_match_rate,
                    llm_metrics.keyword_match_rate,
                    lower_is_better=False
                )
            }
        }
        
        return report
    
    def _calculate_improvement(self, nlp_value: float, llm_value: float, lower_is_better: bool = False) -> str:
        if nlp_value == 0:
            return "N/A"
        
        if lower_is_better:
            improvement = ((nlp_value - llm_value) / nlp_value) * 100
        else:
            improvement = ((llm_value - nlp_value) / nlp_value) * 100
        
        return f"{improvement:+.2f}%"
    
    def save_results_to_json(self, file_path: Path):
        results_data = []
        
        for result in self.results:
            results_data.append({
                "query_id": result.query_id,
                "query_text": result.query_text,
                "response_text": result.response_text,
                "response_time_ms": result.response_time_ms,
                "bot_type": result.bot_type,
                "timestamp": result.timestamp,
                "keywords_found": result.keywords_found,
                "keywords_expected": result.keywords_expected,
                "relevance_score": result.relevance_score,
                "category": result.category,
                "difficulty": result.difficulty
            })
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(results_data)} results to {file_path}")
    
    def save_comparison_report(self, file_path: Path):
        report = self.generate_comparison_report()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved comparison report to {file_path}")
