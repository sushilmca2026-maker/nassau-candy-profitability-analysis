from pathlib import Path
from analysis import clean_data, aggregate_products, aggregate_divisions, pareto, factory_summary, validation_report

ROOT = Path(__file__).resolve().parents[1]
df, stats = clean_data(ROOT / 'data' / 'NassauCandyDistributor.csv')
out = ROOT / 'outputs'
out.mkdir(exist_ok=True)
df.to_csv(out / 'cleaned_transactions.csv', index=False)
aggregate_products(df).to_csv(out / 'product_profitability.csv', index=False)
aggregate_divisions(df).to_csv(out / 'division_performance.csv', index=False)
factory_summary(df).to_csv(out / 'factory_performance.csv', index=False)
pareto(df, 'Sales').to_csv(out / 'revenue_pareto.csv', index=False)
pareto(df, 'Gross Profit').to_csv(out / 'profit_pareto.csv', index=False)
validation_report(df, stats).to_csv(out / 'validation_report.csv', index=False)
(ROOT / 'outputs' / 'data_quality_stats.txt').write_text('\n'.join(f'{k}: {v}' for k,v in stats.items()) + '\n', encoding='utf-8')
print('Generated outputs:', ', '.join(p.name for p in out.iterdir() if p.is_file()))
