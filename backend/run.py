from app import create_app

app = create_app()


@app.shell_context_processor
def make_shell_context():
    from app.models import db, Product, Price, Shop, User
    return dict(db=db, Product=Product, Price=Price, Shop=Shop, User=User)
