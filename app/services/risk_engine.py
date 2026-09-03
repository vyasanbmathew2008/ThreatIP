def calculate_risk(ip_info: dict, behavior: dict) -> dict:
    score = 0
    reasons = []

    requests = behavior.get("requests_last_5m", 0)
    failed = behavior.get("failed_logins_last_5m", 0)

    if requests > 50:
        score += 25
        reasons.append("High request frequency")
    elif requests > 20:
        score += 15
        reasons.append("Elevated request frequency")

    if failed >= 10:
        score += 30
        reasons.append("Many failed login attempts")
    elif failed >= 3:
        score += 20
        reasons.append("Repeated failed login attempts")

    org = (ip_info.get("org") or "").lower()
    isp = (ip_info.get("isp") or "").lower()
    datacenter_terms = ("amazon", "aws", "google cloud", "microsoft", "azure", "digitalocean", "ovh", "hetzner")
    if any(term in org or term in isp for term in datacenter_terms):
        score += 20
        reasons.append("Possible hosting/datacenter network")

    score = min(score, 100)
    if score >= 80:
        level, action = "high", "block"
    elif score >= 50:
        level, action = "medium", "challenge"
    else:
        level, action = "low", "allow"

    return {"score": score, "level": level, "action": action, "reasons": reasons}
