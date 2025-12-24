from .constellation import run as constellation_run
from .name import run as name_run
def selectWeb(site, params):
    if site == "constellation":
        return constellation_run(params)
    elif site == "name":
        return name_run(params)
    return {"error": "unknown site"}

# constellation parameters: [year, month, date]
# example: ["2023", "03", "15"]
