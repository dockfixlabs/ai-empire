from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.models.user import User
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=ProductListResponse)
async def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str = Query(None),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Product).where(Product.user_id == user.id)
    count_query = select(func.count()).select_from(Product).where(Product.user_id == user.id)

    if status:
        query = query.where(Product.status == status)
        count_query = count_query.where(Product.status == status)

    total_result = await db.execute(count_query)
    total = total_result.scalar()

    query = query.order_by(Product.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    products = result.scalars().all()

    return ProductListResponse(
        products=[ProductResponse.model_validate(p) for p in products],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("", response_model=ProductResponse, status_code=201)
async def create_product(
    data: ProductCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    product = Product(
        user_id=user.id,
        title=data.title,
        description=data.description,
        price=data.price,
        category=data.category,
        tags=data.tags,
        content_type=data.content_type,
        ai_generated=data.ai_generated,
        generation_prompt=data.generation_prompt,
    )
    db.add(product)
    await db.flush()
    return ProductResponse.model_validate(product)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Product).where(Product.id == product_id, Product.user_id == user.id)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse.model_validate(product)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    data: ProductUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Product).where(Product.id == product_id, Product.user_id == user.id)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    await db.flush()
    return ProductResponse.model_validate(product)


@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Product).where(Product.id == product_id, Product.user_id == user.id)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.delete(product)
