import os
import ldclient
from ldclient.config import Config
from ldclient.context import Context
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def evaluate_flag(sdk_key, feature_flag_key, user_email, subscription_status, purchase_count):
    """
    This function evaluates the feature flag using user-specific data like email, 
    subscription status, and purchase count. It also provides the reason for why 
    the feature flag evaluated to True or False.
    """
    
    # Initialize LaunchDarkly client
    ldclient.set_config(Config(sdk_key))

    # Create a context with user email, subscription status, and purchase count
    context = Context.builder(user_email) \
        .kind('user') \
        .set("email", user_email) \
        .set("subscription_status", subscription_status) \
        .set("purchase_count", purchase_count) \
        .build()

    # Get detailed evaluation of the feature flag
    flag_detail = ldclient.get().variation_detail(feature_flag_key, context, False)
    flag_status = flag_detail.value
    flag_reason = flag_detail.reason

    # Print the flag evaluation result and the reason why
    print(f"LaunchDarkly Feature flag '{feature_flag_key}' for user '{user_email}' evaluated to: {flag_status}")
    print(f"Reason: {flag_reason}")

    # Close the LaunchDarkly client after evaluation
    ldclient.get().close()

    return flag_detail

# Example usage
if __name__ == "__main__":
    sdk_key = os.getenv("LAUNCHDARKLY_API_KEY")
    feature_flag_key = "premium-content"
    user_email = "user1@example.com"  # Test user email
    subscription_status = "premium"  # Example subscription status
    purchase_count = 3  # Example purchase count

    # Get the flag status and reason for evaluation
    flag_detail = evaluate_flag(sdk_key, feature_flag_key, user_email, subscription_status, purchase_count)