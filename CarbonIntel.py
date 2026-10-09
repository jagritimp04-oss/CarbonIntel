import pandas as pd

class CarbonIntelligenceEngine:
    def __init__(self):
        # In production, load this from a managed CSV/Database
        self.factors = {
            'electricity': {'factor': 0.818, 'scope': 2, 'unit': 'kWh', 'source': 'CEA / EPA eGRID'},
            'diesel': {'factor': 2.68, 'scope': 1, 'unit': 'liters', 'source': 'DEFRA 2023'},
            'petrol': {'factor': 2.31, 'scope': 1, 'unit': 'liters', 'source': 'DEFRA 2023'},
            'waste': {'factor': 447.0, 'scope': 3, 'unit': 'tons', 'source': 'EPA WARM'}
        }
        
        # Reduction strategies matrix 
        self.strategies = [
            {'trigger_category': 'electricity', 'name': 'Install Rooftop Solar', 'cost': 'High', 'payback_years': 4.5, 'reduction_pct': 0.60},
            {'trigger_category': 'electricity', 'name': 'Switch to LED Lighting', 'cost': 'Low', 'payback_years': 0.8, 'reduction_pct': 0.15},
            {'trigger_category': 'petrol', 'name': 'Transition to EV Delivery Fleet', 'cost': 'High', 'payback_years': 3.0, 'reduction_pct': 1.00},
            {'trigger_category': 'waste', 'name': 'Implement Source Segregation & Composting', 'cost': 'Low', 'payback_years': 0.5, 'reduction_pct': 0.80}
        ]

    def calculate_footprint(self, inputs):
        results = []
        total_emissions = 0
        
        for category, amount in inputs.items():
            if category in self.factors:
                meta = self.factors[category]
                emissions = amount * meta['factor']
                total_emissions += emissions
                
                results.append({
                    'Category': category.capitalize(),
                    'Amount': amount,
                    'Unit': meta['unit'],
                    'Scope': f"Scope {meta['scope']}",
                    'Emissions (kg CO2e)': round(emissions, 2),
                    'Assumption/Source': f"{meta['factor']} kgCO2e/{meta['unit']} ({meta['source']})"
                })
                
        df_report = pd.DataFrame(results)
        return df_report, total_emissions

    def generate_reduction_plan(self, inputs, df_report):
        # Identify top emission sources
        hotspots = df_report.sort_values(by='Emissions (kg CO2e)', ascending=False)['Category'].str.lower().tolist()
        
        plan = []
        for hotspot in hotspots:
            # Find matching strategies for this hotspot
            for strat in self.strategies:
                if strat['trigger_category'] == hotspot:
                    current_emissions = df_report[df_report['Category'].str.lower() == hotspot]['Emissions (kg CO2e)'].values[0]
                    co2_saved = current_emissions * strat['reduction_pct']
                    
                    plan.append({
                        'Target': hotspot.capitalize(),
                        'Action': strat['name'],
                        'Est. Cost': strat['cost'],
                        'Payback (years)': strat['payback_years'], # FIX: Keep as float for accurate sorting
                        'Potential CO2 Saved (kg)': round(co2_saved, 2)
                    })
        
        # Rank by quickest payback and highest impact
        df_plan = pd.DataFrame(plan).sort_values(
            by=['Payback (years)', 'Potential CO2 Saved (kg)'], 
            ascending=[True, False]
        )
        return df_plan
# Demo Execution
# Demo Execution
if __name__ == "__main__":
    tool = CarbonIntelligenceEngine()
    
    # 1. Simple inputs from a non-expert (Annual data)
    sample_business_data = {
        'electricity': 12000, # kWh
        'petrol': 2500,       # liters
        'waste': 12           # tons
    }
    
    # 2. Calculate Footprint
    footprint, total = tool.calculate_footprint(sample_business_data)
    
    # 3. Generate Reduction Plan
    reduction_plan = tool.generate_reduction_plan(sample_business_data, footprint)
    
    # --- FIX: Print the stored variables to the terminal ---
    print("\n=== CARBON FOOTPRINT REPORT ===")
    print(footprint.to_string(index=False))
    print(f"\nTotal Emissions: {total:,.2f} kg CO2e")
    
    print("\n=== EMISSION REDUCTION PLAN ===")
    print(reduction_plan.to_string(index=False))