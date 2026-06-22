"""Update publication categories from generic 'Journal Article' to topic-specific tags."""
import re
from pathlib import Path

# Map slug -> new categories
UPDATES = {
    "Lang-2019":          ["research", "trend analysis", "air quality", "meteorological normalisation"],
    "acp-19-7519-2019":   ["research", "air quality"],
    "budisulistiorini-2026": ["research", "mobile monitoring", "VOC", "indoor air quality"],
    "carslaw-2001-a":     ["research", "air quality", "NOx", "particulate matter"],
    "carslaw-2001-b":     ["research", "atmospheric chemistry", "air quality"],
    "carslaw-2001":       ["research", "air quality", "NOx", "air quality modelling"],
    "carslaw-2002-a":     ["research", "dispersion modelling", "air quality modelling"],
    "carslaw-2002-b":     ["research", "vehicle emissions", "emissions inventory"],
    "carslaw-2002-c":     ["research", "air quality", "NOx", "air quality modelling"],
    "carslaw-2002-d":     ["research", "low emission zones", "NOx", "policy"],
    "carslaw-2002":       ["research", "air quality", "particulate matter", "air quality modelling"],
    "carslaw-2004-a":     ["research", "vehicle emissions", "NOx", "policy"],
    "carslaw-2004":       ["research", "NOx", "street canyon", "air quality modelling"],
    "carslaw-2005-a":     ["research", "vehicle emissions", "NOx"],
    "carslaw-2005-b":     ["research", "vehicle emissions", "NOx"],
    "carslaw-2005-c":     ["research", "ozone", "trend analysis"],
    "carslaw-2005-d":     ["research", "vehicle emissions", "congestion charging", "policy"],
    "carslaw-2005-e":     ["research", "vehicle emissions", "congestion charging", "policy"],
    "carslaw-2005":       ["research", "vehicle emissions", "NOx", "emissions inventory"],
    "carslaw-2006-a":     ["research", "airport emissions", "NOx"],
    "carslaw-2006-b":     ["research", "vehicle emissions", "particulate matter", "policy"],
    "carslaw-2006":       ["research", "vehicle emissions", "air quality", "data analysis"],
    "carslaw-2007-a":     ["research", "NOx", "trend analysis", "air quality"],
    "carslaw-2007-b":     ["research", "atmospheric chemistry", "ozone"],
    "carslaw-2007-c":     ["research", "vehicle emissions", "air quality", "data analysis"],
    "carslaw-2007-d":     ["research", "vehicle emissions", "trend analysis", "data analysis"],
    "carslaw-2007-e":     ["research", "vehicle emissions", "air quality", "policy"],
    "carslaw-2007-f":     ["research", "NOx", "vehicle emissions", "policy"],
    "carslaw-2007":       ["research", "air quality", "street canyon", "dispersion modelling"],
    "carslaw-2008":       ["research", "airport emissions", "NOx"],
    "carslaw-2009-b":     ["research", "atmospheric chemistry", "trend analysis", "data analysis"],
    "carslaw-2009":       ["research", "air quality", "source apportionment", "data analysis"],
    "carslaw-2010":       ["research", "vehicle emissions", "policy"],
    "carslaw-2011-a":     ["research", "vehicle emissions", "NOx", "emissions inventory"],
    "carslaw-2011":       ["research", "vehicle emissions", "NOx", "policy"],
    "carslaw-2012-a":     ["research", "air quality modelling", "dispersion modelling", "NOx"],
    "carslaw-2012-b":     ["research", "openair", "data analysis", "air quality"],
    "carslaw-2012-c":     ["research", "openair", "data analysis", "air quality"],
    "carslaw-2012-d":     ["research", "vehicle emissions", "NOx", "trend analysis"],
    "carslaw-2012":       ["research", "airport emissions", "air quality"],
    "carslaw-2013-a":     ["research", "source apportionment", "data analysis", "openair"],
    "carslaw-2013-b":     ["research", "air quality modelling"],
    "carslaw-2013-c":     ["research", "vehicle emissions", "NOx", "remote sensing"],
    "carslaw-2013-d":     ["research", "vehicle emissions", "NOx", "remote sensing"],
    "carslaw-2013":       ["research", "dispersion modelling", "air quality modelling", "air quality"],
    "carslaw-2014-a":     ["research", "indoor air quality"],
    "carslaw-2014-b":     ["research", "indoor air quality", "air quality modelling"],
    "carslaw-2014":       ["research", "source apportionment", "data analysis"],
    "carslaw-2015-a":     ["research", "air quality modelling"],
    "carslaw-2015-b":     ["research", "NOx", "emissions inventory"],
    "carslaw-2015-c":     ["research", "vehicle emissions", "NOx", "policy"],
    "carslaw-2015-d":     ["research", "vehicle emissions", "NOx", "policy"],
    "carslaw-2015":       ["research", "indoor air quality", "particulate matter", "atmospheric chemistry"],
    "carslaw-2016-a":     ["research", "vehicle emissions", "NOx", "trend analysis"],
    "carslaw-2016-b":     ["research", "source apportionment", "data analysis"],
    "carslaw-2016-c":     ["research", "NOx", "emissions inventory"],
    "carslaw-2016-d":     ["research", "air quality"],
    "carslaw-2016":       ["research", "NOx", "emissions inventory", "trend analysis"],
    "carslaw-2019":       ["research", "vehicle emissions", "NOx", "trend analysis"],
    "grange-2017":        ["research", "vehicle emissions", "NOx", "emissions inventory", "policy"],
    "grange-2019":        ["research", "meteorological normalisation", "trend analysis", "air quality"],
    "temperature-2019":   ["research", "vehicle emissions", "NOx"],
}

pub_dir = Path(__file__).parent.parent / "publications"

# Match the categories block in YAML front matter
# Handles both `- tag` and `  - tag` style, ending at next key or ---
CAT_PATTERN = re.compile(
    r"^(categories:\n)(?:[ \t]*-[^\n]*\n)+",
    re.MULTILINE,
)

changed = []
skipped = []

for slug, categories in UPDATES.items():
    qmd = pub_dir / slug / "index.qmd"
    if not qmd.exists():
        print(f"  MISSING: {qmd}")
        continue

    text = qmd.read_text()
    new_cats = "categories:\n" + "".join(f"  - {c}\n" for c in categories)

    new_text, n = CAT_PATTERN.subn(new_cats, text, count=1)
    if n == 0:
        skipped.append(slug)
        print(f"  NO MATCH: {slug}")
    elif new_text == text:
        skipped.append(slug)
        print(f"  UNCHANGED: {slug}")
    else:
        qmd.write_text(new_text)
        changed.append(slug)

print(f"\nUpdated {len(changed)} files, skipped {len(skipped)}")
print("Changed:", changed)
