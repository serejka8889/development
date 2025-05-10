"""
tasks
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
		CREATE TABLE IF NOT EXISTS tasks (
		    id SERIAL PRIMARY KEY,
		    title VARCHAR(255) NOT NULL,
		    description TEXT,
		    deadline DATE,
		    status BOOL
            );
        """,
        """
            drop table if exists tasks cascade;
        """
    )
]
