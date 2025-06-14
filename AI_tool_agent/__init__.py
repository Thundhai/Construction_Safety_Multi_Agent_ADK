from .root_agent import get_agent
from .root_agent import RootAgent  # Make sure RootAgent is the correct class/type name

# Add type hint for root_agent
root_agent: RootAgent = get_agent()
