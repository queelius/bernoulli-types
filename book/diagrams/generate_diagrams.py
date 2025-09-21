#!/usr/bin/env python3
"""
Generate complex diagrams for the book using matplotlib and other libraries
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.patches as mpatches

# Set up the plotting style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10

def plot_bloom_filter_visualization():
    """Visualize how Bloom filters work with multiple hash functions"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Bloom filter bit array
    bits = 32
    bit_array = np.zeros(bits)
    
    # Elements and their hash positions
    elements = {
        'apple': [3, 7, 15],
        'banana': [7, 12, 25],
        'cherry': [15, 20, 28]
    }
    
    # Mark bits for each element
    colors = {'apple': 'red', 'banana': 'yellow', 'cherry': 'purple'}
    
    # First subplot: Show individual elements
    ax1.set_title('Bloom Filter: Individual Element Mappings')
    for i in range(bits):
        ax1.add_patch(Rectangle((i, 0), 1, 1, 
                                facecolor='white', 
                                edgecolor='black'))
    
    y_offset = 2
    for elem, positions in elements.items():
        for pos in positions:
            if pos < bits:
                # Draw arrow from element to bit position
                ax1.arrow(pos + 0.5, 1.2, 0, -0.15, 
                         head_width=0.3, head_length=0.05,
                         fc=colors[elem], ec=colors[elem])
                bit_array[pos] = 1
        
        # Add element label
        ax1.text(bits/2, y_offset, elem, 
                ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.3", 
                         facecolor=colors[elem], alpha=0.5))
        y_offset += 0.5
    
    ax1.set_xlim(-0.5, bits)
    ax1.set_ylim(-0.5, 3.5)
    ax1.set_aspect('equal')
    ax1.axis('off')
    
    # Second subplot: Show combined bit array
    ax2.set_title('Combined Bloom Filter State')
    for i in range(bits):
        color = 'lightgreen' if bit_array[i] == 1 else 'white'
        ax2.add_patch(Rectangle((i, 0), 1, 1, 
                                facecolor=color, 
                                edgecolor='black'))
        ax2.text(i + 0.5, 0.5, str(int(bit_array[i])),
                ha='center', va='center', fontweight='bold')
    
    ax2.set_xlim(-0.5, bits)
    ax2.set_ylim(-0.5, 1.5)
    ax2.set_aspect('equal')
    ax2.axis('off')
    
    # Add false positive rate annotation
    filled_bits = np.sum(bit_array)
    fp_rate = (filled_bits / bits) ** 3  # Approximate for 3 hash functions
    ax2.text(bits/2, -0.7, 
            f'Filled: {filled_bits}/{bits} bits ({filled_bits/bits:.1%})\n'
            f'Approx. False Positive Rate: {fp_rate:.2%}',
            ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue'))
    
    plt.tight_layout()
    plt.savefig('bloom_filter_viz.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('bloom_filter_viz.png', dpi=300, bbox_inches='tight')
    print("Generated: bloom_filter_viz.pdf/png")

def plot_privacy_leakage_timeline():
    """Show how patterns emerge over time from queries"""
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    
    # Simulate query timeline
    hours = np.arange(0, 168)  # One week in hours
    
    # Query patterns for different scenarios
    # Journalist investigating (focused bursts)
    journalist_queries = np.zeros(168)
    journalist_queries[40:45] = [5, 8, 12, 7, 4]  # Monday investigation
    journalist_queries[65:68] = [15, 18, 10]  # Tuesday deep dive
    journalist_queries[88:92] = [6, 9, 11, 7]  # Wednesday follow-up
    journalist_queries[135:140] = [20, 25, 22, 18, 15]  # Friday breakthrough
    
    # Normal user (spread out, lower intensity)
    normal_queries = np.random.poisson(2, 168)
    normal_queries = np.convolve(normal_queries, np.ones(3)/3, mode='same')
    
    # Plot 1: Raw query counts
    axes[0].set_title('Query Volume Over Time')
    axes[0].bar(hours, journalist_queries, color='red', alpha=0.6, label='Journalist')
    axes[0].bar(hours, normal_queries, color='blue', alpha=0.6, label='Normal User')
    axes[0].set_xlabel('Hour of Week')
    axes[0].set_ylabel('Query Count')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Correlation patterns
    axes[1].set_title('Query Correlation Patterns (Co-occurrence within 1 hour)')
    
    # Simulate correlation matrix
    terms = ['senator', 'offshore', 'panama', 'transfer', 'investigation',
             'weather', 'news', 'sports', 'email', 'calendar']
    
    # Journalist has high correlation between investigation terms
    journalist_corr = np.eye(10)
    journalist_corr[:5, :5] = 0.7 + 0.3 * np.random.rand(5, 5)
    np.fill_diagonal(journalist_corr, 1)
    
    im1 = axes[1].imshow(journalist_corr, cmap='Reds', vmin=0, vmax=1)
    axes[1].set_xticks(range(10))
    axes[1].set_yticks(range(10))
    axes[1].set_xticklabels(terms, rotation=45, ha='right')
    axes[1].set_yticklabels(terms)
    axes[1].set_title('Journalist Query Correlations')
    plt.colorbar(im1, ax=axes[1], label='Correlation')
    
    # Plot 3: Frequency distribution
    axes[2].set_title('Term Frequency Distribution (Log Scale)')
    
    journalist_freqs = [50, 45, 40, 35, 30, 5, 3, 2, 1, 1]
    normal_freqs = [10, 8, 7, 6, 5, 15, 20, 18, 12, 10]
    
    x = np.arange(len(terms))
    width = 0.35
    
    axes[2].bar(x - width/2, journalist_freqs, width, 
               label='Journalist', color='red', alpha=0.7)
    axes[2].bar(x + width/2, normal_freqs, width,
               label='Normal User', color='blue', alpha=0.7)
    
    axes[2].set_yscale('log')
    axes[2].set_xlabel('Search Terms')
    axes[2].set_ylabel('Frequency (log scale)')
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(terms, rotation=45, ha='right')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3, which='both')
    
    plt.suptitle('Privacy Leakage: Patterns That Reveal User Intent', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('privacy_leakage_timeline.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('privacy_leakage_timeline.png', dpi=300, bbox_inches='tight')
    print("Generated: privacy_leakage_timeline.pdf/png")

def plot_oblivious_transformation():
    """Show how queries become indistinguishable"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    
    # Original queries (distinguishable)
    queries = ['covid', 'vaccine', 'senator', 'offshore', 'weather', 'news']
    colors = ['red', 'red', 'orange', 'orange', 'blue', 'blue']
    
    # Plot 1: Original queries (distinguishable patterns)
    axes[0, 0].set_title('Original Queries')
    for i, (q, c) in enumerate(zip(queries, colors)):
        axes[0, 0].text(0.5, 0.8 - i*0.15, q, 
                       ha='center', fontsize=12,
                       bbox=dict(boxstyle="round,pad=0.3", 
                                facecolor=c, alpha=0.3))
    axes[0, 0].set_xlim(0, 1)
    axes[0, 0].set_ylim(0, 1)
    axes[0, 0].axis('off')
    
    # Plot 2: After hashing (still distinguishable by pattern)
    axes[0, 1].set_title('Hashed Queries')
    hashes = ['0x3f2a...', '0x8b1c...', '0x2d4e...', 
             '0x9a7f...', '0x1c3b...', '0x5e8d...']
    for i, (h, c) in enumerate(zip(hashes, colors)):
        axes[0, 1].text(0.5, 0.8 - i*0.15, h,
                       ha='center', fontsize=10, family='monospace',
                       bbox=dict(boxstyle="round,pad=0.3",
                                facecolor=c, alpha=0.2))
    axes[0, 1].set_xlim(0, 1)
    axes[0, 1].set_ylim(0, 1)
    axes[0, 1].axis('off')
    
    # Plot 3: After oblivious encoding (indistinguishable)
    axes[0, 2].set_title('Oblivious Encoding')
    np.random.seed(42)
    for i in range(6):
        # Generate random bit pattern
        bits = np.random.randint(0, 2, 16)
        bit_str = ''.join(map(str, bits))
        axes[0, 2].text(0.5, 0.8 - i*0.15, bit_str,
                       ha='center', fontsize=8, family='monospace',
                       bbox=dict(boxstyle="round,pad=0.3",
                                facecolor='gray', alpha=0.3))
    axes[0, 2].set_xlim(0, 1)
    axes[0, 2].set_ylim(0, 1)
    axes[0, 2].axis('off')
    
    # Bottom row: Statistical properties
    # Plot 4: Frequency distribution (original)
    axes[1, 0].set_title('Frequency Pattern')
    freqs = [30, 25, 15, 10, 50, 45]
    axes[1, 0].bar(range(6), freqs, color=colors, alpha=0.6)
    axes[1, 0].set_xlabel('Query ID')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].set_ylim(0, 60)
    
    # Plot 5: Correlation matrix (original)
    axes[1, 1].set_title('Correlation Pattern')
    corr_matrix = np.array([
        [1.0, 0.8, 0.2, 0.1, 0.0, 0.0],
        [0.8, 1.0, 0.2, 0.1, 0.0, 0.0],
        [0.2, 0.2, 1.0, 0.7, 0.0, 0.0],
        [0.1, 0.1, 0.7, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1.0, 0.3],
        [0.0, 0.0, 0.0, 0.0, 0.3, 1.0]
    ])
    im = axes[1, 1].imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
    axes[1, 1].set_xlabel('Query ID')
    axes[1, 1].set_ylabel('Query ID')
    
    # Plot 6: After oblivious (uniform)
    axes[1, 2].set_title('Oblivious: Uniform Noise')
    # Generate uniform random pattern
    uniform_data = np.random.uniform(0.4, 0.6, (6, 6))
    np.fill_diagonal(uniform_data, 0.5)
    im2 = axes[1, 2].imshow(uniform_data, cmap='gray', vmin=0, vmax=1)
    axes[1, 2].set_xlabel('Encoding ID')
    axes[1, 2].set_ylabel('Encoding ID')
    
    plt.suptitle('Oblivious Transformation: From Patterns to Noise',
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('oblivious_transformation.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('oblivious_transformation.png', dpi=300, bbox_inches='tight')
    print("Generated: oblivious_transformation.pdf/png")

def plot_performance_metrics():
    """Generate performance comparison charts"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Data for comparisons
    systems = ['Exact\nHashMap', 'Bloom\nFilter', 'Bernoulli\nOblivious', 'Homomorphic\nEncryption']
    
    # Plot 1: Space usage
    space_usage = [100, 10, 15, 100]  # Relative units
    colors_space = ['blue', 'green', 'red', 'purple']
    axes[0, 0].bar(systems, space_usage, color=colors_space, alpha=0.7)
    axes[0, 0].set_title('Space Usage (Relative)', fontweight='bold')
    axes[0, 0].set_ylabel('Space (GB for 1B items)')
    axes[0, 0].set_ylim(0, 120)
    for i, v in enumerate(space_usage):
        axes[0, 0].text(i, v + 2, str(v), ha='center', fontweight='bold')
    
    # Plot 2: Query latency
    latency = [0.001, 0.0001, 0.00005, 10]  # Seconds
    axes[0, 1].bar(systems, latency, color=colors_space, alpha=0.7)
    axes[0, 1].set_title('Query Latency', fontweight='bold')
    axes[0, 1].set_ylabel('Time (seconds)')
    axes[0, 1].set_yscale('log')
    axes[0, 1].set_ylim(0.00001, 100)
    for i, v in enumerate(latency):
        axes[0, 1].text(i, v * 2, f'{v:.5f}s', ha='center', fontweight='bold')
    
    # Plot 3: Privacy level
    privacy = [0, 20, 95, 100]  # Percentage
    axes[1, 0].bar(systems, privacy, color=colors_space, alpha=0.7)
    axes[1, 0].set_title('Privacy Protection Level', fontweight='bold')
    axes[1, 0].set_ylabel('Privacy (%)')
    axes[1, 0].set_ylim(0, 110)
    for i, v in enumerate(privacy):
        axes[1, 0].text(i, v + 2, f'{v}%', ha='center', fontweight='bold')
    
    # Plot 4: Error rate
    error_rate = [0, 0.001, 0.001, 0]  # False positive rate
    axes[1, 1].bar(systems, [r * 100 for r in error_rate], color=colors_space, alpha=0.7)
    axes[1, 1].set_title('Error Rate', fontweight='bold')
    axes[1, 1].set_ylabel('False Positive Rate (%)')
    axes[1, 1].set_ylim(0, 0.15)
    for i, v in enumerate(error_rate):
        axes[1, 1].text(i, v * 100 + 0.005, f'{v*100:.3f}%', ha='center', fontweight='bold')
    
    plt.suptitle('System Performance Comparison', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('performance_metrics.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('performance_metrics.png', dpi=300, bbox_inches='tight')
    print("Generated: performance_metrics.pdf/png")

def plot_error_propagation():
    """Show how errors propagate through operations"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Create a flow diagram showing error propagation
    operations = ['Input\nSet A\n(ε=0.001)', 
                  'Input\nSet B\n(ε=0.001)',
                  'Union\nA ∪ B\n(ε≤0.002)',
                  'Input\nSet C\n(ε=0.001)',
                  'Intersection\n(A∪B) ∩ C\n(ε≤0.003)']
    
    # Position nodes
    positions = [(1, 2), (1, 0), (3, 1), (5, 1), (7, 1)]
    
    # Draw nodes
    for (x, y), label in zip(positions, operations):
        if 'Input' in label:
            color = 'lightblue'
        elif 'Union' in label:
            color = 'lightgreen'
        else:
            color = 'lightyellow'
        
        fancy_box = FancyBboxPatch((x-0.4, y-0.3), 0.8, 0.6,
                                   boxstyle="round,pad=0.05",
                                   facecolor=color,
                                   edgecolor='black',
                                   linewidth=2)
        ax.add_patch(fancy_box)
        ax.text(x, y, label, ha='center', va='center', fontsize=10)
    
    # Draw arrows
    arrows = [((1.4, 2), (2.6, 1.2)),
             ((1.4, 0), (2.6, 0.8)),
             ((3.4, 1), (4.6, 1)),
             ((5.4, 1), (6.6, 1))]
    
    for start, end in arrows:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    
    # Add error accumulation annotation
    ax.text(4, 2.5, 'Error Accumulation Through Operations',
           fontsize=14, fontweight='bold', ha='center')
    
    ax.text(4, -0.5, 
           'Key Insight: Error rates are bounded and predictable\n'
           'Union: ε₁ + ε₂ - ε₁ε₂ ≈ ε₁ + ε₂\n'
           'Intersection: ε₁ε₂ (for independent errors)',
           ha='center', fontsize=11,
           bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow'))
    
    ax.set_xlim(0, 8)
    ax.set_ylim(-1, 3)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('error_propagation.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('error_propagation.png', dpi=300, bbox_inches='tight')
    print("Generated: error_propagation.pdf/png")

def main():
    """Generate all diagrams"""
    print("Generating book diagrams...")
    
    # Create individual diagram functions
    plot_bloom_filter_visualization()
    plot_privacy_leakage_timeline()
    plot_oblivious_transformation()
    plot_performance_metrics()
    plot_error_propagation()
    
    print("\nAll diagrams generated successfully!")
    print("Files created:")
    print("  - bloom_filter_viz.pdf/png")
    print("  - privacy_leakage_timeline.pdf/png")
    print("  - oblivious_transformation.pdf/png")
    print("  - performance_metrics.pdf/png")
    print("  - error_propagation.pdf/png")

if __name__ == "__main__":
    main()