"""
Sample Data Generation Module
Creates synthetic earthquake damage data for testing and demonstration
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import argparse

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from config.settings import RAW_DATA_DIR, RANDOM_STATE, SAMPLE_SIZE, DEFAULT_DISTRIBUTION, DAMAGE_LEVELS
except ImportError:
    # Fallback if config not available
    RAW_DATA_DIR = Path(__file__).parent.parent.parent / "data" / "raw"
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    RANDOM_STATE = 42
    SAMPLE_SIZE = 10000
    DEFAULT_DISTRIBUTION = [0.05, 0.08, 0.12, 0.15, 0.18, 0.15, 0.12, 0.08, 0.05, 0.02]
    DAMAGE_LEVELS = list(range(1, 11))

def generate_earthquake_data(n_samples=10000, random_state=42, distribution=None):
    """
    Generate synthetic earthquake damage data
    
    Parameters:
    -----------
    n_samples : int
        Number of samples to generate
    random_state : int
        Random seed for reproducibility
    distribution : list
        Probability distribution for damage levels (must sum to 1)
    
    Returns:
    --------
    pandas.DataFrame
        Generated data with building features and damage labels
    """
    
    # Set random seed for reproducibility
    np.random.seed(random_state)
    
    # Use default distribution if none provided
    if distribution is None:
        distribution = DEFAULT_DISTRIBUTION
    
    # Validate distribution
    if not np.isclose(sum(distribution), 1.0):
        distribution = np.array(distribution) / sum(distribution)
        print(f"⚠️ Distribution normalized to sum to 1: {distribution}")
    
    # Generate damage levels based on distribution
    damage_data = np.random.choice(DAMAGE_LEVELS, size=n_samples, p=distribution)
    
    # Generate building features with realistic correlations
    building_age = np.random.gamma(shape=2, scale=20, size=n_samples).astype(int)
    building_age = np.clip(building_age, 1, 100)  # Age between 1-100 years
    
    # Older buildings tend to have more severe damage
    age_effect = (building_age / 100) * 2  # Max +2 severity levels
    damage_with_age = damage_data + (age_effect * np.random.normal(0.5, 0.2, n_samples)).astype(int)
    damage_with_age = np.clip(damage_with_age, 1, 10)
    
    # Generate other building features
    data = {
        'building_id': range(1, n_samples + 1),
        'severe_damage': damage_with_age,
        'original_damage': damage_data,  # Keep original for comparison
        'building_age': building_age,
        'floors': np.random.choice([1, 2, 3, 4, 5], n_samples, p=[0.3, 0.3, 0.2, 0.15, 0.05]),
        'area_sqft': np.random.normal(1500, 500, n_samples).astype(int),
        'has_foundation': np.random.choice([0, 1], n_samples, p=[0.2, 0.8]),
        'material_type': np.random.choice(['brick', 'concrete', 'wood', 'stone'], n_samples),
        'roof_type': np.random.choice(['metal', 'concrete', 'tile', 'thatch'], n_samples),
        'land_slope': np.random.choice(['flat', 'moderate', 'steep'], n_samples),
        'distance_to_fault_km': np.random.exponential(10, n_samples).round(2),
        'soil_type': np.random.choice(['rock', 'soil', 'sand'], n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Ensure area_sqft is positive
    df['area_sqft'] = np.abs(df['area_sqft'])
    df.loc[df['area_sqft'] < 300, 'area_sqft'] = 300
    
    return df

def save_sample_data(df, filename="sample_data.csv"):
    """
    Save generated data to CSV file
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Data to save
    filename : str
        Name of the file to save
    """
    output_path = RAW_DATA_DIR / filename
    df.to_csv(output_path, index=False)
    print(f"✅ Data saved to: {output_path}")
    return output_path

def main():
    """Main function to generate and save sample data"""
    parser = argparse.ArgumentParser(description='Generate sample earthquake damage data')
    parser.add_argument('--samples', type=int, default=SAMPLE_SIZE, help='Number of samples')
    parser.add_argument('--seed', type=int, default=RANDOM_STATE, help='Random seed')
    parser.add_argument('--output', type=str, default='sample_data.csv', help='Output filename')
    
    args = parser.parse_args()
    
    print("🏗️  Generating sample earthquake damage data...")
    print(f"   Samples: {args.samples}")
    print(f"   Random seed: {args.seed}")
    
    # Generate data
    df = generate_earthquake_data(
        n_samples=args.samples,
        random_state=args.seed
    )
    
    # Save to CSV
    save_sample_data(df, args.output)
    
    # Display summary
    print(f"\n📊 Data Summary:")
    print(f"   Total samples: {len(df):,}")
    print(f"   Features: {len(df.columns)}")
    print(f"   Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    print(f"\n📈 Damage Distribution:")
    damage_dist = df['severe_damage'].value_counts(normalize=True).sort_index()
    for level, prop in damage_dist.items():
        print(f"   Level {level}: {prop:.2%}")
    
    # Calculate imbalance metrics
    max_prop = damage_dist.max()
    min_prop = damage_dist.min()
    imbalance_ratio = max_prop / min_prop
    
    print(f"\n⚖️  Class Balance Metrics:")
    print(f"   Most frequent: Level {damage_dist.idxmax()} ({max_prop:.2%})")
    print(f"   Least frequent: Level {damage_dist.idxmin()} ({min_prop:.2%})")
    print(f"   Imbalance ratio: {imbalance_ratio:.2f}")
    
    if imbalance_ratio > 4:
        print("   ⚠️  Significant class imbalance detected")
    else:
        print("   ✅ Classes are relatively balanced")
    
    print(f"\n✅ Sample data generation complete!")

if __name__ == "__main__":
    main()
