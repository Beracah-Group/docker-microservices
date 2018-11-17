#!/usr/bin/env python3
import os

from core.src.api.v1.models import Location, Car, User, Service
from .denting.api.v1.models import Denting
from .washing.src.api.v1.models import Washing
from .service-package.api.v1.models import Servicepkg
from .service-pick&drop.src.api.v1.models import Pickanddrop

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app)
admin.add_view(ModelView(Servicepkg, databases.session))
admin.add_view(ModelView(Denting, databases.session))
admin.add_view(ModelView(Pickanddrop, databases.session))
admin.add_view(ModelView(Washing, databases.session))
admin.add_view(ModelView(Location, Car, User, Service, databases.session))

if __name__ == '__main__':
    manager.run()
