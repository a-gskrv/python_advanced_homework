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
    Boolean,
    func,
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
# HOMEWORK 4
#############################

# 1
category_1 = Category(name="Электроника", description="Гаджеты и устройства.")
session.add(category_1)
category_2 = Category(name="Книги", description="Печатные книги и электронные книги.")
session.add(category_2)
category_3 = Category(name="Одежда", description="Одежда для мужчин и женщин.")
session.add(category_3)
session.commit()


product_1 = Product(name="Смартфон", price=299.99, in_stock=True, category_id=category_1.id)
session.add(product_1)
product_2 = Product(name="Ноутбук", price=499.99, in_stock=True, category_id=category_1.id)
session.add(product_2)
product_3 = Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category_id=category_2.id)
session.add(product_3)
product_4 = Product(name="Джинсы", price=40.50, in_stock=True, category_id=category_3.id)
session.add(product_4)
product_5 = Product(name="Футболка", price=20.00, in_stock=True, category_id=category_3.id)
session.add(product_5)
session.commit()

# 2
print("-"*20, 2, "-"*20)
def print_tables():
    stmt = (select(Category))
    result = session.execute(stmt).scalars()
    for i, cat in enumerate(result, start=1):
        print(f"{i}. {cat.name} ({cat.description}):")
        for k, product in enumerate(cat.products, start=1):
            print(f"\t {i}.{k} - {product.name} - ${product.price:.2f} - "
                  f"({"в наличии" if product.in_stock else "нет на складе"})")

print_tables()


# 3
print("-"*20, 3, "-"*20)
stmt = (
    select(Product)
    .where(Product.name.like("%Смартфон%"))
)
result3 = session.execute(stmt).scalars()
for i, product in enumerate(result3, start=1):
    product.price = 349.99
    session.commit()
    break

print_tables()


# 4
print("-"*20, 4, "-"*20)
stmt = (
    select(func.count(Product.id).label("count"), Product.category_id.label("category_id"))
    .group_by(Product.category_id)
)

result4 = session.execute(stmt).all()
for i, prod in enumerate(result4, start=1):
    print(f"category {prod.category_id} - count {prod.count}")


# 5
print("-"*20, 5, "-"*20)
stmt = (
    select(func.count(Product.id).label("count"), Product.category_id.label("category_id"))
    .group_by(Product.category_id)
    .having(func.count(Product.id).label("count") > 1)
)

result4 = session.execute(stmt).all()
for i, prod in enumerate(result4, start=1):
    print(f"category {prod.category_id} - count {prod.count}")