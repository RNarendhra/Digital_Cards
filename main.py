from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="CargoCrew Digital Business Card"
)


# ============================================================
# PROJECT PATHS
# ============================================================

# Folder where this main.py file is located
BASE_DIR = Path(__file__).resolve().parent

# Templates folder
TEMPLATES_DIR = BASE_DIR / "templates"

# Static folder
STATIC_DIR = BASE_DIR / "static"


# ============================================================
# TEMPLATES
# ============================================================

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)


# ============================================================
# EMPLOYEE DATA
# ============================================================

employees = {

    "hakan": {
        "name": "Hakan Ikizoglu",
        "designation": "Chairman",
        "company": "CargoCrew",
        "mobile": "+971547955888",
        "email": "hakan.ikizoglu@cargocrew.aero",
        "website": "https://www.cargocrew.aero",
        "address": "P.O. Box 566624, Dubai, UAE",
        "order": 1
    },

    "tanzila": {
        "name": "Tanzila Rahim",
        "designation": "Director Strategic",
        "company": "CargoCrew",
        "mobile": "+971543916967",
        "email": "tanzila@cargocrew.aero",
        "website": "https://www.cargocrew.aero",
        "address": "P.O. Box 566624, Dubai, UAE",
        "order": 2
    },

    "houmam": {
        "name": "Houmam Baccora",
        "designation": "Head of Corporate Affairs",
        "company": "CargoCrew",
        "mobile": "+971544586866",
        "email": "houmam.baccora@cargocrew.aero",
        "website": "https://www.cargocrew.aero",
        "address": "P.O. Box 566624, Dubai, UAE",
        "order": 3
    },

    "asim": {
        "name": "Asim Aziz",
        "designation": "Head of Operations",
        "company": "CargoCrew",
        "mobile": "+971545621006",
        "email": "asim.aziz@cargocrew.aero",
        "website": "https://www.cargocrew.aero",
        "address": "P.O. Box 566624, Dubai, UAE",
        "order": 4
    },

    "volkan": {
        "name": "Volkan Yaren",
        "designation": "Commercial Director",
        "company": "CargoCrew",
        "mobile": "+971545625363",
        "email": "volkan@cargocrew.aero",
        "website": "https://www.cargocrew.aero",
        "address": "P.O. Box 566624, Dubai, UAE",
        "order": 5
    },

    "can": {
        "name": "Can Ikizoglu",
        "designation": "COO",
        "company": "CargoCrew",
        "mobile": "+971585785122",
        "email": "can.ikizoglu@cargocrew.aero",
        "website": "https://www.cargocrew.aero",
        "address": "P.O. Box 566624, Dubai, UAE",
        "order": 6
    },

    "sachin": {
        "name": "Sachin Sanesh",
        "designation": "Sales Manager",
        "company": "CargoCrew",
        "mobile": "+971549913255",
        "email": "sachin@cargocrew.aero",
        "website": "https://www.cargocrew.aero",
        "address": "P.O. Box 566624, Dubai, UAE",
        "order": 7
    },


    "Askari": {
        "name": "Muhammad Askari Aliya",
        "designation": "Sales & Operation Executive",
        "company": "CargoCrew",
        "mobile": "+971547074264",
        "email": "sales@stackntrack.ae",
        "website": "https://www.stackntrack.ae",
        "address": "Warehouse No. G01, Dubai Investment Park 2, Dubai, UAE",
        "order": 8
    }
}


# ============================================================
# HOME PAGE
# ============================================================

@app.get("/")
async def home(request: Request):

    # Sort employees according to their order number
    sorted_employees = sorted(
        employees.items(),
        key=lambda item: item[1].get("order", 999)
    )

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "employees": sorted_employees
        }
    )


# ============================================================
# DIGITAL BUSINESS CARD
# ============================================================

@app.get("/{slug}")
async def digital_card(request: Request, slug: str):

    employee = employees.get(slug)

    # Employee doesn't exist
    if employee is None:
        return {
            "error": "Employee not found",
            "available_employee": list(employees.keys())
        }

    return templates.TemplateResponse(
        request=request,
        name="card.html",
        context={
            "employee": employee
        }
    )
