from .constellation import run as constellation_run

def selectWeb(site, params):
    if site == "constellation":
        return constellation_run(params)
         
    return {"error": "unknown site"}
