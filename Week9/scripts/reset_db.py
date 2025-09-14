import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.app import create_app
from scripts.db_utils import ensure_db_ready

app = create_app()

with app.app_context():
    ensure_db_ready()
    print("✅ All tables created successfully")
