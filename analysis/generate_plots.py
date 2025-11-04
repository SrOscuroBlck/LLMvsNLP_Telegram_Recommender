import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11


def load_results():
    # Go up to project root, then into results
    project_root = Path(__file__).parent.parent
    results_dir = project_root / "results"
    
    with open(results_dir / "comparison_report.json", 'r', encoding='utf-8') as f:
        comparison = json.load(f)
    
    nlp_results = comparison['nlp_bot']
    llm_results = comparison['llm_bot']
    
    with open(results_dir / "nlp_results.json", 'r', encoding='utf-8') as f:
        nlp_full = json.load(f)
        nlp_results['results'] = nlp_full
    
    with open(results_dir / "llm_results.json", 'r', encoding='utf-8') as f:
        llm_full = json.load(f)
        llm_results['results'] = llm_full
    
    nlp_results['total_keywords_found'] = sum(len(r.get('keywords_found', [])) for r in nlp_results['results'])
    nlp_results['total_keywords_expected'] = sum(len(r.get('expected_keywords', [])) for r in nlp_results['results'])
    
    llm_results['total_keywords_found'] = sum(len(r.get('keywords_found', [])) for r in llm_results['results'])
    llm_results['total_keywords_expected'] = sum(len(r.get('expected_keywords', [])) for r in llm_results['results'])
    
    return nlp_results, llm_results, comparison


def plot_response_time_comparison(nlp_results, llm_results):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = ['Average', 'Minimum', 'Maximum']
    nlp_times = [
        nlp_results['avg_response_time_ms'],
        nlp_results['min_response_time_ms'],
        nlp_results['max_response_time_ms']
    ]
    llm_times = [
        llm_results['avg_response_time_ms'],
        llm_results['min_response_time_ms'],
        llm_results['max_response_time_ms']
    ]
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, nlp_times, width, label='NLP Bot', color='#2ecc71', alpha=0.8)
    bars2 = ax.bar(x + width/2, llm_times, width, label='LLM Bot', color='#3498db', alpha=0.8)
    
    ax.set_ylabel('Response Time (ms)', fontweight='bold')
    ax.set_xlabel('Metric Type', fontweight='bold')
    ax.set_title('Response Time Comparison: NLP vs LLM', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}',
                   ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    # Save to project/results/ directory (one level up from analysis/)
    output_path = Path(__file__).parent.parent / 'results' / 'plot_response_time_comparison.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print("✓ Saved: plot_response_time_comparison.png")
    plt.close()


def plot_accuracy_by_category(nlp_results, llm_results):
    fig, ax = plt.subplots(figsize=(12, 7))
    
    categories = list(nlp_results['accuracy_by_category'].keys())
    nlp_accuracy = [nlp_results['accuracy_by_category'][cat] for cat in categories]
    llm_accuracy = [llm_results['accuracy_by_category'][cat] for cat in categories]
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, nlp_accuracy, width, label='NLP Bot', color='#2ecc71', alpha=0.8)
    bars2 = ax.bar(x + width/2, llm_accuracy, width, label='LLM Bot', color='#3498db', alpha=0.8)
    
    ax.set_ylabel('Accuracy Score', fontweight='bold')
    ax.set_xlabel('Query Category', fontweight='bold')
    ax.set_title('Accuracy by Query Category: NLP vs LLM', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.legend()
    ax.set_ylim(0, 1.1)
    ax.grid(True, alpha=0.3, axis='y')
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.2f}',
                       ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    output_path = Path(__file__).parent.parent / 'results' / 'plot_accuracy_by_category.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print("✓ Saved: plot_accuracy_by_category.png")
    plt.close()


def plot_accuracy_by_difficulty(nlp_results, llm_results):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    difficulties = list(nlp_results['accuracy_by_difficulty'].keys())
    nlp_accuracy = [nlp_results['accuracy_by_difficulty'][diff] for diff in difficulties]
    llm_accuracy = [llm_results['accuracy_by_difficulty'][diff] for diff in difficulties]
    
    x = np.arange(len(difficulties))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, nlp_accuracy, width, label='NLP Bot', color='#2ecc71', alpha=0.8)
    bars2 = ax.bar(x + width/2, llm_accuracy, width, label='LLM Bot', color='#3498db', alpha=0.8)
    
    ax.set_ylabel('Accuracy Score', fontweight='bold')
    ax.set_xlabel('Query Difficulty', fontweight='bold')
    ax.set_title('Accuracy by Query Difficulty: NLP vs LLM', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([d.capitalize() for d in difficulties])
    ax.legend()
    ax.set_ylim(0, 1.1)
    ax.grid(True, alpha=0.3, axis='y')
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}',
                   ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    output_path = Path(__file__).parent.parent / 'results' / 'plot_accuracy_by_difficulty.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print("✓ Saved: plot_accuracy_by_difficulty.png")
    plt.close()


def plot_overall_metrics(nlp_results, llm_results):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    metrics = ['Avg Relevance\nScore', 'Keyword\nMatch Rate']
    nlp_values = [
        nlp_results['avg_relevance_score'],
        nlp_results['keyword_match_rate']
    ]
    llm_values = [
        llm_results['avg_relevance_score'],
        llm_results['keyword_match_rate']
    ]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, nlp_values, width, label='NLP Bot', color='#2ecc71', alpha=0.8)
    bars2 = ax.bar(x + width/2, llm_values, width, label='LLM Bot', color='#3498db', alpha=0.8)
    
    ax.set_ylabel('Score', fontweight='bold')
    ax.set_xlabel('Metric', fontweight='bold')
    ax.set_title('Overall Performance Metrics: NLP vs LLM', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend()
    ax.set_ylim(0, 1.1)
    ax.grid(True, alpha=0.3, axis='y')
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    output_path = Path(__file__).parent.parent / 'results' / 'plot_overall_metrics.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print("✓ Saved: plot_overall_metrics.png")
    plt.close()


def plot_response_time_log_scale(nlp_results, llm_results):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    nlp_avg = nlp_results['avg_response_time_ms']
    llm_avg = llm_results['avg_response_time_ms']
    
    bots = ['NLP Bot', 'LLM Bot']
    times = [nlp_avg, llm_avg]
    colors = ['#2ecc71', '#3498db']
    
    bars = ax.bar(bots, times, color=colors, alpha=0.8, width=0.5)
    
    ax.set_ylabel('Response Time (ms) - Log Scale', fontweight='bold')
    ax.set_title('Average Response Time Comparison (Log Scale)', fontsize=14, fontweight='bold')
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3, which='both')
    
    for i, (bar, time) in enumerate(zip(bars, times)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{time:.2f} ms',
               ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    speed_factor = llm_avg / nlp_avg
    ax.text(0.5, 0.95, f'NLP is {speed_factor:.0f}x faster',
            transform=ax.transAxes, ha='center', va='top',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
            fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    output_path = Path(__file__).parent.parent / 'results' / 'plot_response_time_log_scale.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print("✓ Saved: plot_response_time_log_scale.png")
    plt.close()


def plot_success_failure_rate(nlp_results, llm_results):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    nlp_successful = sum(1 for result in nlp_results['results'] if result['relevance_score'] > 0.5)
    nlp_failed = nlp_results['total_queries'] - nlp_successful
    
    llm_successful = sum(1 for result in llm_results['results'] if result['relevance_score'] > 0.5)
    llm_failed = llm_results['total_queries'] - llm_successful
    
    nlp_data = [nlp_successful, nlp_failed]
    llm_data = [llm_successful, llm_failed]
    labels = ['Successful\n(>50% relevance)', 'Failed\n(≤50% relevance)']
    colors = ['#2ecc71', '#e74c3c']
    explode = (0.05, 0.05)
    
    ax1.pie(nlp_data, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=90, explode=explode, textprops={'fontsize': 10, 'fontweight': 'bold'})
    ax1.set_title('NLP Bot Success Rate', fontsize=13, fontweight='bold', pad=20)
    
    ax2.pie(llm_data, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=90, explode=explode, textprops={'fontsize': 10, 'fontweight': 'bold'})
    ax2.set_title('LLM Bot Success Rate', fontsize=13, fontweight='bold', pad=20)
    
    fig.suptitle('Query Success Rate Comparison (Relevance > 50%)', 
                 fontsize=15, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    output_path = Path(__file__).parent.parent / 'results' / 'plot_success_failure_rate.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print("✓ Saved: plot_success_failure_rate.png")
    plt.close()


def plot_keyword_coverage(nlp_results, llm_results):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    nlp_keywords = nlp_results['total_keywords_found']
    nlp_total = nlp_results['total_keywords_expected']
    llm_keywords = llm_results['total_keywords_found']
    llm_total = llm_results['total_keywords_expected']
    
    bots = ['NLP Bot', 'LLM Bot']
    found = [nlp_keywords, llm_keywords]
    missed = [nlp_total - nlp_keywords, llm_total - llm_keywords]
    
    x = np.arange(len(bots))
    width = 0.5
    
    bars1 = ax.bar(x, found, width, label='Keywords Found', color='#2ecc71', alpha=0.8)
    bars2 = ax.bar(x, missed, width, bottom=found, label='Keywords Missed', color='#e74c3c', alpha=0.8)
    
    ax.set_ylabel('Number of Keywords', fontweight='bold')
    ax.set_title('Keyword Coverage Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(bots)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    for i, (bot, f, m) in enumerate(zip(bots, found, missed)):
        total = f + m
        percentage = (f / total * 100) if total > 0 else 0
        ax.text(i, f + m + 1, f'{f}/{total}\n({percentage:.1f}%)',
               ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    output_path = Path(__file__).parent.parent / 'results' / 'plot_keyword_coverage.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print("✓ Saved: plot_keyword_coverage.png")
    plt.close()


def plot_category_heatmap(nlp_results, llm_results):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    categories = list(nlp_results['accuracy_by_category'].keys())
    nlp_accuracy = [nlp_results['accuracy_by_category'][cat] for cat in categories]
    llm_accuracy = [llm_results['accuracy_by_category'][cat] for cat in categories]
    
    nlp_data = np.array(nlp_accuracy).reshape(-1, 1)
    llm_data = np.array(llm_accuracy).reshape(-1, 1)
    
    im1 = ax1.imshow(nlp_data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    ax1.set_yticks(np.arange(len(categories)))
    ax1.set_yticklabels(categories)
    ax1.set_xticks([0])
    ax1.set_xticklabels(['NLP Bot'])
    ax1.set_title('NLP Bot Accuracy Heatmap', fontweight='bold', fontsize=13)
    
    for i, acc in enumerate(nlp_accuracy):
        text_color = 'white' if acc < 0.5 else 'black'
        ax1.text(0, i, f'{acc:.2f}', ha='center', va='center',
                color=text_color, fontweight='bold', fontsize=10)
    
    im2 = ax2.imshow(llm_data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    ax2.set_yticks(np.arange(len(categories)))
    ax2.set_yticklabels(categories)
    ax2.set_xticks([0])
    ax2.set_xticklabels(['LLM Bot'])
    ax2.set_title('LLM Bot Accuracy Heatmap', fontweight='bold', fontsize=13)
    
    for i, acc in enumerate(llm_accuracy):
        text_color = 'white' if acc < 0.5 else 'black'
        ax2.text(0, i, f'{acc:.2f}', ha='center', va='center',
                color=text_color, fontweight='bold', fontsize=10)
    
    fig.colorbar(im2, ax=[ax1, ax2], label='Accuracy Score', pad=0.02)
    fig.suptitle('Category-wise Accuracy Comparison', fontsize=15, fontweight='bold')
    
    plt.tight_layout()
    output_path = Path(__file__).parent.parent / 'results' / 'plot_category_heatmap.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print("✓ Saved: plot_category_heatmap.png")
    plt.close()


def plot_query_response_times(nlp_results, llm_results):
    fig, ax = plt.subplots(figsize=(14, 7))
    
    nlp_times = [r['response_time_ms'] for r in nlp_results['results']]
    llm_times = [r['response_time_ms'] for r in llm_results['results']]
    queries = [r['query_text'][:30] + '...' if len(r['query_text']) > 30 else r['query_text'] 
               for r in nlp_results['results']]
    
    x = np.arange(len(queries))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, nlp_times, width, label='NLP Bot', color='#2ecc71', alpha=0.8)
    bars2 = ax.bar(x + width/2, llm_times, width, label='LLM Bot', color='#3498db', alpha=0.8)
    
    ax.set_ylabel('Response Time (ms)', fontweight='bold')
    ax.set_xlabel('Query', fontweight='bold')
    ax.set_title('Response Time per Query: NLP vs LLM', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(queries, rotation=45, ha='right', fontsize=8)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    output_path = Path(__file__).parent.parent / 'results' / 'plot_query_response_times.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print("✓ Saved: plot_query_response_times.png")
    plt.close()


def plot_relevance_distribution(nlp_results, llm_results):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    nlp_relevance = [r['relevance_score'] for r in nlp_results['results']]
    llm_relevance = [r['relevance_score'] for r in llm_results['results']]
    
    ax1.hist(nlp_relevance, bins=10, color='#2ecc71', alpha=0.7, edgecolor='black')
    ax1.axvline(np.mean(nlp_relevance), color='red', linestyle='--', linewidth=2, 
                label=f'Mean: {np.mean(nlp_relevance):.3f}')
    ax1.set_xlabel('Relevance Score', fontweight='bold')
    ax1.set_ylabel('Frequency', fontweight='bold')
    ax1.set_title('NLP Bot Relevance Score Distribution', fontweight='bold', fontsize=13)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.hist(llm_relevance, bins=10, color='#3498db', alpha=0.7, edgecolor='black')
    ax2.axvline(np.mean(llm_relevance), color='red', linestyle='--', linewidth=2,
                label=f'Mean: {np.mean(llm_relevance):.3f}')
    ax2.set_xlabel('Relevance Score', fontweight='bold')
    ax2.set_ylabel('Frequency', fontweight='bold')
    ax2.set_title('LLM Bot Relevance Score Distribution', fontweight='bold', fontsize=13)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    fig.suptitle('Relevance Score Distribution Comparison', fontsize=15, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    output_path = Path(__file__).parent.parent / 'results' / 'plot_relevance_distribution.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print("✓ Saved: plot_relevance_distribution.png")
    plt.close()


def main():
    print("Loading test results...")
    nlp_results, llm_results, comparison = load_results()
    
    print("\nGenerating plots...")
    print("=" * 60)
    
    plot_response_time_comparison(nlp_results, llm_results)
    plot_response_time_log_scale(nlp_results, llm_results)
    plot_accuracy_by_category(nlp_results, llm_results)
    plot_accuracy_by_difficulty(nlp_results, llm_results)
    plot_overall_metrics(nlp_results, llm_results)
    plot_success_failure_rate(nlp_results, llm_results)
    plot_keyword_coverage(nlp_results, llm_results)
    plot_category_heatmap(nlp_results, llm_results)
    plot_query_response_times(nlp_results, llm_results)
    plot_relevance_distribution(nlp_results, llm_results)
    
    print("=" * 60)
    print(f"\n✅ All plots generated successfully!")
    print(f"📁 Saved to: results/ directory")
    print(f"📊 Total plots: 10")
    print("\nPlots generated:")
    print("  1. Response time comparison (bar chart)")
    print("  2. Response time log scale comparison")
    print("  3. Accuracy by category (grouped bar)")
    print("  4. Accuracy by difficulty (grouped bar)")
    print("  5. Overall metrics comparison")
    print("  6. Success/failure rate (pie charts)")
    print("  7. Keyword coverage (stacked bar)")
    print("  8. Category accuracy heatmap")
    print("  9. Query-specific response times")
    print(" 10. Relevance score distribution (histograms)")


if __name__ == "__main__":
    main()
