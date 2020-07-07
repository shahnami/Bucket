# If weight is 1 (default), the get_high_score function will only take into consideration the amount of matches
# if weight is != 1, the get_high_score function will treat the weight as a priority (hence why priority weights start from 100)

WEIGHTS: dict = {
    "OWA Collection": 106,
    "VPN Collection": 105,
    "Staging Collection": 104,
    "None Collection": 103,
    "Auth Collection": 102,
    "AWS Collection": 101,
    "Client Collection": 100,
    "DNS Collection": 100,
}
