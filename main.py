from pathlib import Path

from fastapi import FastAPI, Request, Response, HTTPException
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
        "mobile": "+971544586966",
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
        "name": "Sachin Sandesh",
        "designation": "Sales Manager",
        "company": "CargoCrew",
        "mobile": "+971549913255",
        "email": "sachin@cargocrew.aero",
        "website": "https://www.cargocrew.aero",
        "address": "P.O. Box 566624, Dubai, UAE",
        "order": 7
    },

    "Shaima": {
        "name": "Shaima Jaison",
        "designation": "Senior Sales Executive",
        "company": "CargoCrew",
        "mobile": "+971 54 5083066",
        "email": "shaima@cargocrew.aero",
        "website": "https://www.cargocrew.aero",
        "address": "P.O. Box 566624, Dubai, UAE",
        "order": 8
    },

    "Askari": {
        "name": "Muhammad Askari Aliya",
        "designation": "Sales & Operation Executive",
        "company": "CargoCrew",
        "mobile": "+971547074264",
        "email": "askari@cargocrew.aero",
        "website": "https://www.cargocrew.aero",
        "address": "Warehouse No. G01, Dubai Investment Park 2, Dubai, UAE",
        "order": 9
    }

}


# ============================================================
# VCARD & HELPER FUNCTIONS
# ============================================================

def find_employee(slug: str):
    """Find employee by slug with case-insensitive fallback."""
    if slug in employees:
        return slug, employees[slug]
    slug_lower = slug.lower()
    for key, val in employees.items():
        if key.lower() == slug_lower:
            return key, val
    return None, None


def generate_vcard(employee: dict) -> str:
    """Generate standard RFC 6350 / 2426 vCard 3.0 string with CRLF line endings."""
    name = employee.get("name", "").strip()
    name_parts = name.split()
    if len(name_parts) > 1:
        first_name = " ".join(name_parts[:-1])
        last_name = name_parts[-1]
    else:
        first_name = name
        last_name = ""

    company = employee.get("company", "CargoCrew").strip()
    designation = employee.get("designation", "").strip()
    mobile = employee.get("mobile", "").strip()
    clean_mobile = mobile.replace(" ", "")
    email = employee.get("email", "").strip()
    website = employee.get("website", "").strip()
    address = employee.get("address", "").strip()

    escaped_address = address.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")

    vcard_lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:{last_name};{first_name};;;",
        f"FN:{name}",
        f"ORG:{company}",
        f"TITLE:{designation}",
        f"TEL;TYPE=CELL,VOICE:{clean_mobile}",
        f"EMAIL;TYPE=WORK,INTERNET:{email}",
        f"URL:{website}",
        f"ADR;TYPE=WORK;CHARSET=UTF-8:;;{escaped_address};;;;",
        f"LABEL;TYPE=WORK;CHARSET=UTF-8:{escaped_address}",
        "NOTE;CHARSET=UTF-8:CargoCrew Digital Business Card",
        "END:VCARD",
    ]
    return "\r\n".join(vcard_lines) + "\r\n"


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
# VCARD DOWNLOAD (SAFE DOWNLOAD ENDPOINT)
# ============================================================

@app.get("/{slug}/vcf")
@app.get("/{slug}/vcard")
@app.get("/{slug}/contact.vcf")
async def download_vcard(slug: str):
    emp_slug, employee = find_employee(slug)

    # Employee doesn't exist
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    vcard_content = generate_vcard(employee)
    safe_name = "".join(c for c in employee["name"] if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
    filename = f"{safe_name}.vcf"

    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"; filename*=UTF-8\'\'{filename}',
        "Content-Type": "text/vcard; charset=utf-8",
        "X-Content-Type-Options": "nosniff",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0",
    }

    return Response(
        content=vcard_content.encode("utf-8"),
        media_type="text/vcard; charset=utf-8",
        headers=headers
    )


# ============================================================
# DIGITAL BUSINESS CARD
# ============================================================

@app.get("/{slug}")
async def digital_card(request: Request, slug: str):

    emp_slug, employee = find_employee(slug)

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
            "employee": employee,
            "slug": emp_slug
        }
    )
