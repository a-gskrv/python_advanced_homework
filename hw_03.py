import decimal

from sqlalchemy import (
    select,
    create_engine,
    # BigInteger,
    ForeignKey,
    Integer,
    DECIMAL,
    # SmallInteger,
    String,
    Boolean
)

from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)


engine = create_engine("sqlite:///:memory:")


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True
    )


class Product(Base):
    __tablename__ = "product"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    price: Mapped[decimal.Decimal] = mapped_column(
        DECIMAL(15,2),
        nullable=True
    )

    in_stock: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    #FK
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("category.id"),
        nullable=False
    )

    # relationships
    category = relationship(
        "Category",
        back_populates="products",

    )

class Category(Base):
    __tablename__ = "category"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(250),
        nullable=True
    )


    # relationships
    products = relationship(
        "Product",
        back_populates="category",
    )


Session = sessionmaker(
    bind=engine,
)
session = Session()


Base.metadata.create_all(engine)

#############################
# test
category_1 = Category(name="Laptops", description="Laptops")
session.add(category_1)
category_2 = Category(name="Smartphones")
session.add(category_2)
category_3 = Category(name="Keyboards")
session.add(category_3)
category_4 = Category(name="Monitors")
session.add(category_4)
session.commit()

product_1 = Product(name="Dell 14' 1200", price=520.00, in_stock=True, category_id=category_1.id)
session.add(product_1)
product_2 = Product(name="Asus 15' 1000", price=820.00, in_stock=True, category_id=category_1.id)
session.add(product_2)
product_3 = Product(name="Apple iPhone' 17", price=1520.00, in_stock=True, category_id=category_2.id)
session.add(product_3)
product_4 = Product(name="Samsung 24'", price=150.00, in_stock=True, category_id=category_4.id)
session.add(product_4)

session.commit()


for c in session.scalars(select(Category)).all():
    print(f"{c.name}:")
    for p in c.products:
        print("\t", p.name, p.price, p.in_stock, sep=" - ")


# print(Base.metadata.tables)