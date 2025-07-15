
import pandas as pd
import json
from urllib.parse import urlparse
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

# ----------------------------------------
# Step 1: Flatten JSON (just get it into a table shape)
# ----------------------------------------

# Load JSON file
with open(r'D:\projects\GTAGRA project\Assignment-1\response.json', encoding='utf-8') as file:
    raw_data = json.load(file)

# Grab notices (assuming always present)
notice_list = raw_data.get('notices', [])

# List to hold each row
all_rows = []

# Loop through notices
for each_notice in notice_list:
    copied_notice = each_notice.copy()
    works_data = copied_notice.pop("works", [])

    # Loop through works in each notice
    for single_work in works_data:
        desc_text = single_work.get("description", "")
        infringing_entries = single_work.get("infringing_urls", [])

        # Loop through each infringing URL entry
        for infringing_item in infringing_entries:
            link = infringing_item.get("url", "")

            # Create row dict copying notice info
            row_dict = copied_notice.copy()
            row_dict["work_description"] = desc_text
            row_dict["infringing_url"] = link

            # Add to list
            all_rows.append(row_dict)

# Convert list to DataFrame
df_flat = pd.DataFrame(all_rows)

# Save intermediate CSV so I can peek at it later if needed
df_flat.to_csv(r'D:\projects\GTAGRA project\Assignment-1\Python\flattened_step1.csv', index=False)

# Print progress
print("✅ Step 1 finished — flattened_step1.csv written out.")
print(df_flat.head())

# ----------------------------------------
# Step 2 & 3: Add domain column and resolve IPs in parallel
# ----------------------------------------

# Add domain column
df_flat['domain'] = df_flat['infringing_url'].apply(lambda url: urlparse(url).netloc)

# Function to resolve IP — may fail sometimes
def resolve_ip_address(domain_name):
    try:
        ip_value = socket.gethostbyname(domain_name)
        return ip_value
    except Exception as err:
        return None

# Get all unique domains
unique_domain_list = df_flat['domain'].unique()

# Dictionary to store domain -> IP
domain_ip_lookup = {}

# Use thread pool to resolve in parallel
with ThreadPoolExecutor(max_workers=4) as pool:
    future_to_domain = {pool.submit(resolve_ip_address, d): d for d in unique_domain_list}
    for future in as_completed(future_to_domain):
        domain = future_to_domain[future]
        try:
            ip_addr = future.result()
            domain_ip_lookup[domain] = ip_addr
        except Exception:
            domain_ip_lookup[domain] = None

# Map IP addresses back to DataFrame
df_flat['ip_address'] = df_flat['domain'].map(domain_ip_lookup)

# Save updated CSV
df_flat.to_csv(r'D:\projects\GTAGRA project\Assignment-1\Python\flattened_step2-3.csv', index=False)

# Print progress
print("✅ Step 2 & 3 done — saved as flattened_step3.csv.")
print(df_flat[['domain', 'ip_address']].head())

# ----------------------------------------
# Step 4: Generate various summaries (some fun metrics!)
# ----------------------------------------

# Top 10 domains by count of infringing URLs
# (summary file: summary_urls_per_domain.csv)
domain_summary = df_flat['domain'].value_counts().head(10)
domain_summary.to_csv(r'D:\projects\GTAGRA project\Assignment-1\Python\summary_urls_per_domain.csv')
print("✅ Domain summary saved: summary_urls_per_domain.csv")
print(domain_summary)

# Number of unique notices per sender
# (summary file: summary_notices_per_sender.csv)
notice_summary = df_flat.groupby('sender_name')['id'].nunique().sort_values(ascending=False)
notice_summary.to_csv(r'D:\projects\GTAGRA project\Assignment-1\Python\summary_notices_per_sender.csv')
print("\n✅ Notice summary saved: summary_notices_per_sender.csv")
print(notice_summary.head(10))

# Infringing URLs per work description
# (summary file: summary_urls_per_work.csv)
work_summary = df_flat.groupby('work_description')['infringing_url'].count().sort_values(ascending=False)
work_summary.to_csv(r'D:\projects\GTAGRA project\Assignment-1\Python\summary_urls_per_work.csv')
print("\n✅ Work summary saved: summary_urls_per_work.csv")
print(work_summary.head(10))

# Extra numeric-based metrics
urls_by_sender = df_flat.groupby('sender_name')['infringing_url'].count().sort_values(ascending=False)
top_sender = urls_by_sender.index[0]
top_sender_count = urls_by_sender.iloc[0]
print(f"\n🚨 Top sender by URLs: {top_sender} ({top_sender_count} URLs)")

urls_by_work = df_flat.groupby('work_description')['infringing_url'].count().sort_values(ascending=False)
top_work = urls_by_work.index[0]
top_work_count = urls_by_work.iloc[0]
print(f"\n🎥 Top work by URLs: {top_work} ({top_work_count} URLs)")

urls_by_domain = df_flat['domain'].value_counts()
top_domain = urls_by_domain.index[0]
top_domain_count = urls_by_domain.iloc[0]
print(f"\n🌐 Top domain by URLs: {top_domain} ({top_domain_count} URLs)")

urls_by_notice = df_flat.groupby('id')['infringing_url'].count().sort_values(ascending=False)
top_notice_id = urls_by_notice.index[0]
top_notice_count = urls_by_notice.iloc[0]
print(f"\n📄 Notice ID with most URLs: {top_notice_id} ({top_notice_count} URLs)")

# Unique domains in top sender's data
df_sender = df_flat[df_flat['sender_name'] == top_sender]
unique_domains_sender = df_sender['domain'].nunique()
print(f"\n⭐ Unique domains in top sender’s data: {unique_domains_sender}")
