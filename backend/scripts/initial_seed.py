import asyncio
from json import loads
from pathlib import Path
import app.database.models_registry
from app.database.connection import AsyncSessionLocal
from app.categories.services import (
    create_category_service, 
    create_subcategory_service
)
from app.users.services import create_user_service
from app.products.services import (
    create_product_service, 
    create_product_review_service, 
    create_variant_service
)
from app.products.models import TargetKey
from app.reviews.services import create_site_review_service
from app.users.schemas import UserSchema, UserCreateSchema
from app.categories.schemas import (
    CategoryCreateSchema, 
    SubCategoryCreateSchema, 
    CategorySchema, 
    SubCategorySchema
)
from app.reviews.schemas import SiteReviewCreateSchema
from app.products.schemas import (
    ProductCreateSchema, 
    ProductReviewCreateSchema, 
    ProductVariantCreateSchema, 
    ProductSchema,
    ProductVariantNestedCreateSchema
)
from app.core.utils import create_slug

from faker import Faker


fake = Faker("it_IT")



DATA_DIR = Path(__file__).resolve().parent / "data"

PRODUCTS_PATH = DATA_DIR / "prodotti2.json"
CATEGORIES_PATH = DATA_DIR / "prodotti_slug.json"
PRODUCT_REVIEWS_PATH = DATA_DIR / "recensioniProdotti.json"
REVIEWS_PATH = DATA_DIR / "recensioni.json"


def read_json(path: Path):
    with open(path, encoding="utf-8") as file:
        return loads(file.read())


def to_cents(price: float) -> int:
    return round(price * 100)


def distribute_stock(total: int, n_variants: int) -> list[int]:
    """
    divide the stock between the variants of a product
    """
    
    if n_variants == 0:
        return []
    base, remainder = divmod(total, n_variants)
    return [base + 1 if i < remainder else base for i in range(n_variants)]


async def seed() -> None:
    products_data = read_json(PRODUCTS_PATH)
    categories_data = read_json(CATEGORIES_PATH)["products"]
    product_reviews_data = read_json(PRODUCT_REVIEWS_PATH)
    reviews_data = read_json(REVIEWS_PATH)

    categories_raw: dict[str, dict] = {}
    subcategories_raw: dict[str, dict] = {}
    
    # product_id -> {category_slug, subcategory_slug}
    product_meta: dict[int, dict] = {}  

    for item in categories_data:
        category = item["category"]
        subcategory = item["subcategory"]

        categories_raw.setdefault(category["slug"], {"name": category["name"], "slug": category["slug"]})
        subcategories_raw.setdefault(
            subcategory["slug"],
            {"name": subcategory["name"], "slug": subcategory["slug"], "category_slug": category["slug"]},
        )
        product_meta[item["id"]] = {
            "category_slug": category["slug"],
            "subcategory_slug": subcategory["slug"],
        }

    async with AsyncSessionLocal() as session:
        
        # users 
        fake_users: list[UserSchema] = []
        FAKE_USERS_COUNT = 20
        for _ in range(FAKE_USERS_COUNT):
            name = fake.first_name()
            surname = fake.last_name()
            email = fake.unique.email()
            password = fake.password(
                digits=True,
                upper_case=True,
                lower_case=True,
                special_chars=False,
                length=8,
            )
            payload = UserCreateSchema(
                name=name,
                surname=surname,
                email=email,
                password=password,
            )
            user = await create_user_service(payload, session, is_admin=False)
            fake_users.append(user)

        # categories
        category_objs: dict[str, CategorySchema] = {}
        for slug, data in categories_raw.items():
            category = await create_category_service(
                session,
                CategoryCreateSchema(
                    name=data["name"],
                    slug=slug,
                ),
            )
            category_objs[slug] = category
        await session.flush() 

        # subcategories
        subcategory_objs: dict[str, SubCategorySchema] = {}
        for slug, data in subcategories_raw.items():
            parent = category_objs[data["category_slug"]]
            subcategory = await create_subcategory_service(
                session,
                SubCategoryCreateSchema(
                    name=data["name"],
                    slug=slug,
                    category_id=parent.id,
                ),
            )
            subcategory_objs[slug] = subcategory
        await session.flush()

        # products + first variant
        product_objs: dict[int, ProductSchema] = {}
        skipped: list[int] = []
        
        for item in products_data:
            pid = item["id"]
            meta = product_meta.get(pid)
            if meta is None: 
                skipped.append(pid)
                continue
            
            subcategory = subcategory_objs[meta["subcategory_slug"]]
            
            try:
                target = TargetKey(item["categories"])
            except ValueError:
                print(f"[WARN] target sconosciuto '{item['categories']}' per prodotto id={pid}, skip")
                skipped.append(pid)
                continue
            
            colors = item.get("colors", [])
            sizes = item.get("sizes", [])
            combos = [(color, size) for color in colors for size in sizes]
            stocks = distribute_stock(item.get("stock", 0), len(combos))
            
            if not combos:
                print(f"[WARN] nessun colore o dimensione per prodotto id={pid}, skip")
                skipped.append(pid)
                continue
            
            first_color, first_size = combos[0]
            first_stock = stocks[0]
            
            product = await create_product_service(
                session,
                ProductCreateSchema(
                    title=item["title"],
                    subtitle=item["subtitle"],
                    description=item["description"],
                    price_cents=to_cents(item["price"]),
                    sale_percent=item.get("sale", 0),
                    new_arrivals=item.get("newArrivals", False),
                    image_url=item["image"],
                    sub_category_id=subcategory.id,
                    variant=ProductVariantNestedCreateSchema(
                        size=first_size,
                        color_name=first_color["nome"],
                        color_hex=first_color["hex"],
                        target_key=target,
                        stock=first_stock
                    )
                ),
                skip_image_validation=True
            )
            product_objs[pid] = product
            
            # other variants
            for (color, size), stock in zip(combos[1:], stocks[1:]):
                await create_variant_service(
                    session,
                    ProductVariantCreateSchema(
                        product_id=product.id,
                        size=size,
                        color_name=color["nome"],
                        color_hex=color["hex"],
                        target_key=target,
                        stock=stock
                    )
                )
        
        if skipped:
            print(f"[WARN] skipped {len(skipped)} products: {skipped}")
        
        # site reviews
        for index, user in enumerate(fake_users):
            review_source = reviews_data[index % len(reviews_data)]
            await create_site_review_service(
                user.id,
                SiteReviewCreateSchema(
                    rating=review_source["Stars"],
                    message=review_source["Description"]
                ),
                session
            )
        
        
        # product reviews    
        import random
        product_ids = list(product_objs.keys())
        
        for user in fake_users:
            reviews_count = random.randint(3, 4)
            target_products = random.sample(product_ids, min(reviews_count, len(product_ids)))        
        
            for pid in target_products:
                product = product_objs[pid]
                source_review = random.choice(product_reviews_data)
                description = (
                    f"{source_review['Description']} "
                    f"({product.title}, {product.subtitle})"
                )
                
                available_values = (1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5)
                await create_product_review_service(
                    user.id,
                    product.id,
                    ProductReviewCreateSchema(
                        rating=random.choice(available_values),
                        message=description
                    ),
                    session
                )
    
    print("Seed completato con successo.")


if __name__ == "__main__":
    asyncio.run(seed())