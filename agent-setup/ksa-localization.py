"""
KSA Localization - Saudi Arabia specific localization per tenant
Arabic language, timezone, currency, calendar, business hours
"""

import pytz
import logging
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass

try:
    from hijri_converter import Hijri, Gregorian
    HIJRI_AVAILABLE = True
except ImportError:
    HIJRI_AVAILABLE = False
    logger.warning("hijri-converter not installed. Install with: pip install hijri-converter")

from tenant_isolation import TenantIsolation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class KSALocalization:
    """KSA localization settings"""
    tenant_id: str
    locale: str = "ar_SA"
    timezone: str = "Asia/Riyadh"
    currency: str = "SAR"
    work_week_start: str = "Saturday"
    work_week_end: str = "Wednesday"
    language: str = "ar"
    enable_hijri_calendar: bool = True


class KSALocalizationManager:
    """Manages KSA localization per tenant"""
    
    def __init__(self, tenant_isolation: TenantIsolation):
        self.tenant_isolation = tenant_isolation
        self.ksa_tz = pytz.timezone("Asia/Riyadh")
    
    def get_localization(self, tenant_id: str) -> KSALocalization:
        """Get localization settings for tenant"""
        with self.tenant_isolation.tenant_database(tenant_id) as conn:
            conn.row_factory = lambda cursor, row: {
                col[0]: row[idx] for idx, col in enumerate(cursor.description)
            }
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM tenant_config WHERE tenant_id = ?
            """, (tenant_id,))
            
            row = cursor.fetchone()
            if not row:
                # Return defaults
                return KSALocalization(tenant_id=tenant_id)
            
            return KSALocalization(
                tenant_id=tenant_id,
                locale=row.get("locale", "ar_SA"),
                timezone=row.get("timezone", "Asia/Riyadh"),
                currency=row.get("currency", "SAR"),
                work_week_start=row.get("work_week_start", "Saturday"),
                work_week_end=row.get("work_week_end", "Wednesday"),
                language=row.get("language", "ar"),
                enable_hijri_calendar=row.get("enable_hijri_calendar", True)
            )
    
    def update_localization(
        self,
        tenant_id: str,
        locale: Optional[str] = None,
        timezone: Optional[str] = None,
        currency: Optional[str] = None,
        work_week_start: Optional[str] = None,
        work_week_end: Optional[str] = None,
        language: Optional[str] = None,
        enable_hijri_calendar: Optional[bool] = None
    ) -> bool:
        """Update localization settings"""
        with self.tenant_isolation.tenant_database(tenant_id) as conn:
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if locale:
                updates.append("locale = ?")
                params.append(locale)
            
            if timezone:
                updates.append("timezone = ?")
                params.append(timezone)
            
            if currency:
                updates.append("currency = ?")
                params.append(currency)
            
            if work_week_start:
                updates.append("work_week_start = ?")
                params.append(work_week_start)
            
            if work_week_end:
                updates.append("work_week_end = ?")
                params.append(work_week_end)
            
            if language:
                updates.append("language = ?")
                params.append(language)
            
            if enable_hijri_calendar is not None:
                updates.append("enable_hijri_calendar = ?")
                params.append(enable_hijri_calendar)
            
            if not updates:
                return False
            
            updates.append("updated_at = ?")
            params.append(datetime.now().isoformat())
            params.append(tenant_id)
            
            query = f"UPDATE tenant_config SET {', '.join(updates)} WHERE tenant_id = ?"
            cursor.execute(query, params)
            
            conn.commit()
            
            return cursor.rowcount > 0
    
    def to_local_time(self, tenant_id: str, utc_time: datetime) -> datetime:
        """Convert UTC time to tenant's local time"""
        loc = self.get_localization(tenant_id)
        tz = pytz.timezone(loc.timezone)
        
        if utc_time.tzinfo is None:
            utc_time = pytz.UTC.localize(utc_time)
        
        return utc_time.astimezone(tz)
    
    def to_utc_time(self, tenant_id: str, local_time: datetime) -> datetime:
        """Convert tenant's local time to UTC"""
        loc = self.get_localization(tenant_id)
        tz = pytz.timezone(loc.timezone)
        
        if local_time.tzinfo is None:
            local_time = tz.localize(local_time)
        
        return local_time.astimezone(pytz.UTC)
    
    def format_currency(self, tenant_id: str, amount: float) -> str:
        """Format amount in tenant's currency"""
        loc = self.get_localization(tenant_id)
        
        if loc.currency == "SAR":
            return f"{amount:,.2f} ر.س"  # Saudi Riyal with Arabic
        else:
            return f"{loc.currency} {amount:,.2f}"
    
    def is_business_day(self, tenant_id: str, date: datetime) -> bool:
        """Check if date is a business day for tenant"""
        loc = self.get_localization(tenant_id)
        
        # KSA work week: Saturday to Wednesday
        weekday = date.weekday()  # Monday=0, Sunday=6
        
        work_week_map = {
            "Saturday": 5,
            "Sunday": 6,
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4
        }
        
        start_day = work_week_map.get(loc.work_week_start, 5)
        end_day = work_week_map.get(loc.work_week_end, 2)
        
        # Handle week wrap-around
        if start_day <= end_day:
            return start_day <= weekday <= end_day
        else:
            return weekday >= start_day or weekday <= end_day
    
    def is_business_hours(self, tenant_id: str, time: datetime) -> bool:
        """Check if time is within business hours (9 AM - 6 PM KSA)"""
        if not self.is_business_day(tenant_id, time):
            return False
        
        local_time = self.to_local_time(tenant_id, time)
        hour = local_time.hour
        
        # KSA business hours: 9 AM - 6 PM
        return 9 <= hour < 18
    
    def to_hijri_date(self, tenant_id: str, gregorian_date: datetime) -> Optional[Dict[str, Any]]:
        """Convert Gregorian date to Hijri"""
        loc = self.get_localization(tenant_id)
        
        if not loc.enable_hijri_calendar or not HIJRI_AVAILABLE:
            return None
        
        try:
            hijri = Gregorian(
                gregorian_date.year,
                gregorian_date.month,
                gregorian_date.day
            ).to_hijri()
            
            return {
                "year": hijri.year,
                "month": hijri.month,
                "day": hijri.day,
                "formatted": f"{hijri.year}/{hijri.month}/{hijri.day}"
            }
        except Exception as e:
            logger.error(f"Error converting to Hijri: {str(e)}")
            return None
    
    def from_hijri_date(self, tenant_id: str, hijri_year: int, hijri_month: int, hijri_day: int) -> Optional[datetime]:
        """Convert Hijri date to Gregorian"""
        loc = self.get_localization(tenant_id)
        
        if not loc.enable_hijri_calendar or not HIJRI_AVAILABLE:
            return None
        
        try:
            gregorian = Hijri(hijri_year, hijri_month, hijri_day).to_gregorian()
            return datetime(gregorian.year, gregorian.month, gregorian.day)
        except Exception as e:
            logger.error(f"Error converting from Hijri: {str(e)}")
            return None
    
    def get_next_business_day(self, tenant_id: str, date: datetime) -> datetime:
        """Get next business day"""
        next_day = date + timedelta(days=1)
        while not self.is_business_day(tenant_id, next_day):
            next_day += timedelta(days=1)
        return next_day
    
    def format_date(self, tenant_id: str, date: datetime, include_hijri: bool = False) -> str:
        """Format date according to tenant's locale"""
        loc = self.get_localization(tenant_id)
        local_date = self.to_local_time(tenant_id, date)
        
        if loc.language == "ar":
            # Arabic date format
            formatted = local_date.strftime("%Y/%m/%d")
            if include_hijri and loc.enable_hijri_calendar:
                hijri = self.to_hijri_date(tenant_id, date)
                if hijri:
                    formatted += f" ({hijri['formatted']} هـ)"
            return formatted
        else:
            # English date format
            formatted = local_date.strftime("%Y-%m-%d")
            if include_hijri and loc.enable_hijri_calendar:
                hijri = self.to_hijri_date(tenant_id, date)
                if hijri:
                    formatted += f" (Hijri: {hijri['formatted']})"
            return formatted


# Example usage
if __name__ == "__main__":
    from tenant_manager import TenantManager
    from tenant_isolation import TenantIsolation
    
    tenant_manager = TenantManager()
    tenant_isolation = TenantIsolation(tenant_manager)
    ksa_local = KSALocalizationManager(tenant_isolation)
    
    tenant = tenant_manager.get_tenant_by_subdomain("testco")
    if tenant:
        # Get localization
        loc = ksa_local.get_localization(tenant.tenant_id)
        print(f"Locale: {loc.locale}, Timezone: {loc.timezone}, Currency: {loc.currency}")
        
        # Format currency
        formatted = ksa_local.format_currency(tenant.tenant_id, 1234.56)
        print(f"Formatted currency: {formatted}")
        
        # Check business day
        now = datetime.now()
        is_business = ksa_local.is_business_day(tenant.tenant_id, now)
        print(f"Is business day: {is_business}")
