
import openai, requests, os, random
from datetime import datetime

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GUMROAD_KEY = os.getenv("GUMROAD_API_KEY")

topics = [
    "Mastering AI for Business",
    "Ultimate ChatGPT Side Hustle Course",
    "Learn Digital Marketing with AI",
    "AI Freelancing Secrets",
    "Productivity and Time Management Masterclass",
    "High-Income Skills with AI Tools",
    "Personal Growth & Success System",
    "How to Start an Online Business Fast",
    "AI Prompt Engineering Bootcamp",
    "Earn Money Online with Automation"
]

def generate_course_content(topic):
    prompt = f"""Create a premium online course on '{topic}'.
    Include:
    - 8 video lesson scripts (detailed)
    - 1 complete PDF workbook (Markdown)
    - A professional course description (sales copy)
    Make it structured and high-value."""
    r = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role":"user","content":prompt}],
        max_tokens=7000
    )
    return r.choices[0].message["content"]

def save_course(content, topic):
    filename = f"courses/{topic.replace(' ','_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
    os.makedirs("courses", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

def upload_to_gumroad(file_path, title, price):
    url = "https://api.gumroad.com/v2/products"
    data = {
        "access_token": GUMROAD_KEY,
        "name": title + " (Full Course)",
        "price": price,
        "description": f"A premium course on {title}. Includes 8 video lessons and a PDF workbook. PayPal: fargnom14@gmail.com",
        "custom_permalink": title.lower().replace(" ", "-"),
        "tags": "online course, ai, business, freelancing, productivity, success",
        "published": True
    }
    files = {"file": open(file_path, "rb")}
    return requests.post(url, data=data, files=files).json()

if __name__ == "__main__":
    for _ in range(2):  # 2 full courses per run (8 per day)
        topic = random.choice(topics)
        content = generate_course_content(topic)
        file_path = save_course(content, topic)
        gumroad_res = upload_to_gumroad(file_path, topic, random.choice([4900, 7900, 9900, 14900]))  # €49-149
        print("Uploaded premium course:", gumroad_res)
