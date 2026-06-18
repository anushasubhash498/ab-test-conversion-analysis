import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import scipy.stats as stats

# Set style
sns.set_theme(style="darkgrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Paths
base_dir = r'C:\Users\anusu\.gemini\antigravity\scratch\analytics-portfolio\ab-test-conversion-analysis'
data_path = os.path.join(base_dir, 'data', 'ab_test_data.csv')
output_dir = os.path.join(base_dir, 'outputs')
os.makedirs(output_dir, exist_ok=True)

if not os.path.exists(data_path):
    raise FileNotFoundError(f"Data file not found at {data_path}. Run generate_data.py first.")

df = pd.read_csv(data_path)

# Ensure sorting by date
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values('timestamp')

# Grouped Summary
summary = df.groupby('group').agg(
    users=('user_id', 'count'),
    conversions=('converted', 'sum'),
    conversion_rate=('converted', 'mean')
).reset_index()

print("=== Experiment Summary ===")
print(summary.to_string(index=False))

# Statistical Hypothesis Testing (Two-Proportion Z-Test)
control = df[df['group'] == 'control']
treatment = df[df['group'] == 'treatment']

n_con = len(control)
n_treat = len(treatment)

conv_con = control['converted'].sum()
conv_treat = treatment['converted'].sum()

p_con = conv_con / n_con
p_treat = conv_treat / n_treat

# Pooled probability
p_pooled = (conv_con + conv_treat) / (n_con + n_treat)

# Standard error pooled
se_pooled = np.sqrt(p_pooled * (1 - p_pooled) * (1/n_con + 1/n_treat))

# Z-score and p-value
z_score = (p_treat - p_con) / se_pooled
p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

# 95% Confidence Interval for difference
difference = p_treat - p_con
se_diff = np.sqrt((p_con * (1 - p_con) / n_con) + (p_treat * (1 - p_treat) / n_treat))
margin_of_error = stats.norm.ppf(0.975) * se_diff
ci_lower = difference - margin_of_error
ci_upper = difference + margin_of_error

print("\n=== Statistical Testing ===")
print(f"Control CR: {p_con:.4f} ({p_con*100:.2f}%)")
print(f"Treatment CR: {p_treat:.4f} ({p_treat*100:.2f}%)")
print(f"Absolute Difference: {difference:.4f} ({difference*100:.2f}%)")
print(f"Relative Lift: {((p_treat - p_con) / p_con) * 100:.2f}%")
print(f"Z-Statistic: {z_score:.4f}")
print(f"P-Value: {p_value:.6f}")
print(f"95% Confidence Interval for Difference: [{ci_lower:.4f}, {ci_upper:.4f}]")

significant = p_value < 0.05
print(f"Statistically Significant? {'YES (Reject Null Hypothesis)' if significant else 'NO (Fail to Reject Null)'}")

# 1. Plot conversion rates with error bars (95% CI)
plt.figure(figsize=(8, 6))
# Calculate standard error for each group
se_con = np.sqrt(p_con * (1 - p_con) / n_con)
se_treat = np.sqrt(p_treat * (1 - p_treat) / n_treat)
ci_con = 1.96 * se_con
ci_treat = 1.96 * se_treat

sns.barplot(x='group', y='converted', data=df, errorbar=None, palette='pastel', width=0.5)
plt.errorbar(x=[0, 1], y=[p_con, p_treat], yerr=[ci_con, ci_treat], fmt='none', c='black', capsize=8, elinewidth=2)
plt.title('Conversion Rate Comparison with 95% Confidence Intervals', fontsize=14, fontweight='bold')
plt.xlabel('Experiment Group', fontsize=12)
plt.ylabel('Conversion Rate', fontsize=12)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'conversion_rate_comparison.png'), dpi=300)
plt.close()

# 2. Cumulative conversion rate over time (shows stabilization)
df['date'] = df['timestamp'].dt.date
cumulative_df = df.groupby(['date', 'group']).agg(
    conversions=('converted', 'sum'),
    users=('user_id', 'count')
).reset_index()

cumulative_df['cum_conversions'] = cumulative_df.groupby('group')['conversions'].cumsum()
cumulative_df['cum_users'] = cumulative_df.groupby('group')['users'].cumsum()
cumulative_df['cum_cr'] = cumulative_df['cum_conversions'] / cumulative_df['cum_users']

plt.figure(figsize=(12, 6))
sns.lineplot(data=cumulative_df, x='date', y='cum_cr', hue='group', linewidth=2.5, marker='o', palette='Set1')
plt.title('Cumulative Conversion Rate Over Time (Experiment Stability)', fontsize=14, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Cumulative Conversion Rate', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'cumulative_conversion_rate.png'), dpi=300)
plt.close()

# 3. Device Segment Analysis
device_summary = df.groupby(['device', 'group']).agg(
    users=('user_id', 'count'),
    conversions=('converted', 'sum'),
    conversion_rate=('converted', 'mean')
).reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=device_summary, x='device', y='conversion_rate', hue='group', palette='muted')
plt.title('Conversion Rate Segments by Device Type', fontsize=14, fontweight='bold')
plt.xlabel('Device Type', fontsize=12)
plt.ylabel('Conversion Rate', fontsize=12)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'device_segmentation.png'), dpi=300)
plt.close()

print("\n=== Segment Analysis: Device ===")
print(device_summary.to_string(index=False))

print("\nVisualizations and statistical plots saved to outputs/")
