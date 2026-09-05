import logging
from decimal import Decimal

import httpx

from app.cache.redis import cache
from app.config import settings
from app.enums import CurrencyEnum

logger = logging.getLogger(__name__)

FALLBACK_RATES: dict[tuple[CurrencyEnum, CurrencyEnum], Decimal] = {
    (CurrencyEnum.USD, CurrencyEnum.RUB): Decimal(str(95.0)),
    (CurrencyEnum.USD, CurrencyEnum.EUR): Decimal(str(0.92)),
    (CurrencyEnum.EUR, CurrencyEnum.RUB): Decimal(str(103.26)),
    (CurrencyEnum.RUB, CurrencyEnum.USD): Decimal(str(0.0105)),
    (CurrencyEnum.EUR, CurrencyEnum.USD): Decimal(str(1.087)),
    (CurrencyEnum.RUB, CurrencyEnum.EUR): Decimal(str(0.0097)),
}


async def _cache_key(base: CurrencyEnum, target: CurrencyEnum) -> str:
    return f"exchange_rate:{base.value}:{target.value}"


async def get_exchange_rate(base: CurrencyEnum, target: CurrencyEnum) -> Decimal:
    key = await _cache_key(base, target)

    cached_rate = await cache.get(key)
    if cached_rate is not None:
        return Decimal(cached_rate)

    url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base.value}.json"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
        rates = data.get(base.value, {})
        rate = rates.get(target.value)

        if rate is None:
            raise KeyError("Rate not found")

        rate = Decimal(str(rate))
        await cache.set(key, str(rate), ttl_seconds=settings.cache_ttl_seconds)
        return rate
    except Exception:
        logger.warning(
            "Failed to retrieve the %s->%s exchange rate from the external API, using fallback",
            base.value,
            target.value,
            exc_info=True,
        )
        return FALLBACK_RATES.get((base, target), Decimal(1))


async def invalidate_exchange_rate(base: CurrencyEnum, target: CurrencyEnum) -> None:
    await cache.delete(await _cache_key(base, target))
