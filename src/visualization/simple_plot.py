"""
Simple Visualization Module
Creates professional plots for damage distribution analysis
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from config.settings import FIGURES_DIR, COLORS, DAMAGE_LABELS
except ImportError:
    # Fallback if config not available
    FIGURES_DIR = Path(__file__).parent.parent.parent / "reports" / "figures"
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    COLORS = {
        'primary': '#2E86AB',
        'secondary': '#A23B72',
        'accent': '#F18F01',
        'warning': '#C73E1D',
        'success': '#4C9A8A'
    }
    DAMAGE_LABELS = [f'Level {i}' for i in range(1, 11)]

def plot_damage_distribution(df, target_col='severe_damage', save=False, filename='damage_distribution.png'):
    """
    Create a professional bar plot of damage distribution
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe
    target_col : str
        Column name containing damage labels
    save : bool
        Whether to save the figure
    filename : str
        Filename for saved figure
    
    Returns:
    --------
    fig, ax : matplotlib figure and axes objects
    """
    
    # Calculate value counts
    proportions = df[target_col].value_counts(normalize=True).sort_index()
    
    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Create bars
    bars = ax.bar(
        range(len(proportions)),
        proportions.values,
        color=COLORS['primary'],
        edgecolor='black',
        linewidth=1.5,
        alpha=0.8,
        width=0.7
    )
    
    # Customize labels
    ax.set_xlabel('Damage Severity Level', fontsize=12, fontweight='bold', labelpad=10)
    ax.set_ylabel('Relative Frequency', fontsize=12, fontweight='bold', labelpad=10)
    ax.set_title('Kavrepalanchok: Building Damage Distribution', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Set x-tick labels
    ax.set_xticks(range(len(proportions)))
    ax.set_xticklabels(DAMAGE_LABELS[:len(proportions)], fontsize=10)
    
    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, proportions.values)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                f'{value:.1%}', ha='center', va='bottom', 
                fontsize=9, fontweight='bold')
    
    # Add grid for readability
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.7)
    ax.set_axisbelow(True)
    
    # Set y-axis limits with padding
    ax.set_ylim(0, max(proportions.values) * 1.1)
    
    # Add annotation for class balance
    max_min_ratio = proportions.max() / proportions.min()
    balance_status = "Balanced" if max_min_ratio < 4 else "Imbalanced"
    
    ax.text(0.02, 0.98, 
            f"Class Balance: {balance_status}\nMax/Min Ratio: {max_min_ratio:.2f}",
            transform=ax.transAxes, fontsize=9,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    # Save if requested
    if save:
        save_path = FIGURES_DIR / filename
        plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        print(f"✅ Figure saved to: {save_path}")
    
    return fig, ax

def plot_damage_comparison(df, group_col, target_col='severe_damage', save=False):
    """
    Compare damage distribution across different groups
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe
    group_col : str
        Column to group by
    target_col : str
        Column containing damage labels
    save : bool
        Whether to save the figure
    """
    
    # Get unique groups
    groups = df[group_col].unique()
    n_groups = len(groups)
    
    # Create subplots
    fig, axes = plt.subplots(1, n_groups, figsize=(5*n_groups, 5))
    if n_groups == 1:
        axes = [axes]
    
    fig.suptitle(f'Damage Distribution by {group_col.replace("_", " ").title()}', 
                fontsize=14, fontweight='bold', y=1.02)
    
    for ax, group in zip(axes, groups):
        # Filter data for this group
        group_df = df[df[group_col] == group]
        proportions = group_df[target_col].value_counts(normalize=True).sort_index()
        
        # Plot
        bars = ax.bar(range(len(proportions)), proportions.values,
                     color=COLORS['secondary'], edgecolor='black', alpha=0.8)
        
        ax.set_title(f'{group_col}: {group}\nn={len(group_df)}', fontsize=11)
        ax.set_xlabel('Damage Level')
        ax.set_ylabel('Frequency')
        ax.set_xticks(range(len(proportions)))
        ax.set_xticklabels(range(1, len(proportions)+1))
        
        # Add value labels
        for bar, value in zip(bars, proportions.values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.2f}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    
    if save:
        save_path = FIGURES_DIR / f'damage_by_{group_col}.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Figure saved to: {save_path}")
    
    return fig, axes

def plot_feature_distribution(df, feature_col, target_col='severe_damage', save=False):
    """
    Plot distribution of a feature across damage levels
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe
    feature_col : str
        Feature to analyze
    target_col : str
        Column containing damage labels
    save : bool
        Whether to save the figure
    """
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create box plot
    df.boxplot(column=feature_col, by=target_col, ax=ax)
    
    ax.set_title(f'{feature_col.replace("_", " ").title()} by Damage Level', 
                fontsize=14, fontweight='bold')
    ax.set_xlabel('Damage Severity Level', fontsize=12)
    ax.set_ylabel(feature_col.replace('_', ' ').title(), fontsize=12)
    
    # Add mean markers
    means = df.groupby(target_col)[feature_col].mean()
    ax.plot(range(1, len(means)+1), means.values, 'r--', linewidth=2, label='Mean')
    ax.legend()
    
    plt.suptitle('')  # Remove automatic suptitle
    plt.tight_layout()
    
    if save:
        save_path = FIGURES_DIR / f'{feature_col}_distribution.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Figure saved to: {save_path}")
    
    return fig, ax

def create_dashboard_figure(df, target_col='severe_damage', save=False):
    """
    Create a comprehensive dashboard figure with multiple plots
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe
    target_col : str
        Column containing damage labels
    save : bool
        Whether to save the figure
    """
    
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle('Nepal Earthquake Damage Analysis Dashboard\nKavrepalanchok District', 
                fontsize=16, fontweight='bold', y=0.98)
    
    # Create grid for subplots
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
    
    # Plot 1: Main distribution
    ax1 = fig.add_subplot(gs[0, 0])
    proportions = df[target_col].value_counts(normalize=True).sort_index()
    bars = ax1.bar(range(len(proportions)), proportions.values,
                  color=COLORS['primary'], edgecolor='black')
    ax1.set_title('Damage Distribution', fontweight='bold')
    ax1.set_xlabel('Level')
    ax1.set_ylabel('Frequency')
    ax1.set_xticks(range(len(proportions)))
    ax1.set_xticklabels(range(1, len(proportions)+1))
    
    # Plot 2: Cumulative distribution
    ax2 = fig.add_subplot(gs[0, 1])
    cumulative = proportions.sort_index().cumsum()
    ax2.plot(range(1, len(cumulative)+1), cumulative.values, 
            marker='o', color=COLORS['secondary'], linewidth=2)
    ax2.set_title('Cumulative Distribution', fontweight='bold')
    ax2.set_xlabel('Damage Level')
    ax2.set_ylabel('Cumulative Frequency')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Pie chart
    ax3 = fig.add_subplot(gs[0, 2])
    wedges, texts, autotexts = ax3.pie(
        proportions.values[:5],  # Show top 5 for clarity
        labels=[f'L{i+1}' for i in range(5)],
        autopct='%1.1f%%',
        colors=[COLORS['primary'], COLORS['secondary'], 
                COLORS['accent'], COLORS['warning'], COLORS['success']]
    )
    ax3.set_title('Top 5 Levels Distribution', fontweight='bold')
    
    # Plot 4: Building age distribution
    ax4 = fig.add_subplot(gs[1, 0])
    if 'building_age' in df.columns:
        df.boxplot(column='building_age', by=target_col, ax=ax4)
        ax4.set_title('Building Age by Damage Level', fontweight='bold')
        ax4.set_xlabel('Level')
        ax4.set_ylabel('Age (years)')
        plt.suptitle('')  # Remove automatic suptitle
    
    # Plot 5: Sample size per level
    ax5 = fig.add_subplot(gs[1, 1])
    counts = df[target_col].value_counts().sort_index()
    ax5.bar(range(len(counts)), counts.values, color=COLORS['accent'], edgecolor='black')
    ax5.set_title('Sample Size per Level', fontweight='bold')
    ax5.set_xlabel('Damage Level')
    ax5.set_ylabel('Count')
    ax5.set_xticks(range(len(counts)))
    ax5.set_xticklabels(range(1, len(counts)+1))
    
    # Plot 6: Summary statistics
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.axis('off')
    
    # Calculate metrics
    max_prop = proportions.max()
    min_prop = proportions.min()
    imbalance_ratio = max_prop / min_prop
    
    stats_text = f"""
    📊 SUMMARY STATISTICS
    {'='*25}
    
    Total Samples: {len(df):,}
    Damage Levels: {len(proportions)}
    
    Most Frequent:
      Level {proportions.idxmax()}
      {max_prop:.1%} of samples
    
    Least Frequent:
      Level {proportions.idxmin()}
      {min_prop:.1%} of samples
    
    Imbalance Ratio: {imbalance_ratio:.2f}
    
    {'⚠️ IMBALANCED' if imbalance_ratio > 4 else '✅ BALANCED'}
    
    RECOMMENDATION:
    {'Use sampling techniques' if imbalance_ratio > 4 
     else 'Standard modeling OK'}
    """
    
    ax6.text(0.1, 0.5, stats_text, transform=ax6.transAxes,
            fontsize=11, verticalalignment='center',
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout()
    
    if save:
        save_path = FIGURES_DIR / 'dashboard.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Dashboard saved to: {save_path}")
    
    return fig
