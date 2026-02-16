import requests
from datetime import datetime 
import pytz

# CONFIG
posts = {
    "DIGITAL SERIES OF THE YEAR": {
        "GHOSTING": "ZmVlZGJhY2s6MTI5NzU5MjkzOTA2MDc5OA",
        "LOVE AT FIRST SPIKE": "ZmVlZGJhY2s6MTI5NzU5NTU3OTA2MDUzNA",
        "GOLDEN SCENERY OF TOMORROW": "ZmVlZGJhY2s6MTI5NzU5NjkzNTcyNzA2NQ",
        "HOW TO SPOT A RED FLAG": "ZmVlZGJhY2s6MTI5NzU5MTIzNTcyNzYzNQ",
        "BAD GENIUS": "ZmVlZGJhY2s6MTI5NzU4ODc1MjM5NDU1MA",
        "ALIBI": "ZmVlZGJhY2s6MTI5NzU5ODY4NTcyNjg5MA",
    },
    "FANDOM OF THE YEAR": {
        "JMFYANG": "ZmVlZGJhY2s6MTIyNzg3NDA5MjgxODU3MA",
        "DUSTBIA": "ZmVlZGJhY2s6MTIyNzg3MDgyMjgxODg5Nw",
        "CAPEATH": "ZmVlZGJhY2s6MTIyNzg0NjY1OTQ4Nzk4MA",
        "WILLCA": "ZmVlZGJhY2s6MTIyNzg0Mjg0OTQ4ODM2MQ",
        "KIMPAU": "ZmVlZGJhY2s6MTIyNzgzOTUzNjE1NTM1OQ",
        "ASHDRES": "ZmVlZGJhY2s6MTIyNzgzNjE3NjE1NTY5NQ",
    },
    "LOVETEAM OF THE YEAR": {
        "JMFYANG": "ZmVlZGJhY2s6MTIyNzc4MTIzNjE2MTE4OQ",
        "RABGEL": "ZmVlZGJhY2s6MTIyNzc5MDMyMjgyNjk0Nw",
        "DUSTBIA": "ZmVlZGJhY2s6MTIyNzc4Nzc3NjE2MDUzNQ",
        "ASHDRES": "ZmVlZGJhY2s6MTIyNzc4NTY3OTQ5NDA3OA",
        "KIMPAU": "ZmVlZGJhY2s6MTIyNzc4Mjg4OTQ5NDM1Nw",
        "WILLCA": "ZmVlZGJhY2s6MTIyNzc3OTQyOTQ5NDcwMw",
    },
    "MUSIC VIDEO OF THE YEAR": {
        "WHEREVER YOU ARE": "ZmVlZGJhY2s6OTE1MDA3OTQxMjM5MzY3",
        "MINAMAHAL": "ZmVlZGJhY2s6OTE1MDA1MjQ0NTcyOTcw",
        "HANGGANG DITO NA LANG BA TAYO?": "ZmVlZGJhY2s6OTE1MDAyMTkxMjM5OTQy",
        "WHAT IF TAYO?": "ZmVlZGJhY2s6OTE0OTk4NjcxMjQwMjk0",
        "NAIILANG": "ZmVlZGJhY2s6OTE0OTk1NzUxMjQwNTg2",
        "AYA": "ZmVlZGJhY2s6OTE0OTkyNzE0NTc0MjIz",
    },
    "BREAKTHROUGH STAR OF THE YEAR": {
        "FYANG": "ZmVlZGJhY2s6MTIyODA4Mzc0OTQ2NDI3MQ",
        "WILL": "ZmVlZGJhY2s6MTIyODA3OTgxNjEzMTMzMQ",
        "EMILIO": "ZmVlZGJhY2s6MTIyODA4NzAxMjc5NzI3OA",
        "KLARISSE": "ZmVlZGJhY2s6MTIyODA5MDA2Mjc5Njk3Mw",
        "FAITH": "ZmVlZGJhY2s6MTIyODA5MzY1Mjc5NjYxNA",
        "ANDRES": "ZmVlZGJhY2s6MTIyODA5NjY0Mjc5NjMxNQ",
    },
    "NEW MALE TV PERSONALITY": {
        "JM": "ZmVlZGJhY2s6MTIyODA1MDkzOTQ2NzU1Mg",
        "MATTHEW": "ZmVlZGJhY2s6MTIyODA0NDg4MjgwMTQ5MQ",
        "ANTON": "ZmVlZGJhY2s6MTIyODA0MTU2OTQ2ODQ4OQ",
        "RIVER": "ZmVlZGJhY2s6MTIyODAzODE4NjEzNTQ5NA",
        "RALPH": "ZmVlZGJhY2s6MTIyODAzNDM0MjgwMjU0NQ",
        "DYLAN": "ZmVlZGJhY2s6MTIyODA1NDAwNjEzMzkxMg",
    },
}
fb_dtsg = "NAftSGxIH9AA8B7cF4KEPlkV91fVtVk8BBF6PCwammW74JUDqwbQUFw:16:1756974490"
lsd = "Uq25aBYrQLNcHbwzY-RgZy"
jazoest = "25363"

headers = {
    "accept": "*/*",
    "content-type": "application/x-www-form-urlencoded",
    "x-asbd-id": "359341",
    "x-fb-lsd": lsd
}

graphql_url = "https://www.facebook.com/api/graphql/"
PH_TZ = pytz.timezone("Asia/Manila")

# ---------------- FUNCTIONS ----------------
def fetch_graphql(doc_id, variables, friendly_name):
    data = {
        "fb_dtsg": fb_dtsg,
        "jazoest": jazoest,
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": friendly_name,
        "variables": str(variables).replace("'", '"'),
        "doc_id": doc_id,
        "server_timestamps": "true"
    }
    response = requests.post(graphql_url, headers=headers, data=data, cookies={})
    try:
        return response.json()
    except Exception as e:
        print(f"Failed to parse response for {friendly_name}: {e}")
        return None

def fetch_rankings():
    rankings = {}
    for category, posts_dict in posts.items():
        post_data = []
        for post_name, post_id in posts_dict.items():
            reactions_data = fetch_graphql(
                "24051433444544934",
                {"feedbackTargetID": post_id, "scale": 1},
                "CometUFIReactionsDialogQuery"
            )
            reactions_summary = reactions_data.get("data", {}).get("node", {}).get("top_reactions", {}).get("summary", [])
            reaction_count = next(
                (reaction['reaction_count'] for reaction in reactions_summary 
                 if reaction['reaction']['id'] == '613557422527858'), 0
            )

            shares_data = fetch_graphql(
                "9843821265734688",
                {"feedbackTargetID": post_id},
                "CometUFISharesCountTooltipContentQuery"
            )
            total_shares = shares_data.get("data", {}).get("feedback", {}).get("reshares", {}).get("count", 0)

            total_react_and_share = reaction_count + total_shares
            post_data.append((post_name, reaction_count, total_shares, total_react_and_share))

        sorted_posts = sorted(post_data, key=lambda x: x[3], reverse=True)
        rankings[category] = sorted_posts
    return rankings

def generate_html(rankings):
    current_time = datetime.now(PH_TZ).strftime("%Y-%m-%d %H:%M:%S")
    tables_html = ""

    for category, posts_list in rankings.items():
        tables_html += f"<h2>{category}</h2>"
        tables_html += """
<table border="1" cellpadding="5">
    <tr>
        <th>Rank</th>
        <th>Post Name</th>
        <th>Reactions</th>
        <th>Shares</th>
        <th>Total</th>
        <th>Difference (1st vs 2nd)</th>
    </tr>
"""
        first_post = posts_list[0]
        second_post = posts_list[1] if len(posts_list) > 1 else None
        if second_post:
            reactions_diff = first_post[1] - second_post[1]
            shares_diff = first_post[2] - second_post[2]
            total_diff = first_post[3] - second_post[3]
            diff_text = f"Reactions: {reactions_diff}, Shares: {shares_diff}, Total: {total_diff}"
        else:
            diff_text = "Not enough posts to compare"

        for rank, (post_name, reactions, shares, total) in enumerate(posts_list, 1):
            tables_html += f"""
    <tr>
        <td>{rank}</td>
        <td>{post_name}</td>
        <td>{reactions}</td>
        <td>{shares}</td>
        <td>{total}</td>
        <td>{diff_text if rank == 1 else ''}</td>
    </tr>
"""
        tables_html += "</table><br>"

    html_content = f"""
<html>
<head>
    <title>Facebook Post Rankings</title>
</head>
<body>
    <h1>Facebook Post Rankings</h1>
    <p id="last-update">Last update: {current_time}</p>

    <div id="rankings-table">
        {tables_html}
    </div>

    <script>
        // Live tracker: poll latest index.html every 10 seconds
        async function fetchLatest() {{
            try {{
                const response = await fetch(window.location.href + "?cache_bust=" + new Date().getTime());
                const text = await response.text();
                const parser = new DOMParser();
                const doc = parser.parseFromString(text, "text/html");
                const newTable = doc.getElementById("rankings-table");
                const newTime = doc.getElementById("last-update");
                if(newTable && newTime) {{
                    document.getElementById("rankings-table").innerHTML = newTable.innerHTML;
                    document.getElementById("last-update").innerHTML = newTime.innerHTML;
                }}
            }} catch(err) {{
                console.log("Failed to fetch latest rankings:", err);
            }}
        }}
        setInterval(fetchLatest, 10000);
    </script>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✓ index.html updated successfully")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    rankings = fetch_rankings()
    generate_html(rankings)


