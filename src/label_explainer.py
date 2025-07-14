def explain_flags(row):
    flags = []

    if row.get("WebsiteHTTPS") == 0:
        flags.append("Unsecure website")

    if row.get("HasDisposableDomain") == 1:
        flags.append("Disposable email domain")

    if row.get("MissingFields", 0) >= 2:
        flags.append("Too many missing fields")

    if row.get("EmailCompanyMatch") == 0:
        flags.append("Email & company mismatch")

    if row.get("EmailLength", 0) <= 5:
        flags.append("Unusually short email")

    if not flags:
        return "All checks passed"
    return ", ".join(flags)
