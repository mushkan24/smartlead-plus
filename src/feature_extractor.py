import pandas as pd
import tldextract

DISPOSABLE_DOMAINS = ["tempmail.com", "mailinator.com", "10minutemail.com"]

def extract_features(df):
    df = df.copy()

    # Email length
    df['EmailLength'] = df['Email'].apply(lambda x: len(str(x)) if pd.notnull(x) else 0)

    # Website HTTPS check
    df['WebsiteHTTPS'] = df['Website'].apply(lambda x: 1 if isinstance(x, str) and x.startswith("https") else 0)

    # Count missing fields per row
    df['MissingFields'] = df.isnull().sum(axis=1)

    # Disposable domain flag
    def is_disposable(email):
        return any(domain in str(email) for domain in DISPOSABLE_DOMAINS)

    df['HasDisposableDomain'] = df['Email'].apply(lambda x: 1 if is_disposable(x) else 0)

    # Extract TLD from website
    df['TLD'] = df['Website'].apply(
        lambda x: tldextract.extract(str(x)).suffix if pd.notnull(x) and str(x).strip() != '' else 'unknown'
    )

    # Email domain matches company name
    def email_company_match(row):
        if pd.isnull(row['Email']) or pd.isnull(row['Company']):
            return 0
        email_domain = row['Email'].split('@')[-1].lower().split('.')[0]
        company = str(row['Company']).lower().replace(" ", "")
        return 1 if email_domain in company or company in email_domain else 0

    df['EmailCompanyMatch'] = df.apply(email_company_match, axis=1)

    return df
