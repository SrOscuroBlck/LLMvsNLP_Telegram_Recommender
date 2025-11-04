#!/usr/bin/env python3
"""
Direct function testing for NLP and LLM engines
Tests both bots without Telegram, measuring accuracy and performance
"""

import json
import time
import asyncio
from pathlib import Path
from datetime import datetime

from src.nlp_bot.nlp_engine import NLPEngine, load_corpus_from_json
from src.llm_bot.openai_client import OpenAIClient, load_system_prompt
from src.common.config import load_nlp_bot_config, load_llm_bot_config
from src.analysis.metrics_calculator import MetricsCalculator, QueryResult
from src.common.logger import setup_logger

logger = setup_logger(__name__)


def load_test_queries():
    # Go up to project root, then into tests
    project_root = Path(__file__).parent.parent
    test_file = project_root / "tests" / "test_queries.json"
    with open(test_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['test_queries']


def test_nlp_bot(queries):
    print("\n" + "="*80)
    print("Testing NLP Bot (TF-IDF)")
    print("="*80)
    
    # Initialize NLP bot
    project_root = Path(__file__).parent.parent
    corpus_path = project_root / "data" / "corpus" / "qa_pairs.json"
    corpus = load_corpus_from_json(str(corpus_path))
    nlp_config = load_nlp_bot_config()
    engine = NLPEngine(corpus, similarity_threshold=nlp_config.similarity_threshold)
    
    test_queries = load_test_queries()
    calculator = MetricsCalculator()
    
    for query_data in test_queries:
        query_text = query_data['query']
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Query {query_data['id']}: {query_text}")
        logger.info(f"Category: {query_data['category']} | Difficulty: {query_data['difficulty']}")
        logger.info(f"Expected keywords: {', '.join(query_data['expected_keywords'])}")
        
        start_time = time.time()
        answer, score = engine.find_best_match(query_text)
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        if answer:
            response_text = answer
            logger.info(f"✓ Matched with score: {score:.3f}")
        else:
            response_text = engine.get_fallback_response()
            logger.info(f"✗ No match found (best score: {score:.3f})")
        
        logger.info(f"Response time: {response_time_ms:.2f}ms")
        logger.info(f"Response: {response_text[:100]}...")
        
        result = QueryResult(
            query_id=query_data['id'],
            query_text=query_text,
            response_text=response_text,
            response_time_ms=response_time_ms,
            bot_type="NLP",
            timestamp=datetime.utcnow().isoformat(),
            keywords_expected=query_data['expected_keywords'],
            category=query_data['category'],
            difficulty=query_data['difficulty']
        )
        
        calculator.add_result(result)
        calculator.update_result_metrics(result)
        
        keywords_found_str = ', '.join(result.keywords_found) if result.keywords_found else "None"
        logger.info(f"Keywords found: {keywords_found_str}")
        logger.info(f"Relevance score: {result.relevance_score:.2f}")
    
    return calculator


async def test_llm_engine():
    logger.info("\n" + "=" * 80)
    logger.info("Testing LLM Engine")
    logger.info("=" * 80)
    
    llm_config = load_llm_bot_config()
    client = OpenAIClient(llm_config)
    
    project_root = Path(__file__).parent.parent
    prompt_path = project_root / "data" / "prompts" / "system_prompt.txt"
    system_prompt = load_system_prompt(prompt_path)
    
    test_queries = load_test_queries()
    calculator = MetricsCalculator()
    
    for query_data in test_queries:
        query_text = query_data['query']
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Query {query_data['id']}: {query_text}")
        logger.info(f"Category: {query_data['category']} | Difficulty: {query_data['difficulty']}")
        logger.info(f"Expected keywords: {', '.join(query_data['expected_keywords'])}")
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query_text}
        ]
        
        try:
            start_time = time.time()
            response_text = await client.get_completion(messages)
            end_time = time.time()
            
            response_time_ms = (end_time - start_time) * 1000
            
            logger.info(f"✓ Got response")
            logger.info(f"Response time: {response_time_ms:.2f}ms")
            logger.info(f"Response: {response_text[:100]}...")
            
        except Exception as e:
            logger.error(f"✗ Error: {e}")
            response_text = f"Error: {str(e)}"
            response_time_ms = 0.0
        
        result = QueryResult(
            query_id=query_data['id'],
            query_text=query_text,
            response_text=response_text,
            response_time_ms=response_time_ms,
            bot_type="LLM",
            timestamp=datetime.utcnow().isoformat(),
            keywords_expected=query_data['expected_keywords'],
            category=query_data['category'],
            difficulty=query_data['difficulty']
        )
        
        calculator.add_result(result)
        calculator.update_result_metrics(result)
        
        keywords_found_str = ', '.join(result.keywords_found) if result.keywords_found else "None"
        logger.info(f"Keywords found: {keywords_found_str}")
        logger.info(f"Relevance score: {result.relevance_score:.2f}")
        
        await asyncio.sleep(1)
    
    return calculator


def print_summary(nlp_calculator: MetricsCalculator, llm_calculator: MetricsCalculator):
    logger.info("\n" + "=" * 80)
    logger.info("SUMMARY - NLP vs LLM Comparison")
    logger.info("=" * 80)
    
    nlp_metrics = nlp_calculator.calculate_bot_metrics("NLP")
    llm_metrics = llm_calculator.calculate_bot_metrics("LLM")
    
    logger.info("\n--- NLP Bot Results ---")
    logger.info(f"Total queries: {nlp_metrics.total_queries}")
    logger.info(f"Avg response time: {nlp_metrics.avg_response_time_ms:.2f}ms")
    logger.info(f"Min/Max response time: {nlp_metrics.min_response_time_ms:.2f}ms / {nlp_metrics.max_response_time_ms:.2f}ms")
    logger.info(f"Avg relevance score: {nlp_metrics.avg_relevance_score:.3f}")
    logger.info(f"Keyword match rate: {nlp_metrics.keyword_match_rate:.3f}")
    logger.info(f"Keywords found: {nlp_metrics.total_keywords_found}/{nlp_metrics.total_keywords_expected}")
    
    logger.info("\nAccuracy by category:")
    for category, score in sorted(nlp_metrics.accuracy_by_category.items()):
        logger.info(f"  {category}: {score:.3f}")
    
    logger.info("\nAccuracy by difficulty:")
    for difficulty, score in sorted(nlp_metrics.accuracy_by_difficulty.items()):
        logger.info(f"  {difficulty}: {score:.3f}")
    
    logger.info("\n--- LLM Bot Results ---")
    logger.info(f"Total queries: {llm_metrics.total_queries}")
    logger.info(f"Avg response time: {llm_metrics.avg_response_time_ms:.2f}ms")
    logger.info(f"Min/Max response time: {llm_metrics.min_response_time_ms:.2f}ms / {llm_metrics.max_response_time_ms:.2f}ms")
    logger.info(f"Avg relevance score: {llm_metrics.avg_relevance_score:.3f}")
    logger.info(f"Keyword match rate: {llm_metrics.keyword_match_rate:.3f}")
    logger.info(f"Keywords found: {llm_metrics.total_keywords_found}/{llm_metrics.total_keywords_expected}")
    
    logger.info("\nAccuracy by category:")
    for category, score in sorted(llm_metrics.accuracy_by_category.items()):
        logger.info(f"  {category}: {score:.3f}")
    
    logger.info("\nAccuracy by difficulty:")
    for difficulty, score in sorted(llm_metrics.accuracy_by_difficulty.items()):
        logger.info(f"  {difficulty}: {score:.3f}")
    
    logger.info("\n--- Comparison ---")
    logger.info(f"Response time: NLP {nlp_metrics.avg_response_time_ms:.2f}ms vs LLM {llm_metrics.avg_response_time_ms:.2f}ms")
    logger.info(f"  → NLP is {llm_metrics.avg_response_time_ms / nlp_metrics.avg_response_time_ms:.1f}x faster")
    
    logger.info(f"\nRelevance: NLP {nlp_metrics.avg_relevance_score:.3f} vs LLM {llm_metrics.avg_relevance_score:.3f}")
    improvement = ((llm_metrics.avg_relevance_score - nlp_metrics.avg_relevance_score) / nlp_metrics.avg_relevance_score * 100) if nlp_metrics.avg_relevance_score > 0 else 0
    logger.info(f"  → LLM is {improvement:+.1f}% more relevant")
    
    logger.info(f"\nKeyword match: NLP {nlp_metrics.keyword_match_rate:.3f} vs LLM {llm_metrics.keyword_match_rate:.3f}")


async def main():
    logger.info("Starting direct function tests...")
    logger.info(f"Test time: {datetime.utcnow().isoformat()}")
    
    project_root = Path(__file__).parent.parent
    results_dir = project_root / "results"
    results_dir.mkdir(exist_ok=True)
    
    # Load test queries
    test_queries = load_test_queries()
    
    nlp_calculator = test_nlp_bot(test_queries)
    
    llm_calculator = await test_llm_engine()
    
    combined_calculator = MetricsCalculator()
    combined_calculator.results = nlp_calculator.results + llm_calculator.results
    
    print_summary(nlp_calculator, llm_calculator)
    
    nlp_calculator.save_results_to_json(results_dir / "nlp_results.json")
    llm_calculator.save_results_to_json(results_dir / "llm_results.json")
    combined_calculator.save_results_to_json(results_dir / "all_results.json")
    combined_calculator.save_comparison_report(results_dir / "comparison_report.json")
    
    logger.info("\n" + "=" * 80)
    logger.info("Results saved to results/ directory")
    logger.info("  - nlp_results.json")
    logger.info("  - llm_results.json")
    logger.info("  - all_results.json")
    logger.info("  - comparison_report.json")
    logger.info("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
