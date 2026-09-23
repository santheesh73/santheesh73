import os
import re
import urllib.request
import json

def fetch_streak_svg():
    url = "https://streak-stats.demolab.com?user=santheesh73&theme=tokyonight&hide_border=true&timezone=Asia/Kolkata"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    with urllib.request.urlopen(req, timeout=15) as res:
        return res.read().decode("utf-8")

def get_token_contributions(token):
    if not token:
        return None
    query = """
    query {
      viewer {
        contributionsCollection {
          contributionCalendar {
            totalContributions
          }
        }
      }
    }
    """
    try:
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": query}).encode("utf-8"),
            headers={
                "User-Agent": "Mozilla/5.0",
                "Authorization": f"bearer {token}",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read().decode("utf-8"))
            return data["data"]["viewer"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    except Exception as e:
        print(f"GraphQL query note: {e}")
        return None

def main():
    token = os.environ.get("STREAK_STATS_TOKEN") or os.environ.get("GITHUB_TOKEN")
    
    print("Fetching latest streak SVG from endpoint...")
    svg = fetch_streak_svg()
    
    # Extract base total contributions from SVG
    m = re.search(r'<!-- Total Contributions big number -->.*?<text[^>]*>\s*(\d+)\s*</text>', svg, re.DOTALL)
    if not m:
        print("Could not find Total Contributions in SVG. Writing raw SVG.")
        final_svg = svg
    else:
        base_val = int(m.group(1))
        
        # User has verified real contribution baseline of 472
        # (accounting for private/organization repository contributions)
        token_total = get_token_contributions(token)
        
        # Base count from public API was ~320 when verified total was 472 (offset = 152)
        calculated_total = base_val + 152
        if token_total:
            calculated_total = max(calculated_total, token_total + 152)
        
        real_total = max(472, calculated_total)
        print(f"Base count: {base_val} | Real total calculated: {real_total}")
        
        # Replace big number
        final_svg = re.sub(
            r'(<!-- Total Contributions big number -->.*?<text[^>]*>\s*)(\d+)(\s*</text>)',
            r'\g<1>' + str(real_total) + r'\g<3>',
            svg,
            flags=re.DOTALL
        )

    out_path = os.path.join("assets", "streak.svg")
    os.makedirs("assets", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(final_svg)
    print(f"Successfully updated {out_path}!")

if __name__ == "__main__":
    main()
