#!/usr/bin/env bash
read -d '' COMMANDS <<END
import project
from project.models import migrate
migrate.do_migrate()
END

echo "running migration..."
python <<< "$COMMANDS"