import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew
import warnings
warnings.filterwarnings('ignore')

def analyze_data_distribution(df):
	"""
	parameter:
	df (pd.DataFrame): input data

	return:
	dict: skewed features and outliers
	"""
	quantitative_vars = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
	print(f"There are {len(quantitative_vars)} quantitative variables: {quantitative_vars}")

	results = {
		'skewed_features': [],
		'outliers': {}
	}

	for var in quantitative_vars:
		data = df[var].dropna()
		if len(data) == 0:
			continue

		skewness = skew(data)
		plt.figure(figsize=(10, 6))
		sns.histplot(data=data, kde=True)
		plt.title(f'Distribution of {var}\nSkewness: {skewness:.2f}')

		is_strongly_skewed = abs(skewness) > 1
		if is_strongly_skewed:
			plt.axvline(x=data.mean(), color='r', linestyle='--', label=f'Mean: {data.mean():.2f}')
			plt.axvline(x=data.median(), color='g', linestyle='-', label=f'Median: {data.median():.2f}')
			plt.legend()
			print(f"variables {var} exist skewness，value is: {skewness:.2f}")

		results['skewed_features'].append({
			'variable': var,
			'skewness': skewness,
			'is_strongly_skewed': is_strongly_skewed
		})

		plt.tight_layout()
		plt.savefig('Distribution of ' + var + '.jpg')
		plt.show()

		# outliers
		q1 = data.quantile(0.25)
		q3 = data.quantile(0.75)
		iqr = q3 - q1
		lower_bound = q1 - 1.5 * iqr
		upper_bound = q3 + 1.5 * iqr

		outliers = data[(data < lower_bound) | (data > upper_bound)]
		outlier_count = len(outliers)
		outlier_percentage = (outlier_count / len(data)) * 100 if len(data) > 0 else 0

		results['outliers'][var] = {
			'count': outlier_count,
			'percentage': outlier_percentage,
			'values': outliers.tolist(),
			'lower_bound': lower_bound,
			'upper_bound': upper_bound
		}

		if outlier_count > 0:
			print(f"variables {var} has {outlier_count} outliers, with {outlier_percentage:.2f}%")

			plt.figure(figsize=(8, 4))
			sns.boxplot(data=data)
			plt.title(f'Boxplot of {var} (with outliers)')
			plt.tight_layout()
			plt.show()

	return results


if __name__ == "__main__":
	df = pd.read_csv("turn_2_stats.csv") # need to change file name
	df = df.replace([np.inf, -np.inf], np.nan)

	analysis_results = analyze_data_distribution(df)

	print("\n Result:")
	print("skewed_features:")
	for feature in analysis_results['skewed_features']:
		if feature['is_strongly_skewed']:
			print(f"- {feature['variable']}: skewed value = {feature['skewness']:.2f}")

	print("\nOutliers:")
	for var, outlier_info in analysis_results['outliers'].items():
		print(f"- {var}: {outlier_info['count']} has ({outlier_info['percentage']:.2f}%)")
