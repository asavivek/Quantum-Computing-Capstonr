import pandas as pd
import numpy as np
import os

def generate_cycless_dataset(num_samples=2000, output_path="dataset.csv"):
    np.random.seed(42)
    
    crops = ['Wheat', 'Corn', 'Rice', 'Soybean']
    soil_types = ['Clay', 'Sandy', 'Loam', 'Silt']
    
    data = {
        'temperature': np.random.normal(loc=25, scale=5, size=num_samples),
        'rainfall': np.random.normal(loc=100, scale=30, size=num_samples),
        'humidity': np.random.normal(loc=60, scale=15, size=num_samples),
        'soil_ph': np.random.normal(loc=6.5, scale=1.0, size=num_samples),
        'soil_moisture': np.random.normal(loc=30, scale=10, size=num_samples),
        'soil_nutrients': np.random.normal(loc=50, scale=15, size=num_samples),
        'soil_type': np.random.choice(soil_types, num_samples),
        'crop': np.random.choice(crops, num_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Clip realistic values
    df['soil_ph'] = df['soil_ph'].clip(4.0, 9.0)
    df['humidity'] = df['humidity'].clip(20, 100)
    df['rainfall'] = df['rainfall'].clip(10, 300)
    df['soil_moisture'] = df['soil_moisture'].clip(10, 80)
    
    # Define yield based on some formula (for synthetic realism)
    # Yield = base + temp_factor + rain_factor + soil_factor + noise
    # Wheat prefers cooler, Corn warmer, etc.
    yield_base = {'Wheat': 3.5, 'Corn': 8.0, 'Rice': 5.5, 'Soybean': 3.0}
    
    yields = []
    for i, row in df.iterrows():
        base = yield_base[row['crop']]
        
        # Temp factor
        temp_diff = abs(row['temperature'] - 22) if row['crop'] == 'Wheat' else \
                    abs(row['temperature'] - 28) if row['crop'] == 'Corn' else \
                    abs(row['temperature'] - 30) if row['crop'] == 'Rice' else \
                    abs(row['temperature'] - 26)
        temp_penalty = temp_diff * 0.1
        
        # Rain factor
        rain_diff = abs(row['rainfall'] - 80) if row['crop'] == 'Wheat' else \
                    abs(row['rainfall'] - 120) if row['crop'] == 'Corn' else \
                    abs(row['rainfall'] - 200) if row['crop'] == 'Rice' else \
                    abs(row['rainfall'] - 100)
        rain_penalty = rain_diff * 0.01
        
        # pH factor (6.0 to 7.0 is best)
        ph_penalty = abs(row['soil_ph'] - 6.5) * 0.5
        
        # Soil type multiplier
        soil_mult = 1.2 if row['soil_type'] == 'Loam' else 1.0 if row['soil_type'] in ['Clay', 'Silt'] else 0.8
        
        calc_yield = (base - temp_penalty - rain_penalty - ph_penalty) * soil_mult + (row['soil_nutrients'] * 0.02)
        calc_yield += np.random.normal(0, 0.5) # noise
        
        # Ensure yield is positive
        calc_yield = max(0.5, calc_yield)
        yields.append(calc_yield)
        
    df['yield'] = yields
    
    df.to_csv(output_path, index=False)
    print(f"Generated {num_samples} samples and saved to {output_path}")
    return df

if __name__ == "__main__":
    generate_cycless_dataset()
