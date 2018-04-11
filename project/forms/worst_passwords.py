from project import app
with app.open_resource('forms/WORST_PASSES.txt') as f:
    WORST_PASSWORDS = [line.strip() for line in f]
    TOTAL_WORST_PASSWORDS = len(WORST_PASSWORDS)