import os

from fastapi.templating import Jinja2Templates

import config
from utils import filtros_jinja as fj


full_path = os.path.realpath(__file__)
path = os.path.dirname(full_path)
templates = Jinja2Templates(directory=os.path.join(path, "templates"))
templates.env.globals["nome_app"] = config.NOME_APP
templates.env.filters["formatar_data"] = fj.formatar_data
