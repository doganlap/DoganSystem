"""
Environment Variable Validator
Validates required environment variables at startup to prevent deployment with placeholder values.
"""

import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnvironmentValidationError(Exception):
    """Exception raised when environment validation fails"""
    pass


def validate_environment_variables():
    """
    Validates all required environment variables.
    Fails fast if any placeholders or missing values are detected.
    """
    errors = []
    warnings = []

    # Define required environment variables and their placeholder patterns
    required_vars = {
        'CLAUDE_API_KEY': ['YOUR_ANTHROPIC_API_KEY', 'REPLACE', 'TODO', 'CHANGEME'],
        'ERPNEXT_API_KEY': ['REPLACE_AFTER_SETUP', 'REPLACE', 'TODO', 'CHANGEME'],
        'ERPNEXT_API_SECRET': ['REPLACE_AFTER_SETUP', 'REPLACE', 'TODO', 'CHANGEME'],
    }

    # Define password variables that should not have weak values
    password_vars = {
        'ERPNEXT_ADMIN_PASSWORD': ['admin', 'admin123', 'password', 'PASSWORD'],
        'MYSQL_ROOT_PASSWORD': ['admin', 'admin123', 'password', 'PASSWORD', 'root'],
        'MYSQL_PASSWORD': ['admin', 'admin123', 'password', 'PASSWORD', 'erpnext123'],
        'REDIS_PASSWORD': ['admin', 'admin123', 'password', 'PASSWORD', 'redis'],
        'GRAFANA_ADMIN_PASSWORD': ['admin', 'admin123', 'password', 'PASSWORD'],
    }

    # Validate required API keys
    for var_name, placeholder_patterns in required_vars.items():
        value = os.getenv(var_name)

        if not value:
            errors.append(f"❌ CRITICAL: {var_name} is not set")
            continue

        # Check if value matches any placeholder pattern
        value_upper = value.upper()
        for pattern in placeholder_patterns:
            if pattern.upper() in value_upper:
                errors.append(f"❌ CRITICAL: {var_name} contains placeholder value: {value}")
                break

    # Validate password strength
    for var_name, weak_patterns in password_vars.items():
        value = os.getenv(var_name)

        if not value:
            warnings.append(f"⚠️  WARNING: {var_name} is not set")
            continue

        # Check minimum length
        if len(value) < 16:
            warnings.append(f"⚠️  WARNING: {var_name} is shorter than 16 characters (current: {len(value)})")

        # Check if value matches any weak pattern
        value_lower = value.lower()
        for pattern in weak_patterns:
            if pattern.lower() == value_lower or pattern.lower() in value_lower:
                errors.append(f"❌ CRITICAL: {var_name} contains weak/default password")
                break

        # Check if value matches placeholder pattern
        if 'REPLACE' in value.upper() or 'CHANGE' in value.upper() or 'TODO' in value.upper():
            errors.append(f"❌ CRITICAL: {var_name} contains placeholder value")

    # Optional but recommended variables
    optional_vars = ['STRIPE_SECRET_KEY', 'STRIPE_WEBHOOK_SECRET']
    for var_name in optional_vars:
        value = os.getenv(var_name)
        if value and ('REPLACE' in value.upper() or 'TODO' in value.upper()):
            warnings.append(f"⚠️  WARNING: {var_name} contains placeholder value: {value}")

    # Print results
    if errors or warnings:
        logger.error("=" * 80)
        logger.error("ENVIRONMENT VARIABLE VALIDATION FAILED")
        logger.error("=" * 80)

        if errors:
            logger.error("\n🚨 CRITICAL ERRORS (Application will not start):")
            for error in errors:
                logger.error(f"  {error}")

        if warnings:
            logger.warning("\n⚠️  WARNINGS (Application will start but may have issues):")
            for warning in warnings:
                logger.warning(f"  {warning}")

        logger.error("\n" + "=" * 80)
        logger.error("PLEASE FIX THE ISSUES ABOVE BEFORE DEPLOYING TO PRODUCTION")
        logger.error("=" * 80)

        if errors:
            raise EnvironmentValidationError(
                f"Environment validation failed with {len(errors)} critical error(s). "
                f"See logs above for details."
            )
    else:
        logger.info("✅ All environment variables validated successfully")


def validate_api_key_format(api_key: str, key_name: str) -> bool:
    """
    Validates API key format.
    Returns True if valid, False otherwise.
    """
    if not api_key or len(api_key) < 20:
        logger.error(f"❌ {key_name} is too short (minimum 20 characters)")
        return False

    # Check for placeholder patterns
    placeholder_patterns = ['REPLACE', 'TODO', 'CHANGEME', 'YOUR_', 'EXAMPLE']
    for pattern in placeholder_patterns:
        if pattern.upper() in api_key.upper():
            logger.error(f"❌ {key_name} contains placeholder pattern: {pattern}")
            return False

    return True


if __name__ == "__main__":
    try:
        validate_environment_variables()
        sys.exit(0)
    except EnvironmentValidationError as e:
        logger.error(f"Validation failed: {e}")
        sys.exit(1)
