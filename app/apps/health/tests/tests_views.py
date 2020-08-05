"""
Tests for the health views
"""
from unittest.mock import Mock, patch

from apps.health.views import BWV_TABLES, health_bwv, health_default
from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from app.utils.unittest_helpers import get_unauthenticated_client


class HealthViewsTests(TestCase):
    @patch("apps.health.views.assert_health_generic")
    def test_health_default(self, mock_assert_health_generic):
        """
        health_default calls assert_health_generic with the correct database
        """
        mock_request = Mock()
        health_default(mock_request)
        mock_assert_health_generic.assert_called_with(
            database_name=settings.DEFAULT_DATABASE_NAME
        )

    @patch("apps.health.views.assert_health_generic")
    def test_health_bwv(self, mock_assert_health_generic):
        """
        health_bwv calls assert_health_generic with the correct bwv database
        """
        mock_request = Mock()
        health_bwv(mock_request)
        mock_assert_health_generic.assert_called_with(
            database_name=settings.BWV_DATABASE_NAME
        )

    @patch("apps.health.views.assert_health_generic")
    @patch("apps.health.views.assert_health_database_tables")
    def test_health_bwv_tables(
        self, mock_assert_health_database_tables, mock_assert_health_generic
    ):
        """
        health_bwv calls assert_health_database_tables with the correct bwv database and tables
        """
        mock_request = Mock()
        health_bwv(mock_request)
        mock_assert_health_database_tables.assert_called_with(
            database_name=settings.BWV_DATABASE_NAME, tables=BWV_TABLES
        )


class HealthViewsUrlsTests(TestCase):
    @patch("apps.health.views.assert_health_generic")
    def test_health_default_url_view(self, mock_assert_health_generic):
        """
        URL endpoint for health_default can be called
        """
        url = reverse("health-default")
        client = get_unauthenticated_client()
        response = client.get(url)

        mock_assert_health_generic.assert_called()
        self.assertEquals(response.status_code, 200)

    @patch("apps.health.views.assert_health_generic")
    @patch("apps.health.views.assert_health_database_tables")
    def test_health_bwv_url_view(
        self, mock_assert_health_generic, mock_assert_health_database_tables
    ):
        """
        URL endpoint for health_bwv can be called
        """
        url = reverse("health-bwv")
        client = get_unauthenticated_client()
        response = client.get(url)

        mock_assert_health_generic.assert_called()
        mock_assert_health_database_tables.assert_called()
        self.assertEquals(response.status_code, 200)
