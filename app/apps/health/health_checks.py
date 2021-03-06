import logging

import requests
from apps.health.utils import assert_bwv_health
from django.conf import settings
from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import ServiceUnavailable

logger = logging.getLogger(__name__)


class APIServiceCheckBackend(BaseHealthCheckBackend):
    """
    Generic base class for checking API services
    """

    critical_service = False
    api_url = None
    api_url_suffix = ""
    verbose_name = None

    def check_status(self):
        """Check service by opening and closing a broker channel."""
        logger.debug("Checking status of API url...")
        try:
            assert self.api_url, "The given api_url should be set"
            response = requests.get(f"{self.api_url}{self.api_url_suffix}")
            response.raise_for_status()
        except AssertionError as e:
            self.add_error(
                ServiceUnavailable("The given API endpoint has not been set"),
                e,
            )
        except ConnectionRefusedError as e:
            self.add_error(
                ServiceUnavailable("Unable to connect to API: Connection was refused."),
                e,
            )
        except BaseException as e:
            self.add_error(ServiceUnavailable("Unknown error"), e)
        else:
            logger.debug("Connection established. API is healthy.")

    def identifier(self):
        if self.verbose_name:
            return self.verbose_name

        return self.__class__.__name__


class BAGServiceCheck(APIServiceCheckBackend):
    """
    Endpoint for checking the BAG Service API Endpoint
    """

    critical_service = True
    api_url = settings.BAG_API_SEARCH_URL
    verbose_name = "BAG API Endpoint"


class ZakenServiceCheck(APIServiceCheckBackend):
    """
    Endpoint for checking the Zken API Endpoint
    """

    critical_service = True
    api_url = settings.ZAKEN_API_HEALTH_URL
    verbose_name = "Zaken API Endpoint"


class BWVDatabaseCheck(BaseHealthCheckBackend):
    def check_status(self):
        logger.debug("Checking status of API url...")
        try:
            assert_bwv_health()
        except ConnectionRefusedError as e:
            self.add_error(
                ServiceUnavailable(
                    "Unable to connect to BWV database: Connection was refused."
                ),
                e,
            )
        except BaseException as e:
            self.add_error(ServiceUnavailable("Unknown error"), e)
        else:
            logger.debug("Connection established. BWV database is healthy.")


# TODO: Expand with all the API services that are being used
