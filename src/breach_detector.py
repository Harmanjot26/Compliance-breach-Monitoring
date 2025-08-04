import pandas as pd

def detect_breaches(df):
    df['exposure_breach'] = df['exposure'] > df['limit']
    df['nav_missing'] = df['nav'].isna() | (df['nav'] < 1.0)
    df['kyc_flag'] = df['kyc_status'] != 'current'

    # Filter rows where any breach condition is True
    breaches = df[df[['exposure_breach','nav_missing','kyc_flag']].any(axis=1)].copy()

    # Label the breach types
    def get_breach_types(row):
        types = []
        if row['exposure_breach']: types.append('Exposure Limit Breach')
        if row['nav_missing']: types.append('NAV Missing')
        if row['kyc_flag']: types.append('KYC Expired')
        return ', '.join(types)

    breaches['breach_types'] = breaches.apply(get_breach_types, axis=1)

    return breaches[['transaction_id', 'client_id', 'timestamp', 'breach_types']]
