from urllib.parse import urlencode
from urllib.request import urlopen


# Bare-bones AllWISE cone search around a sky position.
IRSA_GATOR = "https://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-query"


# Hard-coded target for quick testing.
target_name = "Gliese 300"
radius_arcsec = 30.0


# Build the IRSA Gator query URL.
params = {
    "catalog": "allwise_p3as_psd",
    "spatial": "cone",
    "radius": str(radius_arcsec),
    "radunits": "arcsec",
    "objstr": target_name,
    "outfmt": "1",
    "selcols": "designation,ra,dec,w1mpro,w1sigmpro,w2mpro,w2sigmpro",
}
url = f"{IRSA_GATOR}?{urlencode(params)}"


# Download the raw IPAC table as text.
with urlopen(url, timeout=20) as response:
    text = response.read().decode("utf-8", errors="replace")


# Keep the nearest source that has at least one of W1 or W2.
best = None
for line in text.splitlines():
    s = line.strip()
    if not s or s.startswith("\\") or s.startswith("|"):
        continue

    # Expected row format:
    # designation ra dec clon clat w1mpro w1sigmpro w2mpro w2sigmpro dist angle
    parts = s.split()
    if len(parts) < 11:
        continue

    try:
        dist_arcsec = float(parts[9])
    except ValueError:
        continue

    w1 = None if parts[5].lower() == "null" else float(parts[5])
    w1_err = None if parts[6].lower() == "null" else float(parts[6])
    w2 = None if parts[7].lower() == "null" else float(parts[7])
    w2_err = None if parts[8].lower() == "null" else float(parts[8])
    if w1 is None and w2 is None:
        continue

    row = {
        "designation": parts[0],
        "ra_deg": float(parts[1]),
        "dec_deg": float(parts[2]),
        "w1mpro": w1,
        "w1sigmpro": w1_err,
        "w2mpro": w2,
        "w2sigmpro": w2_err,
        "dist_arcsec": dist_arcsec,
    }
    if best is None or row["dist_arcsec"] < best["dist_arcsec"]:
        best = row


# Print the best match, or None if nothing useful was found.
print(best)

W1 = best['w1mpro']
W1_ERR = best['w1sigmpro']
W2 = best['w2mpro']
W2_ERR = best['w2sigmpro']