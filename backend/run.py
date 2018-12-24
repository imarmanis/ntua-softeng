from app import create_app

app = create_app()


@app.shell_context_processor
def make_shell_context():
    from app.models import db, Product
    return dict(db=db, Product=Product)
