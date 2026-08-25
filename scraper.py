import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Verified free AARC-approved CEU sources
SOURCES = [
    {
        "name": "AARC Webcasts — Live & Archived",
        "url": "https://c.aarc.org/education/aarc_crce/index.asp",
        "badge": "Multi-Topic",
        "description": "AARC members earn free CRCE by viewing live webcasts. Members and non-members may view archived webcasts for free — CRCE credit available to those who pass an accompanying test.",
        "hours": "1.0+",
        "source_url": "https://c.aarc.org/education/aarc_crce/index.asp"
    },
    {
        "name": "CRCE Through the Journal",
        "url": "https://www.aarc.org/education/crce-through-the-journal/",
        "badge": "AARC Member Benefit",
        "description": "Earn up to 12 free CRCE each year. Each month, Respiratory Care journal offers 1.0 CRCE per issue. Read the first five articles and pass a 10-question post-test to earn credit.",
        "hours": "12.0/yr",
        "source_url": "https://www.aarc.org/education/crce-through-the-journal/"
    },
    {
        "name": "Dräger Free CRCE Webinars",
        "url": "https://www.draeger.com/en-us_us/Hospital/A-Breath-Ahead",
        "badge": "Neonatal / Critical Care",
        "description": "Free AARC-approved CRCE webinars from Dräger covering neonatal respiratory support, ventilator management, and best practices. Each program approved for 1.0 CRCE contact hour.",
        "hours": "1.0",
        "source_url": "https://www.draeger.com/en-us_us/Hospital/A-Breath-Ahead"
    },
    {
        "name": "Hamilton Medical e-Academy",
        "url": "https://www.hamilton-medical.com/en_US/Academy/e-Academy.html",
        "badge": "Mechanical Ventilation",
        "description": "Free online courses for healthcare professionals covering mechanical ventilation topics. Select modules offer AARC-approved CRCE credits. Learn at your own pace, on any device.",
        "hours": "Varies",
        "source_url": "https://www.hamilton-medical.com/en_US/Academy/e-Academy.html"
    },
    {
        "name": "Methapharm Free CRCE Courses",
        "url": "https://methapharmrespiratory.com/crce-courses/",
        "badge": "Multi-Topic",
        "description": "AARC and CSRT-approved on-demand courses at no cost to healthcare practitioners. Topics relevant to current clinical practice — available anytime to fit your schedule.",
        "hours": "1.0+",
        "source_url": "https://methapharmrespiratory.com/crce-courses/"
    },
    {
        "name": "Continued RT — Free Intro Course",
        "url": "https://www.continued.com/respiratory-therapy/free-ceu-course",
        "badge": "Multi-Topic",
        "description": "Try a free AARC-approved CEU course from Continued Respiratory Therapy — no credit card, no commitment. Evidence-based content from leading RT experts.",
        "hours": "1.0",
        "source_url": "https://www.continued.com/respiratory-therapy/free-ceu-course"
    },
        
    {
        "name": "Aerogen CEU-Accredited Education",
        "url": "https://education.aerogen.com/",
        "badge": "Aerosol / Drug Delivery",
        "description": "Free CEU-accredited webinars and modules on medical aerosol administration from Aerogen. Covers aerosol drug delivery in ventilated and non-ventilated patients across critical care and emergency settings.",
        "hours": "1.0+",
        "source_url": "https://education.aerogen.com/"
    },
    {
        "name": "Fisher & Paykel — Evidence in Action",
        "url": "https://www.fphcare.com/us/events/respiratory-care/evidence-in-action/",
        "badge": "High Flow / Humidification",
        "description": "Free access to Fisher & Paykel Evidence in ACTION webinars on-demand. Earn CRCE credits covering high flow therapy, humidification, and sleep therapy. Certificates emailed same day.",
        "hours": "1.0",
        "source_url": "https://www.fphcare.com/us/events/respiratory-care/evidence-in-action/"
    },
    {
        "name": "Vapotherm Academy — 20+ Free CEUs",
        "url": "https://academy.vapotherm.com/",
        "badge": "High Velocity Therapy",
        "description": "Over 20 free on-demand AARC-approved CRCE courses built by doctors, RTs, nurses, and coaches. Topics include high velocity therapy, ethics, COPD, hypercapnic respiratory failure, and post-extubation support.",
        "hours": "1.0 each",
        "source_url": "https://academy.vapotherm.com/"
    }]

# Sources that require JavaScript and can't be verified by simple HTTP check
ALWAYS_ACTIVE = [
    "https://education.aerogen.com/"
]

def check_source_active(url):
    """Check if a CEU source URL is still active"""
    # Some sites require JavaScript — whitelist them as always activeh
    if url in ALWAYS_ACTIVE:
        return True
    try:
        r = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 SmartRT CEU Checker'
        })
        return r.status_code == 200
    except:
        return False
def scrape_aarc_journal_courses():
    """Scrape current AARC journal course months"""
    try:
        r = requests.get(
            "https://www.aarc.org/education/crce-through-the-journal/",
            timeout=10,
            headers={'User-Agent': 'Mozilla/5.0 SmartRT CEU Checker'}
        )
        soup = BeautifulSoup(r.text, 'html.parser')
        # Look for month links
        links = soup.find_all('a', string=lambda t: t and 'Register for' in t)
        months = [l.get_text(strip=True) for l in links[:3]]
        return months
    except:
        return []

def build_ceu_list():
    """Build verified CEU list with live checking"""
    ceus = []
    for source in SOURCES:
        is_active = check_source_active(source['source_url'])
        ceu = {
            "id": source['name'].lower().replace(' ', '-').replace('&', 'and'),
            "name": source['name'],
            "badge": source['badge'],
            "description": source['description'],
            "hours": source['hours'],
            "url": source['url'],
            "active": is_active,
            "free": True,
            "aarc_approved": True
        }
        ceus.append(ceu)
        print(f"{'✅' if is_active else '❌'} {source['name']}")

    return ceus

if __name__ == "__main__":
    print(f"🫁 Smart RT CEU Scraper — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("Checking CEU sources...")

    ceus = build_ceu_list()
    active = [c for c in ceus if c['active']]

    # Get current AARC journal months
    journal_months = scrape_aarc_journal_courses()

    output = {
        "updated": datetime.now().isoformat(),
        "updated_display": datetime.now().strftime("%B %d, %Y"),
        "total_sources": len(ceus),
        "active_sources": len(active),
        "journal_current_months": journal_months,
        "ceus": ceus
    }

    with open('ceus.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n✅ Done! {len(active)}/{len(ceus)} sources active")
    print(f"📄 Saved to ceus.json")
