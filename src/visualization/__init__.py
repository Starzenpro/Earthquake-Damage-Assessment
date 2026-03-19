"""
Visualization Package for Nepal Earthquake Damage Analysis
"""

from .simple_plot import (
    plot_damage_distribution,
    plot_damage_comparison,
    plot_feature_distribution,
    create_dashboard_figure
)

__all__ = [
    'plot_damage_distribution',
    'plot_damage_comparison',
    'plot_feature_distribution',
    'create_dashboard_figure'
]
