from fastapi import APIRouter, Depends, HTTPException, Request as FastAPIRequest, Query
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.user import User
from app.models.product import Product
from app.dependencies import get_current_user
from app.services.gumroad import GumroadService
from app.services.gumroad_oauth import GumroadOAuth
from app.core.config import get_settings
import secrets

router = APIRouter(prefix="/gumroad", tags=["Gumroad Integration"])
settings = get_settings()


@router.get("/connect")
async def connect_gumroad(
    request: FastAPIRequest,
    token: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Initiate Gumroad OAuth flow - works from browser with ?token= or with auth header"""
    from app.core.security import decode_access_token

    user = None
    auth_header = request.headers.get("authorization", "")
    if auth_header.startswith("Bearer "):
        payload = decode_access_token(auth_header[7:])
        if payload:
            result = await db.execute(select(User).where(User.id == payload.get("sub")))
            user = result.scalar_one_or_none()
    elif token:
        payload = decode_access_token(token)
        if payload:
            result = await db.execute(select(User).where(User.id == payload.get("sub")))
            user = result.scalar_one_or_none()

    if not user:
        return HTMLResponse("""
        <html dir="rtl">
        <head><title>Gumroad AI Empire - Connect</title>
        <style>
          body { font-family: 'Cairo', sans-serif; background: #030712; color: #fff; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
          .card { background: #1e1b4b; padding: 40px; border-radius: 20px; text-align: center; max-width: 500px; border: 1px solid #312e81; }
          h1 { font-size: 24px; margin-bottom: 10px; }
          p { color: #a5b4fc; margin-bottom: 20px; }
          a { display: inline-block; padding: 14px 32px; background: linear-gradient(135deg, #6366f1, #d946ef); color: white; text-decoration: none; border-radius: 12px; font-weight: bold; font-size: 16px; margin: 10px; }
          .hint { font-size: 13px; color: #64748b; margin-top: 20px; }
        </style></head>
        <body>
          <div class="card">
            <h1>ربط Gumroad</h1>
            <p>لربط حساب Gumroad مع نظام AI Empire، سجّل الدخول أو لائا من لوحة التحكم</p>
            <a href="http://localhost:5173">فتح لوحة التحكم</a>
            <div class="hint">بعد تسجيل الدخول، استخدم زر "ربط Gumroad" في الإعدادات</div>
          </div>
        </body></html>
        """, status_code=401)

    oauth = GumroadOAuth()
    state = secrets.token_urlsafe(32)

    redirect_uri = f"http://localhost:8000/api/v1/gumroad/callback"
    auth_url = oauth.get_authorization_url(redirect_uri, state)

    user.gumroad_refresh_token = state
    await db.commit()

    return RedirectResponse(url=auth_url)


@router.get("/callback")
async def gumroad_callback(
    code: str = None,
    state: str = None,
    error: str = None,
    db: AsyncSession = Depends(get_db),
):
    """Handle Gumroad OAuth callback (redirect from Gumroad -> no auth header)"""
    if error:
        return RedirectResponse(f"http://localhost:5173/?gumroad=error&msg={error}")
    if not code:
        return RedirectResponse("http://localhost:5173/?gumroad=error&msg=no_code")

    oauth = GumroadOAuth()
    redirect_uri = f"http://localhost:8000/api/v1/gumroad/callback"
    token_data = await oauth.exchange_code(code, redirect_uri)

    if not token_data:
        return RedirectResponse("http://localhost:5173/?gumroad=error&msg=token_exchange_failed")

    # Find user by state (temporarily stored in gumroad_refresh_token)
    result = await db.execute(
        select(User).where(User.gumroad_refresh_token == state)
    )
    user = result.scalar_one_or_none()

    if not user:
        return RedirectResponse("http://localhost:5173/?gumroad=error&msg=session_expired")

    user.gumroad_token = token_data.get("access_token")
    user.gumroad_refresh_token = token_data.get("refresh_token")
    await db.flush()

    # Get JWT token for redirect
    from app.core.security import create_access_token
    jwt_token = create_access_token({"sub": user.id})
    return RedirectResponse(f"http://localhost:5173/?gumroad=connected&token={jwt_token}")


@router.get("/products")
async def get_gumroad_products(user: User = Depends(get_current_user)):
    token = user.gumroad_token or settings.gumroad_api_key
    if not token:
        raise HTTPException(status_code=400, detail="Gumroad not connected. Set GUMROAD_API_KEY or connect via OAuth.")

    gumroad = GumroadService(access_token=token)
    try:
        products = await gumroad.get_products()
        return {"products": products, "count": len(products)}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Gumroad API error: {str(e)}")
    finally:
        await gumroad.close()


@router.get("/sales")
async def get_gumroad_sales(product_id: str = None, user: User = Depends(get_current_user)):
    token = user.gumroad_token or settings.gumroad_api_key
    if not token:
        raise HTTPException(status_code=400, detail="Gumroad not connected.")

    gumroad = GumroadService(access_token=token)
    try:
        sales = await gumroad.get_sales(product_id)
        return {"sales": sales, "count": len(sales)}
    finally:
        await gumroad.close()


@router.post("/sync")
async def sync_from_gumroad(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    token = user.gumroad_token or settings.gumroad_api_key
    if not token:
        raise HTTPException(status_code=400, detail="Gumroad not connected.")

    gumroad = GumroadService(access_token=token)
    try:
        products = await gumroad.get_products()
        synced = 0
        for gp in products:
            existing = await db.execute(
                select(Product).where(
                    Product.gumroad_product_id == gp["id"],
                    Product.user_id == user.id,
                )
            )
            if not existing.scalar_one_or_none():
                product = Product(
                    user_id=user.id,
                    gumroad_product_id=gp["id"],
                    title=gp.get("name", "Untitled"),
                    price=float(gp.get("price", 0)) / 100,
                    is_published=gp.get("published", False),
                    gumroad_data=gp,
                )
                db.add(product)
                synced += 1

        await db.flush()
        return {"synced": synced, "total": len(products), "products": products}
    finally:
        await gumroad.close()


@router.post("/publish/{product_id}")
async def publish_to_gumroad(
    product_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not user.gumroad_token:
        raise HTTPException(status_code=400, detail="Gumroad not connected.")

    result = await db.execute(
        select(Product).where(Product.id == product_id, Product.user_id == user.id)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    gumroad = GumroadService(access_token=user.gumroad_token)
    try:
        if product.gumroad_product_id:
            gp = await gumroad.update_product(
                product.gumroad_product_id,
                name=product.title,
                description=product.description or product.title,
                price=product.price,
            )
        else:
            gp = await gumroad.create_product(
                name=product.title,
                description=product.description or product.title,
                price=product.price,
                tags=product.tags.split(",") if product.tags else None,
            )
            product.gumroad_product_id = gp.get("id")
            product.gumroad_data = gp

        product.status = "published"
        product.is_published = True
        product.published_at = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
        await db.flush()
        return {"product": gp, "message": "Published to Gumroad!"}
    finally:
        await gumroad.close()


@router.post("/token")
async def set_gumroad_token(
    data: dict,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Set Gumroad access token directly (simpler than OAuth)"""
    token = data.get("token")
    if not token:
        raise HTTPException(status_code=400, detail="Token required")

    user.gumroad_token = token
    await db.flush()

    gumroad = GumroadService(access_token=token)
    try:
        user_info = await gumroad.get_user()
        return {
            "message": "Gumroad token saved!",
            "connected": True,
            "user": user_info.get("user", {}).get("email", "unknown"),
            "token_preview": token[:20] + "...",
        }
    except Exception as e:
        user.gumroad_token = None
        await db.flush()
        raise HTTPException(status_code=400, detail=f"Invalid Gumroad token: {e}")
    finally:
        await gumroad.close()


@router.get("/verify")
async def verify_gumroad(user: User = Depends(get_current_user)):
    """Verify Gumroad connection is working"""
    if not user.gumroad_token:
        raise HTTPException(status_code=400, detail="Gumroad not connected.")

    gumroad = GumroadService(access_token=user.gumroad_token)
    try:
        user_info = await gumroad.get_user()
        return {
            "connected": True,
            "user": user_info.get("user", {}).get("email", "unknown"),
        }
    except Exception as e:
        return {"connected": False, "error": str(e)}
    finally:
        await gumroad.close()
